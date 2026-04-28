# 🏦 FINTECH-CLOUD-EKS — Containerised Fintech API on AWS Kubernetes

> A complete end-to-end DevOps project: Python Flask fintech API containerised with Docker,
> infrastructure provisioned via both **eksctl** and **Terraform**, image stored in Amazon ECR,
> deployed to AWS EKS via Kubernetes, tested locally on Minikube, and automated through
> GitHub Actions CI/CD — proven across **53 real terminal + browser screenshots**.

![AWS](https://img.shields.io/badge/AWS-EKS-FF9900?style=flat-square&logo=amazonaws)
![Kubernetes](https://img.shields.io/badge/Kubernetes-1.34%2F1.35-326CE5?style=flat-square&logo=kubernetes)
![Docker](https://img.shields.io/badge/Docker-python%3A3.11-2496ED?style=flat-square&logo=docker)
![Terraform](https://img.shields.io/badge/Terraform-IaC-7B42BC?style=flat-square&logo=terraform)
![Python](https://img.shields.io/badge/Python-Flask-3776AB?style=flat-square&logo=python)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?style=flat-square&logo=githubactions)

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Tech Stack & Why Each Tool](#tech-stack--why-each-tool)
- [Repository Structure](#repository-structure)
- [Phase 1 — System Setup & AWS CLI](#phase-1--system-setup--aws-cli)
- [Phase 2 — Application & Docker Build](#phase-2--application--docker-build)
- [Phase 3 — Amazon ECR](#phase-3--amazon-ecr)
- [Phase 4 — EKS Cluster via eksctl](#phase-4--eks-cluster-via-eksctl)
- [Phase 5 — EKS Cluster via Terraform](#phase-5--eks-cluster-via-terraform)
- [Phase 6 — Kubernetes Deployment](#phase-6--kubernetes-deployment)
- [Phase 7 — GitHub Actions CI/CD](#phase-7--github-actions-cicd)
- [Phase 8 — Minikube Local Testing](#phase-8--minikube-local-testing)
- [Real Errors & Fixes (from screenshots)](#real-errors--fixes-from-screenshots)
- [Live Proof — Application Running](#live-proof--application-running)
- [Versions Confirmed](#versions-confirmed)

---

## Project Overview

This project deploys a Python Flask API to AWS EKS end-to-end, from raw system setup
on Ubuntu 24.04 WSL2 all the way to a live Kubernetes pod serving traffic.

**Two complete infrastructure paths were proven:**
- **eksctl path** → cluster name: `reluna-cluster` (Kubernetes 1.34)
- **Terraform path** → cluster name: `fintech-eks` (Kubernetes 1.29, 19 resources)

| Detail | Value |
|---|---|
| AWS Account | `005905649522` |
| Region | `ap-south-1` (Mumbai) |
| OS | Ubuntu 24.04.4 LTS on WSL2 (kernel `6.6.87.2-microsoft-standard-WSL2`) |
| IAM User | `dd-user` |
| ECR Repo | `005905649522.dkr.ecr.ap-south-1.amazonaws.com/fintech-api` |
| GitHub Repo | `rey26341-sudo/FINTECH-CLOUD-EKS` |

---

## Tech Stack & Why Each Tool

| Tool | Version (Proven) | Why It Was Used |
|---|---|---|
| **Ubuntu 24.04 LTS (WSL2)** | kernel 6.6.87.2 | Linux environment on Windows — WSL2 gives native Docker networking and kubectl compatibility |
| **Python + Flask** | 3.11 / Flask 3.1.3 | Lightweight API — minimal boilerplate, single `pip install flask`, easy to containerise |
| **Docker** | 29.2.1 | Packages the app and all dependencies into one portable image — the single unit of deployment across local, ECR, and EKS |
| **Amazon ECR** | — | AWS-native private registry — EKS nodes pull images over the internal network using IAM roles; no Docker credentials needed in pod specs |
| **AWS CLI** | v2.34.11 | Primary interface to AWS — configure credentials, create ECR repos, update kubeconfig, describe VPCs/subnets |
| **eksctl** | 0.224.0 | Fastest CLI to spin up a production EKS cluster — auto-creates VPC, subnets, IAM roles, CloudFormation stacks, and installs all addons |
| **Terraform** | via snap | IaC — reproducible, version-controlled cluster using `terraform-aws-eks` module; 19 resources created in one `apply` |
| **kubectl** | v1.35.2 | Standard Kubernetes CLI — applies manifests, inspects pods/nodes/services |
| **Minikube** | v1.38.1 | Local Kubernetes on Docker driver — validates manifests before cloud deployment |
| **GitHub Actions** | ci.yml + deploy.yml | Cloud CI/CD — every `git push` to `main` triggers build → push to registry → deploy to Kubernetes |
| **Claude Code** | 2.1.85 | AI coding assistant — installed on WSL2 during development |

---

## Repository Structure

```
FINTECH-CLOUD-EKS/
├── .github/
│   └── workflows/
│       ├── deploy.yml        # CD: Configure AWS → Login ECR → Build → Push → kubectl apply
│       └── ci.yml            # CI: Login Docker Hub → Build → Push to Docker Hub
├── api-service/
│   ├── k8s/
│   │   ├── deployment.yaml   # 2 replicas, fintech-app:latest, port 5000, resource limits
│   │   └── service.yaml      # NodePort (Minikube) / LoadBalancer (EKS)
│   ├── app.py                # Flask — returns "fintech API is running"
│   ├── requirements.txt      # flask
│   ├── Dockerfile            # FROM python:3.11, 6 build steps
│   └── README.md
├── infra/
│   ├── main.tf               # terraform-aws-eks module (cluster: fintech-eks)
│   ├── variables.tf
│   ├── outputs.tf
│   ├── terraform.tfstate
│   └── terraform.tfstate.backup
├── .gitignore
└── README.md
```

---

## Phase 1 — System Setup & AWS CLI

**Proof:** Screenshots 1–5 (March 18, 2026)

```bash
# Verify OS
uname -a
# Linux LAPTOP-A8LSS8GU 6.6.87.2-microsoft-standard-WSL2 #1 SMP x86_64 GNU/Linux

# System update
sudo apt update && sudo apt upgrade -y

# Base tools — all already at newest version on this machine
sudo apt install -y curl unzip git
# curl 8.5.0-2ubuntu10.8 | unzip 6.0 | git 2.43.0

# AWS CLI v2 — apt package not available in Ubuntu noble repos
sudo apt install -y awscli
# E: Package 'awscli' has no installation candidate  ← PROOF: had to install manually

curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
# 63.7 MB downloaded at 11.1 MB/s

unzip awscliv2.zip
sudo ./aws/install --update
aws --version
# aws-cli/2.34.11 Python/3.13.11 Linux/6.6.87.2-microsoft-standard-WSL2 exe/x86_64.ubuntu.24

# Configure credentials
aws configure
# AWS Access Key ID:     AKIAQCYABB5ZBHTFZBXA
# Default region name:  ap-south-1
# Default output format: json

# Confirm authentication before touching infrastructure
aws sts get-caller-identity
# {
#   "UserId":  "AIDAQCYABB5ZEHUT2I4TX",
#   "Account": "005905649522",
#   "Arn":     "arn:aws:iam::005905649522:user/dd-user"
# }
```

**Why `aws sts get-caller-identity` first?**
Confirms the right IAM user is active and credentials are valid before provisioning
any paid infrastructure. Catches wrong-account mistakes before they cost money.

---

## Phase 2 — Application & Docker Build

**Proof:** Screenshots 11–13, batch-2 screenshots 1 & 13 (March 18–22, 2026)

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

**Dockerfile (6 steps, python:3.11 base):**
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

# Build — pulled python:3.11 (sha256:ff461875d046...)
docker build -t fintech-api .
# Step 1/6: FROM python:3.11          ← base layer
# Step 4/6: RUN pip install           ← flask 3.1.3 + blinker, click,
#                                        itsdangerous, jinja2, markupsafe, werkzeug
# Successfully built 961d550ebb57
# Successfully tagged fintech-api:latest

# Run locally
docker run -d -p 5000:5000 fintech-api
# 8bc1f5fbc4bde055ca1052146d40760fa86238ce9b98dca8d144d67c6ed40111

docker ps
# CONTAINER ID  IMAGE        STATUS          PORTS
# 8bc1f5fbc4bd  fintech-api  Up 11 seconds   0.0.0.0:5000->5000/tcp
```

**Browser proof:** `localhost:5000` → **"fintech API is running"** ✅ (Screenshot 11)

**Why python:3.11?**
Stable LTS Python; Flask 3.x supports it natively. Official Docker base images
receive upstream security patches automatically.

**Why `host='0.0.0.0'`?**
Flask's default `127.0.0.1` only accepts connections from inside the container.
`0.0.0.0` allows Docker port mapping and Kubernetes liveness probes to reach it.

---

## Phase 3 — Amazon ECR

**Proof:** Batch-2 screenshots 1–2 (March 22, 2026)

```bash
# First attempt had a typo — caught immediately
aws ecr create-repository --repositiry-name fintech-api --region ap-south-1
# aws: [ERROR]: ParamValidation: the following arguments are required: --repository-name

# Correct command
aws ecr create-repository --repository-name fintech-api --region ap-south-1
# {
#   "repositoryArn":  "arn:aws:ecr:ap-south-1:005905649522:repository/fintech-api",
#   "registryId":     "005905649522",
#   "repositoryName": "fintech-api",
#   "repositoryUri":  "005905649522.dkr.ecr.ap-south-1.amazonaws.com/fintech-api",
#   "createdAt":      "2026-03-22T11:26:27.728000+00:00",
#   "encryptionType": "AES256"
# }

# Authenticate Docker to ECR
aws ecr get-login-password --region ap-south-1 \
  | docker login --username AWS --password-stdin \
    005905649522.dkr.ecr.ap-south-1.amazonaws.com
# Login Succeeded

# Tag and push
docker tag fintech-api:latest \
  005905649522.dkr.ecr.ap-south-1.amazonaws.com/fintech-api:latest

docker push 005905649522.dkr.ecr.ap-south-1.amazonaws.com/fintech-api:latest
# 2e01e049c9cd: Pushed
# 60cb62ce5e3a: Pushed  ... (11 layers total)
# latest: digest: sha256:81e08707c9477fde634966f3a19a57fcb1a9366a2383068d621c25a0c6eca8ea
#         size: 2631
```

**Why ECR over Docker Hub?**
ECR sits inside the same AWS region as EKS — nodes pull images over the internal
network with no egress cost and no rate limits. IAM roles on EC2 nodes grant pull
permissions; no Docker credentials are needed in pod specs or Kubernetes secrets.

---

## Phase 4 — EKS Cluster via eksctl

**Proof:** Screenshots 4–10, batch-2 screenshots 2–8 (March 18–23, 2026)

### Install eksctl

```bash
# First try — not installed
eksctl create cluster ...
# eksctl: command not found  ← PROOF screenshot 4

# Download and install
curl --silent --location \
  "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_Linux_amd64.tar.gz" \
  -o eksctl.tar.gz
tar -xzf eksctl.tar.gz
sudo mv eksctl /usr/local/bin/
sudo chmod +x /usr/local/bin/eksctl
eksctl version
# 0.224.0
```

### Create the cluster (final working command)

```bash
# Started with t3.medium / 2 nodes, switched to t3.small / 1 node (cost optimisation)
eksctl create cluster \
  --name reluna-cluster \
  --region ap-south-1 \
  --nodegroup-name standard-workers \
  --node-type t3.small \
  --nodes 1

# What eksctl did automatically (proven in screenshot logs):
# [i] using Kubernetes version 1.34
# [i] setting availability zones to [ap-south-1b ap-south-1c ap-south-1a]
# [i] subnets for ap-south-1b — public:192.168.0.0/19   private:192.168.96.0/19
# [i] subnets for ap-south-1c — public:192.168.32.0/19  private:192.168.128.0/19
# [i] subnets for ap-south-1a — public:192.168.64.0/19  private:192.168.160.0/19
# [i] nodegroup "standard-workers" will use AmazonLinux2023/1.34
# [i] building cluster stack "eksctl-reluna-cluster-cluster"
# [i] deploying stack "eksctl-reluna-cluster-cluster"
# [✔] created addon: vpc-cni
# [✔] created addon: kube-proxy
# [✔] created addon: coredns
# [✔] created addon: metrics-server
# [✔] saved kubeconfig as "/home/iswaryak/.kube/config"
# [✔] all EKS cluster resources for "reluna-cluster" have been created
# [✔] nodegroup "standard-workers" has 1 node(s)
# [✔] node "ip-192-168-0-230.ap-south-1.compute.internal" is ready
# [✔] EKS cluster "reluna-cluster" in "ap-south-1" region is ready
```

### Install kubectl (required separately — eksctl does NOT install it)

```bash
# Error proof: eksctl reported "kubectl not found, v1.10.0 or newer is required"
curl -LO "https://dl.k8s.io/release/$(curl -L -s \
  https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin
kubectl version --client
# Client Version: v1.35.2
# Kustomize Version: v5.7.1
```

### Connect and verify

```bash
aws eks update-kubeconfig --region ap-south-1 --name reluna-cluster
# Added new context arn:aws:eks:ap-south-1:005905649522:cluster/reluna-cluster

kubectl get nodes
# NAME                                          STATUS  VERSION
# ip-192-168-0-230.ap-south-1.compute.internal Ready   v1.34.4-eks-f69f56f

# Later added second node via nodegroup command
eksctl create nodegroup \
  --cluster reluna-cluster \
  --region ap-south-1 \
  --name standard-workers \
  --node-type t3.small \
  --nodes 1

kubectl get nodes
# ip-192-168-63-176.ap-south-1.compute.internal  Ready  v1.34.4-eks-f69f56f
# ip-192-168-76-120.ap-south-1.compute.internal  Ready  v1.34.4-eks-f69f56f
```

**Why eksctl?**
One command provisions the full production network topology — VPC, subnets,
route tables, NAT gateways, IAM roles for control plane and nodes, and the EKS
cluster itself — instead of writing 400+ lines of CloudFormation by hand.

---

## Phase 5 — EKS Cluster via Terraform

**Proof:** Batch-3 screenshots 4–8 (March 25 – April 3, 2026)

```bash
# Terraform not installed
terraform init
# Command 'terraform' not found, but can be installed with: sudo snap install terraform

sudo snap install terraform

# Created infra/ directory with three files
mkdir ~/fintech-platform/infra && cd infra
nano main.tf      # terraform-aws-eks module config
nano variables.tf # cluster_name = "fintech-eks", region, node_type
nano outputs.tf   # cluster_endpoint, kubeconfig

# Described existing VPCs and subnets before writing Terraform config
aws ec2 describe-vpcs --region ap-south-1 \
  --query "Vpcs[*].[VpcId,IsDefault]" --output table
# vpc-0d2cecacf70993137 (eksctl cluster VPC — tagged eksctl-reluna-cluster-cluster/VPC)
# vpc-00c69f43f962375cd (default VPC)

aws ec2 describe-subnets --region ap-south-1 \
  --filters "Name=vpc-id,Values=<default-vpc-id>" \
  --query "Subnets[*].[SubnetId,AvailabilityZone]" --output table
# Subnets in ap-south-1b, ap-south-1a, ap-south-1c confirmed

# Apply — proved working in screenshot
terraform apply
# module.eks.aws_eks_cluster.this[0]: Creating...
# module.eks.aws_eks_cluster.this[0]: Still creating... [08m00s elapsed]
# module.eks.aws_eks_cluster.this[0]: Creation complete after 8m55s [id=fintech-eks]
# module.eks.data.tls_certificate.this[0]: Read complete after 0s
# module.eks.aws_iam_openid_connect_provider.oidc_provider[0]: Creating...
# module.eks.aws_iam_openid_connect_provider.oidc_provider[0]: Creation complete after 2s
#   [id=arn:aws:iam::005905649522:oidc-provider/oidc.eks.ap-south-1.amazonaws.com/...]
# module.eks.module.eks_managed_node_group["default"].aws_eks_node_group.this[0]:
#   Creation complete after 1m48s [id=fintech-eks:default-20260401100015434360000005]
#
# Apply complete! Resources: 19 added, 0 changed, 0 destroyed.

# Grant IAM access to cluster (required for kubectl auth)
aws eks associate-access-policy \
  --cluster-name fintech-eks \
  --principal-arn arn:aws:iam::005905649522:user/dd-user \
  --policy-arn arn:aws:eks::aws:cluster-access-policy/AmazonAIOpsAssistantPolicy \
  --access-scope type=cluster \
  --region ap-south-1

# Update kubeconfig
aws eks update-kubeconfig --region ap-south-1 --name fintech-eks
# Updated context arn:aws:eks:ap-south-1:005905649522:cluster/fintech-eks

kubectl get nodes
# NAME                                           STATUS  AGE  VERSION
# ip-172-31-36-185.ap-south-1.compute.internal  Ready   2d   v1.29.15-eks-ecaa3a6
```

**Why Terraform after eksctl?**
eksctl is fast but imperative — hard to reproduce exactly. Terraform is declarative:
the same `main.tf` creates identical infrastructure in any account. The
`terraform-aws-eks` module also enables advanced features: OIDC provider for
pod-level IAM roles (IRSA), managed node groups with custom launch templates,
and optional CloudWatch logging — all in version-controlled code.

---

## Phase 6 — Kubernetes Deployment

**Proof:** Batch-2 screenshots 5–10, batch-3 screenshots 11–12, 18–20 (March 23 – April 16, 2026)

**api-service/k8s/deployment.yaml:**
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
        image: fintech-app:latest
        ports:
        - containerPort: 5000
        resources:
          limits:
            cpu: "500m"
            memory: "256Mi"
          requests:
            cpu: "250m"
            memory: "128Mi"
```

**api-service/k8s/service.yaml:**
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
  type: NodePort
```

```bash
# Apply manifests (after fixing YAML indentation errors — proof in screenshots)
kubectl apply -f k8s/deployment.yaml
# deployment.apps/fintech-deployment created

kubectl apply -f service.yaml
# service/fintech-service created

# Verify pods — 2 replicas running
kubectl get pods
# NAME                                  READY  STATUS   RESTARTS  AGE
# fintech-deployment-5d69fc4c5b-qjjs7   1/1    Running  0         65s
# fintech-deployment-5d69fc4c5b-tmx4j   1/1    Running  0         65s

# Verify service
kubectl get svc
# NAME             TYPE      CLUSTER-IP      PORT(S)
# fintech-service  NodePort  10.111.191.215  80:31677/TCP

# On EKS — expose via AWS LoadBalancer
kubectl expose deployment fintech-api \
  --type=LoadBalancer \
  --port=80 \
  --target-port=5000
# service/fintech-api exposed

kubectl get svc
# fintech-api  LoadBalancer  10.100.162.3
# EXTERNAL-IP: adf007ccbbb0d4d7ab4dc4991ce81a85-571019563.ap-south-1.elb.amazonaws.com
# PORT(S): 80:30667/TCP

# Full pod health check (proven in screenshot 51-52)
kubectl describe pod fintech-deployment-554fbf7549-bk4xm
# Name:       fintech-deployment-554fbf7549-bk4xm
# Node:       minikube/192.168.49.2
# Labels:     app=fintech
# Image:      fintech-app:latest
# Port:       5000/TCP
# State:      Running
# Started:    Thu, 16 Apr 2026 17:43:58 +0000
# Ready:      True
# Restart Count: 0
# Conditions:
#   PodReadyToStartContainers  True
#   Initialized                True
#   Ready                      True
#   ContainersReady            True
#   PodScheduled               True
# Events:
#   Scheduled → Pulled → Created → Started  (all Normal)
```

**Why 2 replicas?**
If one pod crashes or the node becomes unavailable, the second replica continues
serving traffic. The ReplicaSet controller automatically recreates failed pods.

**Why resource limits?**
Without `limits`, a misbehaving pod can consume all node CPU/memory and starve
other workloads. `requests` tell the scheduler how much to reserve; `limits` cap
maximum consumption.

---

## Phase 7 — GitHub Actions CI/CD

**Proof:** Batch-2 screenshots 11–14, batch-3 screenshots 9, 14–17 (March 24 – April 16, 2026)

### Repository push

```bash
cd ~/fintech-platform
git init
git add .
git commit -m "Initial commit - fintech EKS deployment project"
# 1339 files changed, 252349 insertions(+)
# create mode 100644 api-service/Dockerfile
# create mode 100644 api-service/README.md ...

git push
# First push rejected — PAT missing 'workflow' scope
# Fixed: regenerated PAT with workflow permission
# Second push: SUCCESS → eeb4ba8 pushed to main
```

### CI Pipeline (ci.yml) — proven working

```yaml
name: CI Pipeline
on:
  push:
    branches: [main]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      - name: Log in to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      - name: Build Docker Image
        run: docker build -t fintech-app ./api-service
      - name: Push to Docker Hub
        run: docker push <username>/fintech-app:latest
```

**Proof results (screenshots 47–48, 50):**
- CI Pipeline #1 — **Success** — commit `795e9e5` — **32s total** ✅
- Fix formatting in CI workflow for Docker push #4 — **Success** — **41s total** ✅

### CD Pipeline (deploy.yml)

```yaml
name: Deploy to EKS
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Configure AWS
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id:     ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ap-south-1

      - name: Login to ECR
        run: |
          aws ecr get-login-password --region ap-south-1 \
          | docker login --username AWS --password-stdin \
            005905649522.dkr.ecr.ap-south-1.amazonaws.com

      - name: Build Docker Image
        run: docker build -t fintech-api ./api-service

      - name: Tag Image
        run: docker tag fintech-api:latest \
          005905649522.dkr.ecr.ap-south-1.amazonaws.com/fintech-api:latest

      - name: Push Image
        run: docker push \
          005905649522.dkr.ecr.ap-south-1.amazonaws.com/fintech-api:latest

      - name: Update kubeconfig
        run: aws eks update-kubeconfig \
          --region ap-south-1 --name reluna-cluster

      - name: Deploy to Kubernetes
        run: kubectl apply -f api-service/k8s/
```

**GitHub Secrets configured (proven in screenshots 15–16):**

| Secret | Purpose |
|---|---|
| `AWS_ACCESS_KEY_ID` | AWS authentication for Configure AWS step |
| `AWS_SECRET_ACCESS_KEY` | AWS authentication (missing this caused first failure) |
| `DOCKER_USERNAME` | Docker Hub login for CI pipeline |
| `DOCKER_PASSWORD` | Docker Hub login for CI pipeline |

---

## Phase 8 — Minikube Local Testing

**Proof:** Batch-3 screenshots 10–13, 18–19 (April 15–16, 2026)

```bash
# minikube not installed
minikube start
# Command 'minikube' not found

# Download and install
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
# 128 MB downloaded at 4523k/s

sudo install minikube-linux-amd64 /usr/local/bin/minikube
minikube version
# minikube version: v1.38.1

# Start local cluster
minikube start
# 😄  minikube v1.38.1 on Ubuntu 24.04 (kvm/amd64)
# ✨  Automatically selected the docker driver
# ⚠️  Memory warning: 3072 MiB allocated of 3588 MiB total (WSL2 constraint)
# 🚀  Using Docker driver with root privileges
# 🔥  Creating docker container (CPUs=2, Memory=3072MB)
# 🐳  Preparing Kubernetes v1.35.1 on Docker 29.2.1
# 🔗  Configuring bridge CNI
# 🔎  Verifying Kubernetes components...
#     ▪ Using image gcr.io/k8s-minikube/storage-provisioner:v5
# 🌟  Enabled addons: storage-provisioner, default-storageclass
# 🏄  Done! kubectl is now configured to use "minikube" cluster

kubectl get nodes
# NAME      STATUS  ROLES          AGE   VERSION
# minikube  Ready   control-plane  31h   v1.35.1

# Build app image locally for Minikube
docker build -t fintech-app:latest ./api-service
# Successfully built 5fc39f184b65
# Successfully tagged fintech-app:latest

# Apply Kubernetes manifests
kubectl apply -f api-service/k8s/deployment.yaml
# deployment.apps/fintech-deployment created

kubectl apply -f api-service/k8s/service.yaml
# service/fintech-service created

# Check pods
kubectl get pods
# NAME                                   READY  STATUS   AGE
# fintech-deployment-5d69fc4c5b-qjjs7    1/1    Running  65s
# fintech-deployment-5d69fc4c5b-tmx4j    1/1    Running  65s

# Check service
kubectl get svc
# NAME             TYPE      CLUSTER-IP      PORT(S)       AGE
# fintech-service  NodePort  10.111.191.215  80:31677/TCP  80s

# Open tunnel to service
minikube service fintech-service
# |-----------|-----------------|-------------|--------------------------|
# | NAMESPACE |      NAME       | TARGET PORT |           URL            |
# |-----------|-----------------|-------------|--------------------------|
# | default   | fintech-service |          80 | http://192.168.49.2:31677|
# |-----------|-----------------|-------------|--------------------------|
# 🎉  Opening service default/fintech-service in default browser...
#     http://127.0.0.1:45233
```

**Browser proof:** `http://127.0.0.1:45233` → **"fintech API is running"** ✅ (Screenshot batch-3, image 13)

**Why Minikube?**
Testing Kubernetes manifests on a real cloud cluster costs money and takes 10–15
minutes per iteration. Minikube runs a complete Kubernetes cluster locally on
the Docker driver — manifest errors show up in seconds, for free.

---

## Real Errors & Fixes (from screenshots)

Every error below is proven in the screenshot trail.

| # | Error (exact message from screenshot) | Root Cause | Fix |
|---|---|---|---|
| 1 | `E: Package 'awscli' has no installation candidate` | awscli not in Ubuntu 24.04 noble repos | Manual install from `awscli.amazonaws.com` zip |
| 2 | `eksctl: command not found` | eksctl not pre-installed on Ubuntu | Downloaded tar.gz from GitHub releases, moved to `/usr/local/bin/` |
| 3 | `ParamValidation: --repository-name required` | Typo `--repositiry-name` in ECR command | Corrected spelling: `--repository-name` |
| 4 | `AlreadyExistsException: Stack [eksctl-reluna-cluster-cluster] already exists` | Previous failed eksctl run left a CloudFormation stack | `eksctl delete cluster --region ap-south-1 --name reluna-cluster` |
| 5 | `kubectl not found, v1.10.0 or newer is required` | eksctl does NOT install kubectl | Installed kubectl v1.35.2 manually from `dl.k8s.io` |
| 6 | `error parsing deployment.yaml: yaml: line 17: did not find expected '-'` | YAML indentation error in deployment manifest | Opened in `nano`, fixed indentation, applied third time |
| 7 | `couldn't get current server API group list: dial tcp 127.0.0.1:8080: connection refused` | kubeconfig pointed to wrong context after cluster was deleted and recreated | `aws eks update-kubeconfig --region ap-south-1 --name reluna-cluster` |
| 8 | `aws eks list clusters` → `Found invalid choice 'list'` | Subcommand uses hyphen not space | `aws eks list-clusters --region ap-south-1` |
| 9 | `only one argument is allowed to be used as a name` | Nested `eksctl create cluster` command pasted inside another | Separated into clean single-line command |
| 10 | `remote rejected: refusing to allow a PAT to create workflow without 'workflow' scope` | GitHub PAT did not include `workflow` permission | Regenerated PAT with `workflow` scope checked |
| 11 | GitHub Actions: `aws-secret-access-key must be provided` | Only `AWS_ACCESS_KEY_ID` was added to secrets; `AWS_SECRET_ACCESS_KEY` missing | Added `AWS_SECRET_ACCESS_KEY` in repo Settings → Secrets |
| 12 | GitHub Actions: `error: the path "k8s/" does not exist` | Workflow used `k8s/` but manifests live at `api-service/k8s/` | Updated `deploy.yml` path to `api-service/k8s/` |
| 13 | GitHub Actions CI: `Error: Username and password required` on Docker Hub login | Docker Hub secrets not set in the repo | Added `DOCKER_USERNAME` + `DOCKER_PASSWORD` as repository secrets |
| 14 | `Command 'terraform' not found` | Terraform not installed on WSL2 | `sudo snap install terraform` |
| 15 | `error: the server doesn't have a resource type "pods"` | Typo: `kubectl get pods` written as `kubectl get pods` with extra `s` → `kubectl get pods` | Used exact `kubectl get pods` |

---

## Live Proof — Application Running

| Environment | Access URL | Screenshot proof | Output |
|---|---|---|---|
| Docker local | `localhost:5000` | Screenshot 11 (batch 1) | `fintech API is running` ✅ |
| Minikube tunnel | `127.0.0.1:45233` | Screenshot 13 (batch 3) | `fintech API is running` ✅ |
| EKS LoadBalancer | `adf007ccbbb0d4d7ab4dc4991ce81a85-571019563.ap-south-1.elb.amazonaws.com` | Batch-2 screenshot 5 | `fintech API is running` ✅ |
| GitHub Actions CI | Actions tab → CI Pipeline #1 | Screenshots 14–15 (batch 3) | ✅ Success — 32s |
| GitHub Actions CI re-run | Fix formatting #4 | Screenshot 17 (batch 3) | ✅ Success — 41s |

---

## Versions Confirmed

```
Ubuntu:          24.04.4 LTS (WSL2 kernel 6.6.87.2-microsoft-standard-WSL2)
AWS CLI:         2.34.11 (Python/3.13.11)
eksctl:          0.224.0
kubectl:         v1.35.2 (Kustomize v5.7.1)
Minikube:        v1.38.1
Docker:          29.2.1
Python:          3.11
Flask:           3.1.3
Terraform:       via snap (provisioned 19 EKS resources)
Claude Code:     2.1.85
EKS (eksctl):    Kubernetes 1.34 — node v1.34.4-eks-f69f56f
EKS (Terraform): Kubernetes 1.29 — node v1.29.15-eks-ecaa3a6
```
