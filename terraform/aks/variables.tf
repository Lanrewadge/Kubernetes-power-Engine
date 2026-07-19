variable "location" {
  description = "Azure region for deployment"
  type        = string
  default     = "eastus"
}

variable "resource_group_name" {
  description = "Azure Resource Group name"
  type        = string
  default     = "rg-kubernetes-power-engine"
}

variable "cluster_name" {
  description = "AKS cluster name"
  type        = string
  default     = "aks-power-engine"
}

variable "dns_prefix" {
  description = "AKS DNS prefix"
  type        = string
  default     = "power-engine"
}

variable "node_min_count" {
  description = "Minimum number of AKS worker nodes (cluster autoscaler)"
  type        = number
  default     = 2
}

variable "node_max_count" {
  description = "Maximum number of AKS worker nodes (cluster autoscaler)"
  type        = number
  default     = 6
}

variable "node_vm_size" {
  description = "AKS worker node VM size"
  type        = string
  default     = "Standard_D2s_v5"
}

variable "kubernetes_version" {
  description = "AKS Kubernetes version"
  type        = string
  default     = "1.30"
}

variable "app_namespace" {
  description = "Namespace for app deployment"
  type        = string
  default     = "power-engine"
}

variable "image_repository" {
  description = "Container image repository for app"
  type        = string
  default     = "ghcr.io/lanrewadge/kubernetes-power-engine"
}

variable "image_tag" {
  description = "Container image tag"
  type        = string
  default     = "latest"
}
