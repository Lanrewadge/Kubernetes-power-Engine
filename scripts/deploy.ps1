param(
    [ValidateSet("dev", "prod")]
    [string]$Environment = "dev"
)

$ErrorActionPreference = "Stop"

Write-Host "Deploying overlay: $Environment"
kubectl apply -k "k8s/overlays/$Environment"
Write-Host "Deployment submitted."
