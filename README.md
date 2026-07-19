# Kubernetes Power Engine

 Kubernetes scaffold with production-oriented patterns.

## What this includes

- Flask sample service with Docker image support
- Kubernetes base manifests
- Kustomize environment overlays (dev, prod)
- Helm chart for reusable deployments
- Argo CD GitOps app-of-apps manifests
- Prometheus and Grafana monitoring resources
- Terraform AKS provisioning and app deployment
- GitHub Actions CI pipeline for validation and image build
- Deployment helper script for quick rollout

## Project layout

- app: application code and Dockerfile
- k8s/base: baseline Kubernetes resources
- k8s/overlays/dev: development-specific patches
- k8s/overlays/prod: production-specific patches
- helm/kubernetes-power-engine: Helm chart
- gitops/argocd: Argo CD project and applications
- monitoring/base: ServiceMonitor and PrometheusRule
- monitoring/dashboards: Grafana dashboard ConfigMap
- terraform/aks: AKS infrastructure and Helm release
- .github/workflows: CI workflow
- scripts: utility scripts

## Quick start

1. Build and run locally:

```bash
cd app
pip install -r requirements.txt
python main.py
```

2. Deploy with Kustomize:

```bash
kubectl apply -k k8s/overlays/dev
```

3. Deploy with PowerShell script:

```powershell
./scripts/deploy.ps1 -Environment dev
```

4. Deploy with Helm:

```bash
helm upgrade --install power-engine ./helm/kubernetes-power-engine
```

## GitOps with Argo CD

Install Argo CD first, then bootstrap the app-of-apps root:

```bash
kubectl apply -f gitops/argocd/bootstrap/root-application.yaml
```

Root app path:

- gitops/argocd

Managed child applications:

- power-engine-dev (k8s/overlays/dev)
- power-engine-prod (k8s/overlays/prod)

## Monitoring

Apply monitoring resources after installing kube-prometheus-stack:

```bash
kubectl apply -k monitoring/base
```

This adds:

- ServiceMonitor for scraping /metrics
- PrometheusRule alerts for availability and errors
- Grafana dashboard ConfigMap

## Terraform AKS deployment

```bash
cd terraform/aks
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform plan
terraform apply
```

## Endpoints

- /: app metadata response
- /healthz: liveness endpoint
- /readyz: readiness endpoint
- /metrics: Prometheus metrics endpoint
