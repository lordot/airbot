provider "kubernetes" {
  host = data.aws_eks_cluster.my-eks-cluster.endpoint
  token = data.aws_eks_cluster_auth.my-eks-cluster-auth.token
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.my-eks-cluster.certificate_authority[0].data)
}

data "aws_eks_cluster" "my-eks-cluster" {
  name = module.eks.cluster_name
}

data "aws_eks_cluster_auth" "my-eks-cluster-auth" {
  name = module.eks.cluster_name
}

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "19.16.0"

  cluster_name = var.cluster_name
  cluster_version = "1.28"

  vpc_id = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  eks_managed_node_groups = {
    blue = {
      min_size = 1
      max_size = 2
      desired_size = 1

      instance_types = ["t3.small"]
      capacity_type  = "SPOT"
    }
    green = {
      min_size = 1
      max_size = 2
      desired_size = 1

      instance_types = ["t3.medium"]
      capacity_type  = "SPOT"
    }
  }

  tags = {
    Environment = "dev"
    Terraform   = "true"
  }
}