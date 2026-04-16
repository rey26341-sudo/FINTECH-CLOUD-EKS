# 🏦 Fintech Cloud EKS — Containerized Fintech API on AWS Kubernetes

![AWS](https://img.shields.io/badge/AWS-EKS-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

> **Production-grade deployment of a containerized Fintech REST API on AWS Elastic Kubernetes Service (EKS), with automated CI/CD using GitHub Actions.**

---

## 📌 Project Overview

This project demonstrates a full end-to-end cloud-native deployment pipeline for a **Fintech API** — from writing the service in Python, containerizing it with Docker, pushing it to a container registry, and deploying it to a managed **AWS EKS** cluster using Kubernetes manifests.

It reflects real-world DevOps practices used in the **financial technology** sector where reliability, scalability, and security are non-negotiable.

---

## 🏗️ Architecture

```
Developer Push
      │
      ▼
┌─────────────────────┐
│   GitHub Actions     │  ← CI/CD Pipeline (.github/workflows)
│  Build → Test → Push │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Amazon ECR         │  ← Container Registry
│  (Docker Image)      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   AWS EKS Cluster    │  ← Managed Kubernetes
│  ┌───────────────┐  │
│  │  Deployment   │  │  ← Kubernetes Deployment
│  │  (Pods x N)   │  │
│  └───────────────┘  │
│  ┌───────────────┐  │
│  │   Service     │  │  ← LoadBalancer / ClusterIP
│  └───────────────┘  │
└─────────────────────┘
           │
           ▼
    External Traffic
   (REST API Clients)
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **API Service** | Python (FastAPI / Flask) |
| **Containerization** | Docker |
| **Orchestration** | Kubernetes (AWS EKS) |
| **Cloud Provider** | Amazon Web Services (AWS) |
| **CI/CD** | GitHub Actions |
| **Container Registry** | Amazon ECR |
| **Infrastructure** | AWS VPC, IAM, EKS Node Groups |

---

## 📁 Project Structure

```
FINTECH-CLOUD-EKS/
│
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions CI/CD pipeline
│
├── api-service/
│   ├── app.py                  # Main Fintech API application
│   ├── requirements.txt        # Python dependencies
│   └── Dockerfile              # Container build instructions
│
└── .gitignore
```

---

## ⚙️ CI/CD Pipeline

The GitHub Actions pipeline automates the full deployment lifecycle:

```
1. Code Push to main branch
        ↓
2. Checkout & Setup Python environment
        ↓
3. Run Tests
        ↓
4. Docker Build & Tag image
        ↓
5. Push to Amazon ECR
        ↓
6. kubectl apply → Deploy to EKS
        ↓
7. Verify Rollout
```

---

## 🚀 Getting Started

### Prerequisites

- AWS CLI configured (`aws configure`)
- `kubectl` installed
- `eksctl` installed
- Docker installed
- Python 3.9+

### 1. Clone the Repository

```bash
git clone https://github.com/rey26341-sudo/FINTECH-CLOUD-EKS.git
cd FINTECH-CLOUD-EKS
```

### 2. Build the Docker Image Locally

```bash
cd api-service
docker build -t fintech-api .
docker run -p 8000:8000 fintech-api
```

### 3. Create EKS Cluster

```bash
eksctl create cluster \
  --name fintech-cluster \
  --region us-east-1 \
  --nodegroup-name standard-workers \
  --node-type t3.medium \
  --nodes 2
```

### 4. Configure kubectl

```bash
aws eks update-kubeconfig \
  --region us-east-1 \
  --name fintech-cluster
```

### 5. Deploy to EKS

```bash
kubectl apply -f k8s/
kubectl get pods
kubectl get services
```

---

## 🔐 Security Considerations

- IAM roles follow **least privilege principle** for EKS node groups
- Secrets managed via **AWS Secrets Manager** (not hardcoded)
- `.gitignore` excludes all credentials, `.env` files, and kubeconfig
- Container runs as **non-root user** inside Docker

---

## 📈 Key Learnings & Skills Demonstrated

- ✅ Containerizing a Python API with Docker
- ✅ Provisioning a managed Kubernetes cluster on AWS EKS
- ✅ Writing GitHub Actions workflows for automated CI/CD
- ✅ Pushing and pulling images from Amazon ECR
- ✅ Kubernetes Deployments, Services, and Pod management
- ✅ AWS IAM roles and policies for EKS
- ✅ Cloud-native architecture for Fintech use cases

---

## 👩‍💻 Author

**Rey** — DevOps & Cloud Engineer | Cybersecurity Enthusiast
- GitHub: [@rey26341-sudo](https://github.com/rey26341-sudo)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

> *Built as part of a DevOps & Multicloud Architecture portfolio — demonstrating real-world deployment pipelines for financial technology systems.*
