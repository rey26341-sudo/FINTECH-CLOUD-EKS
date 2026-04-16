provider "aws" {
  region = "ap-south-1"
}

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"

  cluster_name    = "fintech-eks"
  cluster_version = "1.29"


  cluster_endpoint_private_access = true
  cluster_endpoint_public_access = true


  vpc_id = "vpc-0d2cecacf70993137"

  subnet_ids = [
    "subnet-0c421980d596a9c14",
    "subnet-00732fa404f448c55"
  ]

  eks_managed_node_groups = {
    default = {
      instance_types = ["t3.small"]
      desired_size   = 1
      min_size       = 1
      max_size       = 2
    }
  }
}



