output "eks_host" {
  value = data.aws_eks_cluster.my-eks-cluster.endpoint
}