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
- Cluster (node) autoscaling via AKS's cluster autoscaler
- NGINX ingress controller behind an Azure LoadBalancer for external traffic
- Horizontal Pod Autoscaling (CPU + memory) and Vertical Pod Autoscaling (recommendation mode)
- GitHub Actions CI pipeline for validation, image build, and security scanning (Trivy, Terrascan) with OIDC Azure login
- Deployment helper script for quick rollout

## Autoscaling

- **Node autoscaling**: `terraform/aks` provisions the AKS default node pool with the cluster autoscaler enabled (`node_min_count` / `node_max_count` in `variables.tf`).
- **Horizontal Pod Autoscaling**: `k8s/base/hpa.yaml` and the Helm chart's `hpa.yaml` scale on both CPU and memory utilization.
- **Vertical Pod Autoscaling**: `k8s/base/vpa.yaml` and the Helm chart's `vpa.yaml` run in `updateMode: "Off"` (recommendations only) so they don't fight with the HPA over CPU/memory. The VPA controller itself is installed via the `helm_release.vpa` resource in `terraform/aks/main.tf` (Fairwinds VPA chart). On non-AKS clusters (e.g. local Docker Desktop), install the [Kubernetes VPA components](https://github.com/kubernetes/autoscaler/tree/master/vertical-pod-autoscaler) yourself before applying `vpa.yaml`, or drop it from the overlay.

## Traffic / load balancing

`terraform/aks` installs the `ingress-nginx` controller (`helm_release.ingress_nginx`) with `controller.service.type=LoadBalancer`, which provisions an Azure Standard Load Balancer to front external traffic to the `power-engine` Ingress.

## CI/CD security

The GitHub Actions workflow (`.github/workflows/ci-cd.yml`) runs:

- **Trivy** — config/IaC scan of the repo and a vulnerability scan of the built container image (fails on CRITICAL/HIGH findings).
- **Terrascan** — policy scans of the Terraform (`terraform/aks`) and Kubernetes (`k8s/base`) manifests.
- **OIDC Azure login** (`azure/login@v2`) for the `terraform-plan` job — no long-lived Azure credentials are stored in GitHub. Configure a federated credential on an Azure AD app registration for this repo, then set these repository secrets:
  - `AZURE_CLIENT_ID`
  - `AZURE_TENANT_ID`
  - `AZURE_SUBSCRIPTION_ID`

  The workflow only runs `terraform plan` (never `apply`) — provisioning real AKS infrastructure remains a manual step (see below).

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
