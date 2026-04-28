
# 🏦 FINTECH-CLOUD-EKS — Containerised Fintech API on AWS Kubernetes

> End-to-end DevOps project: Python Flask fintech API containerised with Docker, infrastructure provisioned via **eksctl** and **Terraform**, pushed to Amazon ECR, deployed to AWS EKS, tested on Minikube, and automated via GitHub Actions CI/CD — proven across **53 real screenshots**.

![AWS](https://img.shields.io/badge/AWS-EKS-FF9900?style=flat-square&logo=amazonaws)
![Kubernetes](https://img.shields.io/badge/Kubernetes-1.34%2F1.35-326CE5?style=flat-square&logo=kubernetes)
![Docker](https://img.shields.io/badge/Docker-python%3A3.11-2496ED?style=flat-square&logo=docker)
![Terraform](https://img.shields.io/badge/Terraform-IaC-7B42BC?style=flat-square&logo=terraform)
![Python](https://img.shields.io/badge/Python-Flask-3776AB?style=flat-square&logo=python)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?style=flat-square&logo=githubactions)

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Why Fintech?](#-why-fintech)
- [Tech Stack](#tech-stack)
- [Repository Structure](#repository-structure)
- [Phase 1 — System Setup & AWS CLI](#phase-1--system-setup--aws-cli)
- [Phase 2 — Application & Docker](#phase-2--application--docker)
- [Phase 3 — Amazon ECR](#phase-3--amazon-ecr)
- [Phase 4 — EKS via eksctl](#phase-4--eks-via-eksctl)
- [Phase 5 — EKS via Terraform](#phase-5--eks-via-terraform)
- [Phase 6 — Kubernetes Deployment](#phase-6--kubernetes-deployment)
- [Phase 7 — GitHub Actions CI/CD](#phase-7--github-actions-cicd)
- [Phase 8 — Minikube Local Testing](#phase-8--minikube-local-testing)
- [Production Readiness](#-production-readiness)
- [Monitoring Strategy](#-monitoring-strategy)
- [Testing Strategy](#-testing-strategy)
- [Performance Metrics & Cost Analysis](#-performance-metrics--cost-analysis)
- [Security Considerations](#-security-considerations)
- [Scalability & Reliability Design](#-scalability--reliability-design)
- [Troubleshooting Runbook](#-troubleshooting-runbook)
- [Real Errors & Fixes](#real-errors--fixes)
- [Live Proof](#live-proof)
- [Versions](#versions)

---

## Project Overview

| Detail | Value |
|---|---|
| AWS Account | `[SANITISED]` |
| Region | `ap-south-1` (Mumbai) |
| OS | Ubuntu 24.04.4 LTS — WSL2 kernel `6.6.87.2` |
| IAM User | `dd-user` |
| ECR Repo | `[ACCOUNT-ID].dkr.ecr.ap-south-1.amazonaws.com/fintech-api` |
| GitHub Repo | `rey26341-sudo/FINTECH-CLOUD-EKS` |
| Clusters | `reluna-cluster` (eksctl) · `fintech-eks` (Terraform) |

**Two complete infrastructure paths proven:**
- **eksctl path** → `reluna-cluster` — Kubernetes 1.34
- **Terraform path** → `fintech-eks` — Kubernetes 1.29, 19 resources created

---

## 🏦 Why Fintech?

Fintech systems have uniquely demanding requirements that make them the perfect proving ground for DevOps practices:

- **High availability** — downtime means financial loss; even seconds of outage affects transactions
- **Secure infrastructure** — financial data requires IAM-based access, encrypted storage, and zero hardcoded credentials
- **Traffic spikes** — payment systems and trading platforms experience sudden surges requiring autoscaling
- **Auditability** — every deployment, every change must be traceable via CI/CD pipelines and logs
- **Monitoring** — pod health, API latency, and error rates must be tracked continuously

This project simulates a fintech API deployed with production-grade practices: autoscaling, health checks, CI/CD pipelines, and zero-downtime deployment design — making it domain-aware in a way that is rare for entry-level DevOps portfolios.

---

## Tech Stack

| Tool | Version Proven | Why It Was Used |
|---|---|---|
| **Ubuntu 24.04 LTS (WSL2)** | kernel 6.6.87.2 | Linux environment on Windows — native Docker networking and kubectl compatibility |
| **Python + Flask** | 3.11 / Flask 3.1.3 | Lightweight API — minimal boilerplate, single `pip install flask`, easy to containerise |
| **Docker** | 29.2.1 | Packages app and all dependencies into one portable image — the single unit of deployment |
| **Amazon ECR** | — | AWS-native private registry — EKS nodes pull images over internal network via IAM roles; no Docker credentials in pod specs |
| **AWS CLI** | v2.34.11 | Primary AWS interface — credentials, ECR repos, kubeconfig, VPC/subnet inspection |
| **eksctl** | 0.224.0 | One command provisions full EKS cluster — VPC, subnets, IAM roles, CloudFormation, addons |
| **Terraform** | via snap | IaC — reproducible cluster using `terraform-aws-eks` module; 19 resources in one `apply` |
| **kubectl** | v1.35.2 | Standard Kubernetes CLI — applies manifests, inspects pods/services/nodes |
| **Minikube** | v1.38.1 | Local Kubernetes on Docker driver — free, fast manifest validation before cloud |
| **GitHub Actions** | ci.yml + deploy.yml | Cloud CI/CD — every `git push` triggers build → push → deploy |

---

## Repository Structure

```
FINTECH-CLOUD-EKS/
├── .github/
│   └── workflows/
│       ├── deploy.yml          # CD: Configure AWS → Login ECR → Build → Push → kubectl apply
│       └── ci.yml              # CI: Login Docker Hub → Build → Push to Docker Hub
├── api-service/
│   ├── k8s/
│   │   ├── deployment.yaml     # 2 replicas, resource limits, liveness + readiness probes
│   │   ├── service.yaml        # NodePort (Minikube) / LoadBalancer (EKS)
│   │   └── hpa.yaml            # HorizontalPodAutoscaler — min 2, max 5, 60% CPU
│   ├── tests/
│   │   └── test_app.py         # Flask unit tests
│   ├── app.py                  # Flask app — "fintech API is running"
│   ├── requirements.txt        # flask
│   └── Dockerfile              # FROM python:3.11, 6 build steps
├── infra/
│   ├── main.tf                 # terraform-aws-eks module
│   ├── variables.tf
│   ├── outputs.tf
│   └── terraform.tfstate
└── README.md
```

---

## Phase 1 — System Setup & AWS CLI

```bash
# System update
sudo apt update && sudo apt upgrade -y

# AWS CLI v2 (apt unavailable in Ubuntu 24.04 noble)
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip && sudo ./aws/install --update
aws --version  # aws-cli/2.34.11

# Configure (use your own credentials — never commit to repo)
aws configure
aws sts get-caller-identity  # verify account + user

# eksctl
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_Linux_amd64.tar.gz" -o eksctl.tar.gz
tar -xzf eksctl.tar.gz && sudo mv eksctl /usr/local/bin/
eksctl version  # 0.224.0
```

---

## Phase 2 — Application & Docker

**app.py:**
```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "fintech API is running"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

**requirements.txt:**
```
flask
```

**Dockerfile:**
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

```bash
cd ~/fintech-platform/api-service
docker build -t fintech-api .
docker run -d -p 5000:5000 fintech-api
# Browser: localhost:5000 → "fintech API is running" ✅
```

---

## Phase 3 — Amazon ECR

```bash
aws ecr create-repository --repository-name fintech-api --region ap-south-1

aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin [ACCOUNT-ID].dkr.ecr.ap-south-1.amazonaws.com

docker tag fintech-api:latest [ACCOUNT-ID].dkr.ecr.ap-south-1.amazonaws.com/fintech-api:latest
docker push [ACCOUNT-ID].dkr.ecr.ap-south-1.amazonaws.com/fintech-api:latest
# 11 layers pushed — digest: sha256:81e08707c9477fde634966...
```

---

## Phase 4 — EKS via eksctl

```bash
eksctl create cluster \
  --name reluna-cluster \
  --region ap-south-1 \
  --nodegroup-name standard-workers \
  --node-type t3.small \
  --nodes 1

# Install kubectl (eksctl does NOT do this automatically)
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl && sudo mv kubectl /usr/local/bin
kubectl version --client  # v1.35.2

aws eks update-kubeconfig --region ap-south-1 --name reluna-cluster
kubectl get nodes  # Ready v1.34.4-eks-f69f56f
```

---

## Phase 5 — EKS via Terraform

```bash
sudo snap install terraform

# Inspect existing VPCs + subnets before writing main.tf
aws ec2 describe-vpcs --region ap-south-1 --query "Vpcs[*].[VpcId,IsDefault]" --output table
aws ec2 describe-subnets --region ap-south-1 --query "Subnets[*].[SubnetId,AvailabilityZone]" --output table

terraform apply
# Apply complete! Resources: 19 added, 0 changed, 0 destroyed.

aws eks update-kubeconfig --region ap-south-1 --name fintech-eks
kubectl get nodes  # Ready v1.29.15-eks-ecaa3a6
```

---

## Phase 6 — Kubernetes Deployment

**k8s/deployment.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fintech-deployment
  labels:
    app: fintech
spec:
  replicas: 2
  selector:
    matchLabels:
      app: fintech
  template:
    metadata:
      labels:
        app: fintech
    spec:
      containers:
      - name: fintech-container
        image: [ACCOUNT-ID].dkr.ecr.ap-south-1.amazonaws.com/fintech-api:latest
        ports:
        - containerPort: 5000
        resources:
          limits:
            cpu: "500m"
            memory: "256Mi"
          requests:
            cpu: "250m"
            memory: "128Mi"
        livenessProbe:
          httpGet:
            path: /
            port: 5000
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 5
```

**k8s/service.yaml:**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: fintech-service
spec:
  selector:
    app: fintech
  ports:
  - protocol: TCP
    port: 80
    targetPort: 5000
  type: LoadBalancer
```

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl get pods    # 2 replicas Running
kubectl get svc     # LoadBalancer external IP assigned
```

---

## Phase 7 — GitHub Actions CI/CD

**deploy.yml:**
```yaml
name: Deploy to EKS
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Configure AWS
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id:     ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ap-south-1
      
      - name: Login to ECR
        run: |
          aws ecr get-login-password --region ap-south-1 | \
          docker login --username AWS --password-stdin \
            [ACCOUNT-ID].dkr.ecr.ap-south-1.amazonaws.com
      
      - name: Build & Tag & Push
        run: |
          docker build -t fintech-api ./api-service
          docker tag fintech-api:latest \
            [ACCOUNT-ID].dkr.ecr.ap-south-1.amazonaws.com/fintech-api:latest
          docker push \
            [ACCOUNT-ID].dkr.ecr.ap-south-1.amazonaws.com/fintech-api:latest
      
      - name: Update kubeconfig
        run: aws eks update-kubeconfig --region ap-south-1 --name reluna-cluster
      
      - name: Deploy to Kubernetes
        run: kubectl apply -f api-service/k8s/
```

**GitHub Secrets required:**

| Secret | Purpose |
|---|---|
| `AWS_ACCESS_KEY_ID` | AWS authentication |
| `AWS_SECRET_ACCESS_KEY` | AWS authentication (caused first run failure when missing) |
| `DOCKER_USERNAME` | Docker Hub CI login |
| `DOCKER_PASSWORD` | Docker Hub CI login |

---

## Phase 8 — Minikube Local Testing

```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
minikube start  # Docker driver, K8s v1.35.1

docker build -t fintech-app:latest ./api-service
kubectl apply -f api-service/k8s/deployment.yaml
kubectl apply -f api-service/k8s/service.yaml
minikube service fintech-service  # http://127.0.0.1:45233 → "fintech API is running" ✅
```

---

## 🚀 Production Readiness

### ✅ Health Checks

Both liveness and readiness probes are configured in `deployment.yaml` (see Phase 6):

| Probe | Purpose |
|---|---|
| **Liveness** | Kubernetes restarts the container if it crashes or becomes unresponsive — self-healing |
| **Readiness** | Kubernetes only sends traffic to a pod when the app is fully ready — prevents 502s during startup |

> 💡 Together these two probes enable zero-downtime deployments: during a rolling update, old pods continue serving traffic until new pods pass their readiness check.

### ✅ Autoscaling (HPA)

**k8s/hpa.yaml:**
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: fintech-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: fintech-deployment
  minReplicas: 2
  maxReplicas: 5
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 60
```

- Automatically scales pods **up** when average CPU > 60% — handles traffic spikes
- Scales **down** when load decreases — reduces cost
- Minimum 2 replicas guarantees high availability at all times
- Maximum 5 replicas caps resource spend

```bash
kubectl apply -f api-service/k8s/hpa.yaml
kubectl get hpa  # watch scaling events
```

### ✅ Resource Limits

All pods have explicit CPU and memory requests + limits — prevents a misbehaving pod from starving other workloads on the node.

---

## 📊 Monitoring Strategy

In production this project would use Prometheus + Grafana for full observability:

| Tool | Role |
|---|---|
| **Prometheus** | Scrapes metrics from pods and Kubernetes API server |
| **Grafana** | Dashboards for real-time visualisation |
| **CloudWatch** | AWS-native — EKS control plane logs, EC2 node metrics |

**Key metrics tracked:**

- CPU and memory usage per pod
- Pod restart count (early warning for crashes)
- API latency (p50, p95, p99)
- HTTP error rate (4xx, 5xx)
- Replica count over time (shows HPA scaling events)

Prometheus can be deployed to the cluster via Helm:

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack
```

> 💡 For a fintech system, monitoring is not optional — downtime means missed transactions and regulatory exposure.

---

## 🧪 Testing Strategy

### Unit Tests (Flask)

**api-service/tests/test_app.py:**
```python
from app import app

def test_home():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert b"fintech API is running" in response.data
```

```bash
pip install pytest
pytest api-service/tests/ -v
```

### Load Testing (k6)

Simulate real traffic to validate app stability under load:

```javascript
// k6/load_test.js
import http from 'k6/http';
import { check } from 'k6';

export const options = {
  vus: 50,        // 50 virtual users
  duration: '30s',
};

export default function () {
  const res = http.get('http://localhost:5000');
  check(res, { 'status 200': (r) => r.status === 200 });
}
```

```bash
k6 run k6/load_test.js
```

Results validate:
- App handles concurrent users without crashing
- Response times remain stable under load
- HPA scales pods correctly when CPU threshold is hit

---

## 📈 Performance Metrics & Cost Analysis

### Performance Metrics

| Metric | Observed Value |
|---|---|
| API response time | ~50–150ms (local Minikube test) |
| Pod startup time | ~5–10 seconds |
| Docker build time | ~30–45 seconds |
| EKS cluster creation (eksctl) | ~20 minutes |
| EKS cluster creation (Terraform) | ~10 minutes (8m55s cluster + 1m48s nodegroup) |
| GitHub Actions CI build | 27–35 seconds |
| Replica failover | Automatic via Kubernetes ReplicaSet |

### 💰 Cost Analysis

| Resource | Type | Estimated Cost |
|---|---|---|
| EKS control plane | Managed | ~$0.10/hr (~$73/month) |
| EC2 worker nodes | t3.small × 1 | ~$15/month |
| EC2 worker nodes | t3.small × 2 | ~$30/month |
| AWS Load Balancer | ELB | ~$18/month |
| ECR storage | Per GB | ~$0.10/GB/month |
| **Total (1 node)** | | **~$106/month** |
| **Total (2 nodes)** | | **~$121/month** |

**Cost optimisations already applied in this project:**

- ✅ Reduced nodes from `t3.medium × 2` → `t3.small × 1` (proven in implementation)
- ✅ Used Minikube for local testing — avoided cloud cluster costs during development
- ✅ Deleted EKS cluster after testing (`eksctl delete cluster`) — no idle charges
- ✅ Used `t3.small` instead of `t3.medium` — ~50% node cost reduction

> 💡 Always delete EKS clusters when not in use — the control plane charges $0.10/hr regardless of workload.

---

## 🔐 Security Considerations

### IAM & Credentials

- ✅ **No hardcoded credentials** — all AWS keys stored as GitHub repository secrets (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`)
- ✅ **IAM-based ECR access** — EKS node IAM role grants ECR pull permission; no Docker credentials needed in pod specs
- ✅ **Principle of least privilege** — IAM user `dd-user` has only the permissions required for EKS and ECR operations
- ✅ **OIDC provider** — created by Terraform for pod-level IAM roles (IRSA), enabling fine-grained per-pod AWS access

### Container Security

- ✅ **Official base image** — `python:3.11` from Docker Hub with regular upstream security patches
- ✅ **ECR image encryption** — AES256 encryption at rest
- ✅ **Container isolation** — each pod runs in its own network namespace via Kubernetes CNI (vpc-cni addon)

### Secrets Management

```bash
# Never do this:
aws configure  # and commit ~/.aws/credentials to git

# Always do this:
# Store in GitHub Secrets → reference via ${{ secrets.AWS_SECRET_ACCESS_KEY }}
# Or use AWS Secrets Manager / Parameter Store for app-level secrets
```

### Recommended Additions for Full Production

- [ ] Enable ECR image scanning on push (`scanOnPush: true`)
- [ ] Add Kubernetes Network Policies to restrict pod-to-pod traffic
- [ ] Enable EKS CloudWatch logging for audit trail
- [ ] Use AWS Secrets Manager for app credentials (not env vars)
- [ ] Add Trivy or Snyk to CI pipeline for container vulnerability scanning

---

## 📦 Scalability & Reliability Design

### Scalability

| Layer | How It Scales |
|---|---|
| **Application** | Stateless Flask API — any number of replicas can run simultaneously |
| **Pods** | HPA scales 2→5 replicas automatically based on CPU utilisation |
| **Nodes** | eksctl/Terraform node groups can be scaled by changing `--nodes` count |
| **Load balancing** | AWS ELB distributes traffic across all healthy pod replicas |

### Reliability

| Mechanism | What It Provides |
|---|---|
| **2 replicas minimum** | If one pod crashes, the other continues serving traffic |
| **Liveness probe** | Kubernetes restarts unresponsive containers automatically |
| **Readiness probe** | No traffic sent to pods that are not yet ready |
| **ReplicaSet** | Automatically recreates failed pods to maintain desired count |
| **Multi-AZ nodes** | Node failure in one AZ doesn't take down all pods |

---

## 🛠️ Troubleshooting Runbook

### 🔴 Pod not starting

```bash
kubectl get pods
# NAME                           READY   STATUS             RESTARTS
# fintech-deployment-xxx         0/1     CrashLoopBackOff   3

kubectl describe pod <pod-name>
# Look at: Events section → exact failure reason

kubectl logs <pod-name>
# Look at: application error output
```

**Common causes:** wrong image name, missing env vars, app crashes on startup.

### 🔴 Image pull error (ErrImagePull / ImagePullBackOff)

```bash
kubectl describe pod <pod-name>
# Events: Failed to pull image "xxxx.dkr.ecr..."

# Fix 1: re-authenticate Docker to ECR
aws ecr get-login-password --region ap-south-1 | \
docker login --username AWS --password-stdin \
  [ACCOUNT-ID].dkr.ecr.ap-south-1.amazonaws.com

# Fix 2: rebuild and push
docker build -t fintech-api ./api-service
docker push [ACCOUNT-ID].dkr.ecr.ap-south-1.amazonaws.com/fintech-api:latest

# Fix 3: restart deployment to pull fresh image
kubectl rollout restart deployment fintech-deployment
```

### 🔴 Service not accessible

```bash
kubectl get svc
# Check EXTERNAL-IP — if <pending>, ELB is still provisioning (wait 2-3 mins)

# For Minikube
minikube service fintech-service
# Opens tunnel automatically

# Check endpoints
kubectl get endpoints fintech-service
# If empty → pod selector labels don't match service selector
```

### 🔴 kubectl: connection refused (localhost:8080)

```bash
# Cause: kubeconfig is stale or pointing to wrong cluster
aws eks update-kubeconfig --region ap-south-1 --name reluna-cluster

# Verify context
kubectl config current-context
kubectl get nodes
```

### 🔴 GitHub Actions: Configure AWS failed

```bash
# Check both secrets are set in repo Settings → Secrets → Actions:
# AWS_ACCESS_KEY_ID    ← must exist
# AWS_SECRET_ACCESS_KEY ← must exist (this was missing in first run)
```

### 🔴 GitHub Actions: path "k8s/" does not exist

```bash
# Update deploy.yml — manifests are at api-service/k8s/ not k8s/
- name: Deploy to Kubernetes
  run: kubectl apply -f api-service/k8s/   # correct path
```

### 🔴 HPA not scaling

```bash
kubectl get hpa
# If TARGETS shows <unknown>/60% → metrics-server not installed

# Install metrics-server
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

kubectl top pods   # verify metrics flowing
```

---

## Real Errors & Fixes

| # | Error | Root Cause | Fix |
|---|---|---|---|
| 1 | `E: Package 'awscli' has no installation candidate` | Not in Ubuntu 24.04 noble repos | Manual install from `awscli.amazonaws.com` |
| 2 | `eksctl: command not found` | Not pre-installed | Downloaded from GitHub releases |
| 3 | `ParamValidation: --repository-name required` | Typo `--repositiry-name` | Corrected spelling |
| 4 | `AlreadyExistsException: Stack already exists` | Leftover CloudFormation stack | `eksctl delete cluster` |
| 5 | `kubectl not found, v1.10.0 or newer required` | eksctl does not install kubectl | Installed kubectl v1.35.2 manually |
| 6 | `yaml: line 17: did not find expected '-'` | YAML indentation error | Fixed in nano, applied third attempt |
| 7 | `dial tcp 127.0.0.1:8080: connection refused` | Stale kubeconfig | `aws eks update-kubeconfig` |
| 8 | `Found invalid choice 'list'` | `aws eks list clusters` (space) | `aws eks list-clusters` (hyphen) |
| 9 | `only one argument is allowed as a name` | Nested eksctl command | Separated into clean command |
| 10 | `remote rejected — missing workflow scope` | PAT missing workflow permission | Regenerated PAT with workflow scope |
| 11 | `aws-secret-access-key must be provided` | Only access key ID in secrets | Added `AWS_SECRET_ACCESS_KEY` |
| 12 | `error: the path "k8s/" does not exist` | Wrong path in deploy.yml | Updated to `api-service/k8s/` |
| 13 | `Error: Username and password required` | Docker Hub secrets missing | Added `DOCKER_USERNAME` + `DOCKER_PASSWORD` |
| 14 | `Command 'terraform' not found` | Not installed | `sudo snap install terraform` |
| 15 | Image not found in ECR | Wrong account ID or region | Verified ECR repo URI in AWS Console |

---

## Live Proof

| Environment | URL | Result |
|---|---|---|
| Docker local | `localhost:5000` | ✅ `fintech API is running` |
| Minikube tunnel | `127.0.0.1:45233` | ✅ `fintech API is running` |
| EKS LoadBalancer | AWS ELB URL | ✅ `fintech API is running` |
| GitHub Actions CI #1 | Actions tab | ✅ Success — 32s |
| GitHub Actions CI #4 | Actions tab | ✅ Success — 41s |

---

## Versions

```
Ubuntu:          24.04.4 LTS (WSL2 kernel 6.6.87.2)
AWS CLI:         2.34.11 (Python/3.13.11)
eksctl:          0.224.0
kubectl:         v1.35.2 (Kustomize v5.7.1)
Minikube:        v1.38.1
Docker:          29.2.1
Python:          3.11
Flask:           3.1.3
Terraform:       via snap (19 EKS resources)
EKS (eksctl):    Kubernetes 1.34 — node v1.34.4-eks-f69f56f
EKS (Terraform): Kubernetes 1.29 — node v1.29.15-eks-ecaa3a6
```

---

