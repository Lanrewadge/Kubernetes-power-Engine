# Terraform AKS Deployment

This Terraform stack provisions an AKS cluster and deploys the Power Engine app using the local Helm chart.

## Prerequisites

- Terraform >= 1.6
- Azure CLI authenticated (`az login`)
- Sufficient Azure subscription permissions

## Deploy

```bash
cd terraform/aks
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform plan
terraform apply
```

## Access cluster

Use the output command after apply:

```bash
az aks get-credentials --resource-group <rg> --name <cluster>
```

## Destroy

```bash
terraform destroy
```
