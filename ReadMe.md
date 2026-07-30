# 🏦 FINTECH-CLOUD-EKS — Containerised Fintech API on AWS Kubernetes with Blockchain Settlement

> End-to-end DevOps + Web3 project: Python Flask fintech API with real **Ethereum Sepolia testnet** payment settlement, containerised with Docker, infrastructure provisioned via **eksctl** and **Terraform**, pushed to Amazon ECR, deployed to AWS EKS, tested on Minikube, and automated via GitHub Actions CI/CD.

[![AWS](https://img.shields.io/badge/AWS-EKS-FF9900?style=flat-square&logo=amazonaws)](#)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-1.34%2F1.35-326CE5?style=flat-square&logo=kubernetes)](#)
[![Docker](https://img.shields.io/badge/Docker-python%3A3.11-2496ED?style=flat-square&logo=docker)](#)
[![Terraform](https://img.shields.io/badge/Terraform-IaC-7B42BC?style=flat-square&logo=terraform)](#)
[![Python](https://img.shields.io/badge/Python-Flask-3776AB?style=flat-square&logo=python)](#)
[![Web3](https://img.shields.io/badge/Web3-Ethereum%20Sepolia-3C3C3D?style=flat-square&logo=ethereum)](#)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?style=flat-square&logo=githubactions)](#)

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
- [Phase 9 — Blockchain Settlement Layer (Ethereum Sepolia)](#phase-9--blockchain-settlement-layer-ethereum-sepolia)
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
- [Roadmap](#-roadmap)

---

## Project Overview

| Detail            | Value                                                        |
| ------------------ | ------------------------------------------------------------ |
| AWS Account        | `[SANITISED]`                                                |
| Region              | `ap-south-1` (Mumbai)                                        |
| OS                  | Ubuntu 24.04.4 LTS — WSL2 kernel `6.6.87.2`                  |
| IAM User            | `dd-user`                                                    |
| ECR Repo            | `[ACCOUNT-ID].dkr.ecr.ap-south-1.amazonaws.com/fintech-api`  |
| GitHub Repo         | `rey26341-sudo/FINTECH-CLOUD-EKS`                            |
| Clusters            | `reluna-cluster` (eksctl) · `fintech-eks` (Terraform)        |
| Blockchain Network  | Ethereum **Sepolia** testnet (chain ID `11155111`)           |
| Web3 Provider       | Alchemy RPC (HTTPS endpoint)                                 |

**Two complete infrastructure paths proven:**

- **eksctl path** → `reluna-cluster` — Kubernetes 1.34
- **Terraform path** → `fintech-eks` — Kubernetes 1.29, 19 resources created

**Beyond infrastructure**, the API now performs real on-chain settlement: `POST /invoice` signs and broadcasts an actual transaction to Ethereum Sepolia and returns the transaction hash, verifiable on Etherscan.

---

## 💡 Why Fintech?

Fintech systems have uniquely demanding requirements that make them the perfect proving ground for DevOps and Web3 practices:

- **High availability** — downtime means financial loss; even seconds of outage affects transactions
- **Secure infrastructure** — financial data requires IAM-based access, encrypted storage, and zero hardcoded credentials
- **Traffic spikes** — payment systems and trading platforms experience sudden surges requiring autoscaling
- **Auditability** — every deployment and every on-chain transaction is traceable — via CI/CD logs *and* a public blockchain explorer
- **Monitoring** — pod health, API latency, and error rates must be tracked continuously
- **Multi-chain readiness** — real fintech platforms can't assume a single blockchain; the settlement layer is built chain-agnostic from day one

---

## Tech Stack

| Tool                        | Version Proven      | Why It Was Used                                                                                                             |
| --------------------------- | -------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| **Ubuntu 24.04 LTS (WSL2)** | kernel 6.6.87.2      | Linux environment on Windows — native Docker networking and kubectl compatibility                                          |
| **Python + Flask**          | 3.11 / Flask 3.1.3   | Lightweight API — minimal boilerplate, easy to containerise                                                                 |
| **web3.py**                 | 7.16.0                | Python library for signing and broadcasting Ethereum transactions to Sepolia via JSON-RPC                                  |
| **eth-account**             | 0.13.7                | Wallet/key management — loads a private key and signs raw transactions locally before broadcast                            |
| **python-dotenv**           | 1.2.2                 | Loads RPC URLs and private keys from `.env` — keeps secrets out of source code                                             |
| **Alchemy**                  | —                    | Ethereum Sepolia RPC provider — HTTPS JSON-RPC endpoint for reading chain state and broadcasting signed transactions        |
| **Docker**                   | 29.2.1                | Packages app and all dependencies into one portable image — the single unit of deployment                                  |
| **Amazon ECR**               | —                    | AWS-native private registry — EKS nodes pull images over internal network via IAM roles; no Docker credentials in pod specs |
| **AWS CLI**                  | v2.34.11              | Primary AWS interface — credentials, ECR repos, kubeconfig, VPC/subnet inspection                                          |
| **eksctl**                   | 0.224.0               | One command provisions full EKS cluster — VPC, subnets, IAM roles, CloudFormation, addons                                  |
| **Terraform**                | via snap              | IaC — reproducible cluster using `terraform-aws-eks` module; 19 resources in one `apply`                                   |
| **kubectl**                  | v1.35.2               | Standard Kubernetes CLI — applies manifests, inspects pods/services/nodes                                                   |
| **Minikube**                 | v1.38.1               | Local Kubernetes on Docker driver — free, fast manifest validation before cloud                                            |
| **GitHub Actions**           | ci.yml + deploy.yml   | Cloud CI/CD — every `git push` triggers build → push → deploy                                                              |

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
│   ├── app.py                  # Flask app entrypoint — registers blueprints, health check
│   ├── config.py               # Loads Sepolia RPC URL / wallet key / chain ID from .env
│   ├── requirements.txt        # flask, web3, python-dotenv
│   └── Dockerfile              # FROM python:3.11, 6 build steps
├── blockchain/                 # Chain-agnostic settlement layer
│   ├── interface.py            # Single entrypoint routes/ talks to — hides chain-specific logic
│   └── ethereum/
│       ├── web3_client.py      # Web3 connection to Sepolia RPC
│       ├── wallet.py           # Wallet address + balance lookups
│       └── transaction.py      # Builds, signs, and broadcasts ETH transactions
├── routes/
│   ├── health.py                # /health endpoint
│   └── invoice.py               # POST /invoice — triggers on-chain settlement
├── models/                       # (reserved) data models for invoices/transactions
├── workers/                      # (reserved) background jobs — e.g. tx status polling
├── utils/                        # (reserved) shared helpers
├── config.py                     # Root-level config loader (mirrors api-service/config.py)
├── infra/
│   ├── main.tf                   # terraform-aws-eks module
│   ├── variables.tf
│   ├── outputs.tf
│   └── terraform.tfstate         # ⚠️ excluded from git — see Security Considerations
├── .env                           # ⚠️ never committed — RPC URL + private key
├── .gitignore
└── README.md
```

> **Note on `config.py` duplication:** both `/config.py` and `/api-service/config.py` currently exist with identical content. `api-service/app.py` adds the project root to `sys.path` so it can import the shared modules (`blockchain/`, `routes/`) that live outside `api-service/`. Consolidating into a single config module is on the [Roadmap](#-roadmap).

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

**requirements.txt:**
```
flask
web3
python-dotenv
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

> **Secrets in Kubernetes:** once `/invoice` is deployed to EKS, `WALLET_PRIVATE_KEY` must be injected as a Kubernetes `Secret`, not baked into the image or a plain ConfigMap. See [Security Considerations](#-security-considerations).

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

| Secret                  | Purpose                                                    |
| ------------------------ | ----------------------------------------------------------- |
| `AWS_ACCESS_KEY_ID`      | AWS authentication                                          |
| `AWS_SECRET_ACCESS_KEY`  | AWS authentication (caused first run failure when missing)  |
| `DOCKER_USERNAME`        | Docker Hub CI login                                         |
| `DOCKER_PASSWORD`        | Docker Hub CI login                                         |
| `SEPOLIA_RPC_URL`        | *(planned)* — inject at deploy time as a K8s Secret         |
| `WALLET_PRIVATE_KEY`     | *(planned)* — inject at deploy time as a K8s Secret         |

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

## Phase 9 — Blockchain Settlement Layer (Ethereum Sepolia)

The API now performs real on-chain payment settlement rather than just returning a status string. This phase adds a **chain-agnostic** blockchain module so additional networks (Polygon, Solana) can be added later without touching `routes/`.

### 9.1 — Design: chain-agnostic interface

```
blockchain/
├── interface.py         # send_payment(chain, to, value) / get_balance(chain, address)
└── ethereum/
    ├── web3_client.py    # Sepolia RPC connection
    ├── wallet.py          # address + balance lookups
    └── transaction.py     # build, sign, broadcast
```

`routes/invoice.py` only ever imports from `blockchain/interface.py` — never reaches into `blockchain/ethereum/` directly. Adding Polygon or Solana later means adding a new subfolder plus one `elif` branch in `interface.py`; **no route code changes**.

### 9.2 — Environment configuration

```bash
# .env  (never committed — see .gitignore)
SEPOLIA_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR_ALCHEMY_KEY
WALLET_PRIVATE_KEY=your_test_wallet_private_key
CHAIN_ID=11155111
```

RPC endpoint provisioned via an Alchemy app scoped to **Ethereum → Sepolia**, using the HTTPS JSON-RPC URL (not the WSS/websocket endpoint, which is only needed for real-time event subscriptions).

### 9.3 — Core modules

`blockchain/ethereum/web3_client.py` — establishes and validates the RPC connection:
```python
from web3 import Web3
from config import SEPOLIA_RPC_URL

def get_web3():
    w3 = Web3(Web3.HTTPProvider(SEPOLIA_RPC_URL))
    if not w3.is_connected():
        raise ConnectionError("Could not connect to Sepolia RPC")
    return w3
```

`blockchain/ethereum/transaction.py` — builds, signs, and broadcasts a transaction:
```python
from blockchain.ethereum.web3_client import get_web3
from blockchain.ethereum.wallet import get_account
from config import CHAIN_ID

def send_transaction(to_address, value_eth):
    w3 = get_web3()
    account = get_account()
    tx = {
        "from": account.address,
        "to": to_address,
        "value": w3.to_wei(value_eth, "ether"),
        "nonce": w3.eth.get_transaction_count(account.address),
        "gas": 21000,
        "gasPrice": w3.eth.gas_price,
        "chainId": CHAIN_ID,
    }
    signed_tx = account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    return w3.to_hex(tx_hash)
```

`blockchain/interface.py` — the single entrypoint the API talks to:
```python
from blockchain.ethereum import wallet as eth_wallet
from blockchain.ethereum import transaction as eth_transaction

SUPPORTED_CHAINS = {"ethereum"}  # add "polygon", "solana" as built

def send_payment(chain: str, to_address: str, value: float):
    if chain == "ethereum":
        return eth_transaction.send_transaction(to_address, value)
    raise ValueError(f"Unsupported chain: {chain}")

def get_balance(chain: str, address: str = None):
    if chain == "ethereum":
        return eth_wallet.get_balance(address)
    raise ValueError(f"Unsupported chain: {chain}")
```

### 9.4 — API endpoint

`routes/invoice.py`:
```python
from flask import Blueprint, request, jsonify
from blockchain.interface import send_payment

invoice_bp = Blueprint("invoice", __name__)

@invoice_bp.route("/invoice", methods=["POST"])
def create_invoice():
    data = request.get_json()
    to_address = data.get("to_address")
    amount = data.get("amount")
    chain = data.get("chain", "ethereum")

    if not to_address or amount is None:
        return jsonify({"error": "to_address and amount are required"}), 400

    try:
        tx_hash = send_payment(chain, to_address, amount)
        return jsonify({"status": "sent", "tx_hash": tx_hash})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "transaction failed", "details": str(e)}), 500
```

### 9.5 — Live proof of on-chain settlement

```bash
curl -X POST http://localhost:5000/invoice \
  -H "Content-Type: application/json" \
  -d '{"to_address": "0x822Afd3C5864e39C383e480871952705aBf15EE5", "amount": 0.0001}'

# → {"status":"sent","tx_hash":"0x1962c53b6a6d97a195fd67dd0a8fe94033b2b5b7e54821fe31bad6a77c86e989"}
```

Verified on Sepolia Etherscan:

| Field              | Value                                                                          |
| ------------------- | ------------------------------------------------------------------------------ |
| Status              | ✅ Success                                                                       |
| Block               | 11380376 (25 confirmations)                                                     |
| Value               | 0.0001 ETH                                                                       |
| Transaction Fee     | 0.0000230780 ETH                                                                 |
| Explorer            | `sepolia.etherscan.io/tx/0x1962c53b6a6d97a195fd67dd0a8fe94033b2b5b7e54821fe31bad6a77c86e989` |

This confirms the Flask API genuinely signs and broadcasts real transactions to a live public blockchain — not a mocked response.

---

## 🚀 Production Readiness

### ✅ Health Checks

Both liveness and readiness probes are configured in `deployment.yaml` (see Phase 6):

| Probe          | Purpose                                                                                            |
| --------------- | ---------------------------------------------------------------------------------------------------- |
| **Liveness**    | Kubernetes restarts the container if it crashes or becomes unresponsive — self-healing               |
| **Readiness**   | Kubernetes only sends traffic to a pod when the app is fully ready — prevents 502s during startup    |

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

| Tool             | Role                                                    |
| ----------------- | --------------------------------------------------------- |
| **Prometheus**    | Scrapes metrics from pods and Kubernetes API server        |
| **Grafana**       | Dashboards for real-time visualisation                      |
| **CloudWatch**    | AWS-native — EKS control plane logs, EC2 node metrics       |

**Key metrics tracked:**

- CPU and memory usage per pod
- Pod restart count (early warning for crashes)
- API latency (p50, p95, p99)
- HTTP error rate (4xx, 5xx)
- Replica count over time (shows HPA scaling events)
- **On-chain metrics** *(planned)* — transaction confirmation time, failed-transaction rate, gas price at broadcast time

Prometheus can be deployed to the cluster via Helm:
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack
```

> 💡 For a fintech system, monitoring is not optional — downtime means missed transactions and regulatory exposure. For a system that also settles on-chain, a stuck or underpriced transaction is an additional failure mode worth alerting on.

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

> **Planned addition:** unit tests for `blockchain/interface.py` using a mocked `web3.py` provider, so CI can validate transaction-building logic without needing live Sepolia RPC access or funded test wallets.

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

| Metric                            | Observed Value                                 |
| ----------------------------------- | ------------------------------------------------- |
| API response time                   | ~50–150ms (local Minikube test)                    |
| Pod startup time                    | ~5–10 seconds                                      |
| Docker build time                   | ~30–45 seconds                                     |
| EKS cluster creation (eksctl)       | ~20 minutes                                        |
| EKS cluster creation (Terraform)    | ~10 minutes (8m55s cluster + 1m48s nodegroup)      |
| GitHub Actions CI build             | 27–35 seconds                                      |
| Replica failover                    | Automatic via Kubernetes ReplicaSet                |
| Sepolia tx confirmation             | ~15–30 seconds (25 confirmations observed in ~2 min)|
| Sepolia gas cost (0.0001 ETH send)  | 0.0000230780 ETH (~21,000 gas)                     |

### 💰 Cost Analysis

| Resource            | Type         | Estimated Cost           |
| --------------------- | -------------- | --------------------------- |
| EKS control plane     | Managed       | ~$0.10/hr (~$73/month)       |
| EC2 worker nodes      | t3.small × 1  | ~$15/month                   |
| EC2 worker nodes      | t3.small × 2  | ~$30/month                   |
| AWS Load Balancer     | ELB           | ~$18/month                   |
| ECR storage           | Per GB        | ~$0.10/GB/month              |
| Sepolia gas           | Testnet       | Free (faucet-funded, no real value) |
| **Total (1 node)**    |               | **~$106/month**              |
| **Total (2 nodes)**   |               | **~$121/month**              |

**Cost optimisations already applied in this project:**

- ✅ Reduced nodes from `t3.medium × 2` → `t3.small × 1` (proven in implementation)
- ✅ Used Minikube for local testing — avoided cloud cluster costs during development
- ✅ Deleted EKS cluster after testing (`eksctl delete cluster`) — no idle charges
- ✅ Used `t3.small` instead of `t3.medium` — ~50% node cost reduction
- ✅ Developed and tested blockchain settlement entirely on **testnet** — zero real financial risk during development

> 💡 Always delete EKS clusters when not in use — the control plane charges $0.10/hr regardless of workload.

---

## 🔐 Security Considerations

### IAM & Credentials

- ✅ **No hardcoded credentials** — all AWS keys stored as GitHub repository secrets (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`)
- ✅ **IAM-based ECR access** — EKS node IAM role grants ECR pull permission; no Docker credentials needed in pod specs
- ✅ **Principle of least privilege** — IAM user `dd-user` has only the permissions required for EKS and ECR operations
- ✅ **OIDC provider** — created by Terraform for pod-level IAM roles (IRSA), enabling fine-grained per-pod AWS access

### Blockchain Key Management

- ✅ **`WALLET_PRIVATE_KEY` is never hardcoded** — loaded exclusively via `python-dotenv` from a local `.env` file
- ✅ **`.env` is git-ignored** and confirmed absent from both the working tree and commit history before every push
- ✅ **Testnet-only wallet** — the private key in use controls a Sepolia-only wallet with no real-world value, isolated from any mainnet wallet
- ⚠️ **Planned for EKS deployment:** `WALLET_PRIVATE_KEY` must move to a Kubernetes `Secret` (or AWS Secrets Manager, mounted via CSI driver) before this service runs in the cluster — it currently only exists in local `.env`, which does not survive into the container image or pod spec unless explicitly wired, and should stay that way

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
# For wallet keys specifically: Kubernetes Secret, never a ConfigMap
```

### Recommended Additions for Full Production

- [ ] Enable ECR image scanning on push (`scanOnPush: true`)
- [ ] Add Kubernetes Network Policies to restrict pod-to-pod traffic
- [ ] Enable EKS CloudWatch logging for audit trail
- [ ] Use AWS Secrets Manager for app credentials (not env vars)
- [ ] Add Trivy or Snyk to CI pipeline for container vulnerability scanning
- [ ] Move `WALLET_PRIVATE_KEY` from `.env` to a Kubernetes Secret before any cluster deployment of the blockchain-enabled API
- [ ] Add rate limiting / request validation on `POST /invoice` before any public exposure — currently accepts any `to_address` and `amount` without spend limits

---

## 📦 Scalability & Reliability Design

### Scalability

| Layer                | How It Scales                                                            |
| ---------------------- | ---------------------------------------------------------------------------- |
| **Application**        | Stateless Flask API — any number of replicas can run simultaneously          |
| **Pods**                | HPA scales 2→5 replicas automatically based on CPU utilisation                |
| **Nodes**               | eksctl/Terraform node groups can be scaled by changing `--nodes` count       |
| **Load balancing**      | AWS ELB distributes traffic across all healthy pod replicas                  |
| **Blockchain layer**    | `blockchain/interface.py` supports adding new chains (Polygon, Solana) without changing route code |

### Reliability

| Mechanism               | What It Provides                                                |
| -------------------------- | -------------------------------------------------------------------- |
| **2 replicas minimum**     | If one pod crashes, the other continues serving traffic               |
| **Liveness probe**         | Kubernetes restarts unresponsive containers automatically             |
| **Readiness probe**        | No traffic sent to pods that are not yet ready                        |
| **ReplicaSet**             | Automatically recreates failed pods to maintain desired count         |
| **Multi-AZ nodes**         | Node failure in one AZ doesn't take down all pods                     |
| **On-chain error handling**| `/invoice` catches both invalid-input (`ValueError` → 400) and transaction failures (insufficient gas, RPC errors → 500 with detail) rather than crashing unhandled |

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

### 🔴 `pip install` fails with "externally-managed-environment"
```bash
# Cause: system Python on Ubuntu 24.04 blocks global pip installs (PEP 668)
# Fix: always install into the project venv, never system-wide
cd api-service
source venv/bin/activate
pip install web3 python-dotenv
```

### 🔴 `ModuleNotFoundError: No module named 'blockchain'`
```bash
# Cause: running a script from api-service/ or another subdirectory,
# where blockchain/ and config.py (project-root level) aren't on the path
cd ~/fintech-platform    # run from project root
source api-service/venv/bin/activate
python3 -c "from blockchain.ethereum.wallet import get_account; print(get_account().address)"
```

### 🔴 `/invoice` returns 500 Internal Server Error
```bash
# Cause: usually insufficient Sepolia ETH balance to cover gas
python3 -c "from blockchain.ethereum.wallet import get_balance; print(get_balance())"
# If 0 → fund the wallet address from a Sepolia faucet, then retry
```

---

## Real Errors & Fixes

| #  | Error                                               | Root Cause                        | Fix                                            |
| --- | ----------------------------------------------------- | ------------------------------------ | ---------------------------------------------- |
| 1  | `E: Package 'awscli' has no installation candidate`  | Not in Ubuntu 24.04 noble repos      | Manual install from `awscli.amazonaws.com`      |
| 2  | `eksctl: command not found`                          | Not pre-installed                    | Downloaded from GitHub releases                 |
| 3  | `ParamValidation: --repository-name required`        | Typo `--repositiry-name`             | Corrected spelling                              |
| 4  | `AlreadyExistsException: Stack already exists`       | Leftover CloudFormation stack        | `eksctl delete cluster`                         |
| 5  | `kubectl not found, v1.10.0 or newer required`       | eksctl does not install kubectl      | Installed kubectl v1.35.2 manually               |
| 6  | `yaml: line 17: did not find expected '-'`           | YAML indentation error               | Fixed in nano, applied third attempt             |
| 7  | `dial tcp 127.0.0.1:8080: connection refused`        | Stale kubeconfig                     | `aws eks update-kubeconfig`                      |
| 8  | `Found invalid choice 'list'`                        | `aws eks list clusters` (space)      | `aws eks list-clusters` (hyphen)                 |
| 9  | `only one argument is allowed as a name`             | Nested eksctl command                | Separated into clean command                     |
| 10 | `remote rejected — missing workflow scope`           | PAT missing workflow permission      | Regenerated PAT with workflow scope              |
| 11 | `aws-secret-access-key must be provided`             | Only access key ID in secrets        | Added `AWS_SECRET_ACCESS_KEY`                    |
| 12 | `error: the path "k8s/" does not exist`              | Wrong path in deploy.yml             | Updated to `api-service/k8s/`                    |
| 13 | `Error: Username and password required`              | Docker Hub secrets missing           | Added `DOCKER_USERNAME` + `DOCKER_PASSWORD`      |
| 14 | `Command 'terraform' not found`                      | Not installed                        | `sudo snap install terraform`                    |
| 15 | Image not found in ECR                               | Wrong account ID or region           | Verified ECR repo URI in AWS Console             |
| 16 | `error: externally-managed-environment` (pip)        | PEP 668 blocks system-wide installs  | Installed into `api-service/venv` instead         |
| 17 | `Invalid username or token` (git push)               | GitHub dropped password auth         | Switched to Personal Access Token (PAT)           |
| 18 | `ModuleNotFoundError: No module named 'blockchain'`  | Ran script from wrong directory      | Run from project root with venv active            |
| 19 | `/invoice` → 500 Internal Server Error               | Wallet had 0 Sepolia ETH for gas     | Funded wallet via Sepolia faucet, retried         |
| 20 | Heredoc (`cat << EOF`) silently failed on paste      | Terminal mangled multi-line paste, Ctrl+C killed it | Switched to `nano` for all multi-line file creation |

---

## Live Proof

| Environment            | URL / Reference                                                                          | Result                     |
| ------------------------ | -------------------------------------------------------------------------------------------- | ---------------------------- |
| Docker local              | `localhost:5000`                                                                              | ✅ `fintech API is running`   |
| Minikube tunnel           | `127.0.0.1:45233`                                                                             | ✅ `fintech API is running`   |
| EKS LoadBalancer          | AWS ELB URL                                                                                    | ✅ `fintech API is running`   |
| GitHub Actions CI #1      | Actions tab                                                                                    | ✅ Success — 32s              |
| GitHub Actions CI #4      | Actions tab                                                                                    | ✅ Success — 41s              |
| **Sepolia settlement**    | `sepolia.etherscan.io/tx/0x1962c53b6a6d97a195fd67dd0a8fe94033b2b5b7e54821fe31bad6a77c86e989` | ✅ Success — block 11380376   |

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
web3.py:         7.16.0
eth-account:     0.13.7
python-dotenv:   1.2.2
Terraform:       via snap (19 EKS resources)
EKS (eksctl):    Kubernetes 1.34 — node v1.34.4-eks-f69f56f
EKS (Terraform): Kubernetes 1.29 — node v1.29.15-eks-ecaa3a6
Blockchain:      Ethereum Sepolia (chain ID 11155111) via Alchemy RPC
```

---

## 🗺️ Roadmap

- [ ] `GET /transaction/status` — check confirmation status of a settled invoice by tx hash
- [ ] `GET /balance` — expose wallet balance via API rather than the Python shell
- [ ] Consolidate duplicate `config.py` files (root + `api-service/`) into one shared module
- [ ] Add `blockchain/polygon/` following the same pattern as `blockchain/ethereum/`, wired through `interface.py`
- [ ] Wire `WALLET_PRIVATE_KEY` and `SEPOLIA_RPC_URL` into a Kubernetes Secret for cluster deployment
- [ ] Unit tests for `blockchain/interface.py` with a mocked web3 provider
- [ ] Request validation and spend limits on `POST /invoice`
- [ ] Prometheus metrics for on-chain transaction success rate and confirmation latency

---

## About

DEPLOYING CONTAINERIZED FINTECH API TO AWS USING KUBERNETES, WITH REAL ETHEREUM SEPOLIA SETTLEMENT

### Topics
`python` `docker` `kubernetes` `aws` `devops` `ci-cd` `fintech` `web3` `ethereum` `blockchain`
