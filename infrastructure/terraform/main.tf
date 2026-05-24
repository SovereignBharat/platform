terraform {
  required_version = ">= 1.6.0"
}

provider "kubernetes" {}

resource "kubernetes_namespace" "sovereignbharat" {
  metadata {
    name = "sovereignbharat"
  }
}
