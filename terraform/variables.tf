variable "aws_region" {
  default = "us-west-2"
}

variable "profile" {

}

variable "vpc_name" {
  default = "online-judge-dev"
}

variable "vpc_cidr" {
  default = "172.16.0.0/22"
}

variable "zones" {
  default = "a,b,c"
}

variable "public_cidrs" {
  default = "172.16.0.0/25,172.16.0.128/25,172.16.1.0/25"
}

variable "private_cidrs" {
  default = "172.16.1.128/25,172.16.2.0/25,172.16.2.128/25"
}

variable "servicename" {
  default="online-judge"
}

variable "environment" {
  default = "dev"
}

variable "image_id" {
  default="ami-af8b30cf"
}

variable "instance_type" {
  default="m3.medium"
}

variable "admin_key_name" {
  default="online-judge-dev"
}

variable "worker_pool_max_size" {
  default = "1"
}

variable "worker_pool_min_size" {
  default = "0"
}

variable "worker_pool_desired" {
  default = "1"
}

variable "elasticache_instance_type" {
  default = "cache.t2.small"
}