#data "aws_eks_cluster" "cluster" {
#  name = module.eks.cluster_id
#}
#
#data "aws_eks_cluster_auth" "cluster" {
#  name = module.eks.cluster_id
#}
#
#provider "kubernetes" {
#  host                   = data.aws_eks_cluster.cluster.endpoint
#  cluster_ca_certificate = base64decode(data.aws_eks_cluster.cluster.certificate_authority[0].data)
#  token                  = data.aws_eks_cluster_auth.cluster.token
#}

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "19.16.0"

  cluster_name = var.cluster_name
  cluster_version = "1.28"
  cluster_endpoint_public_access = true

  vpc_id = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  aws_auth_users = [
    {
      userarn  = "arn:aws:iam::340482041692:user/admin"
      username = "admin"
      groups   = ["system:masters"]
    }
  ]

  eks_managed_node_groups = {
#    blue = {
#      min_size = 1
#      max_size = 2
#      desired_size = 1
#
#      instance_types = ["t3.small"]
#      capacity_type  = "SPOT"
#    }
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