# - terraform variables related to aws access secrets and keys
variable "aws_access_key" {}
variable "aws_secret_key" {}
variable "aws_key_path" {}
variable "aws_key_name" {}

# - terraform variables for vpc
variable "aws_region" {
  description = "region for vpc"
  default = "us-west-1"
}

variable "vpc_nat_instance_type" {
  default = "m1.small"
}

variable "aws_azs" {
  description = "availability zones"
  default = []
}

variable "aws_nat_amis" {
  default = {
    us-west-1 = "ami-863b6391"
  }
}

variable "vpc_name" {
  default = "terraform-aws-vpc"
}

variable "vpc_cidr" {
  description = "cidr block for whole vpc, default to 65536 ips"
  default = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
  description = "cidr for public subnet, default to 256 ips, 10.0.0.0 to 10.0.0.255"
  default = "10.0.0.0/24"
}

variable "private_subnet_cidr" {
  description = "cidr for private subnet, default to 256 ips, 10.0.1.0 to 10.0.1.255"
  default = "10.0.1.0/24"
}