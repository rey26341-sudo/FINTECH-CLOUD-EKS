import os
import sys
import json
from kubernetes import client, config
from groq import Groq

# 1. Initialize Kubernetes Local Client
try:
    config.load_kube_config()
except Exception:
    config.load_incluster_config()

v1 = client.CoreV1Api()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# 2. Define Diagnostic Tools
def get_pods(namespace="default"):
    """Lists all pods and their status in a namespace."""
    pods = v1.list_namespaced_pod(namespace)
    res = []
    for p in pods.items:
        restarts = p.status.container_statuses[0].restart_count if p.status.container_statuses else 0
        reason = "Running"
        if p.status.container_statuses and p.status.container_statuses[0].state.waiting:
            reason = p.status.container_statuses[0].state.waiting.reason
        elif p.status.container_statuses and p.status.container_statuses[0].state.terminated:
            reason = p.status.container_statuses[0].state.terminated.reason

        res.append({
            "name": p.metadata.name,
            "status": p.status.phase,
            "restarts": restarts,
            "reason": reason
        })
    return json.dumps(res)

def get_pod_logs(pod_name, namespace="default"):
    """Fetches trailing logs for a specific pod."""
    try:
        logs = v1.read_namespaced_pod_log(name=pod_name, namespace=namespace, tail_lines=50)
        return logs if logs else "No logs available."
    except Exception as e:
        return f"Error retrieving logs: {str(e)}"

def describe_pod(pod_name, namespace="default"):
    """Gets pod details and recent events."""
    try:
        pod = v1.read_namespaced_pod(name=pod_name, namespace=namespace)
        events = v1.list_namespaced_event(namespace, field_selector=f"involvedObject.name={pod_name}")

        event_list = [{"reason": e.reason, "message": e.message} for e in events.items[-5:]]

        return json.dumps({
            "status": pod.status.phase,
            "container_statuses": [
                {
                    "name": c.name,
                    "state": str(c.state),
                    "last_state": str(c.last_state)
                } for c in (pod.status.container_statuses or [])
            ],
            "recent_events": event_list
        })
    except Exception as e:
        return f"Error describing pod: {str(e)}"

# Function Tool Mapping
tools_map = {
    "get_pods": get_pods,
    "get_pod_logs": get_pod_logs,
    "describe_pod": describe_pod
}

tools_spec = [
    {
        "type": "function",
        "function": {
            "name": "get_pods",
            "description": "Lists all pods and their status in a namespace.",
            "parameters": {
                "type": "object",
                "properties": {
                    "namespace": {"type": "string", "default": "default"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_pod_logs",
            "description": "Fetches trailing logs for a specific pod.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pod_name": {"type": "string"},
                    "namespace": {"type": "string", "default": "default"}
                },
                "required": ["pod_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "describe_pod",
            "description": "Gets pod status details and recent events.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pod_name": {"type": "string"},
                    "namespace": {"type": "string", "default": "default"}
                },
                "required": ["pod_name"]
            }
        }
    }
]

def run_investigation(query):
    print(f"\n[USER PROMPT]: {query}\n")
    messages = [
        {"role": "system", "content": "You are an expert Kubernetes SRE agent. Interrogate cluster resources to diagnose issues. Return findings structured as: Evidence, Probable Root Cause, Recommended Action."},
        {"role": "user", "content": query}
    ]

    while True:
        response = groq_client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
            tools=tools_spec,
            tool_choice="auto"
        )

        msg = response.choices[0].message
        messages.append(msg)

        if not msg.tool_calls:
            print("\n=== INVESTIGATION REPORT ===")
            print(msg.content)
            break

        for tool_call in msg.tool_calls:
            func_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            print(f"🔧 [TOOL CALL]: {func_name}({args})")

            result = tools_map[func_name](**args)

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "Why is fintech-api failing?"
    run_investigation(query)
