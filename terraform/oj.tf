provider "aws" {
  "region" = "us-west-2"

  # - change this to your aws credential profile name
  "profile" = "bittiger"
}

resource "aws_ecs_cluster" "online-judge" {
  name = "${var.servicename}-${var.environment}"
}

module "ecs-vpc" {
  source = "./vpc"
  aws_region = "${var.aws_region}"
  vpc_name = "${var.vpc_name}"
  vpc_cidr = "${var.vpc_cidr}"
  zones = "${var.zones}"
  public_cidrs = "${var.public_cidrs}"
  private_cidrs = "${var.private_cidrs}"
  servicename = "${var.servicename}"
  environment = "${var.environment}"
}

resource "aws_security_group" "ecs_communication" {
  name = "aws-ecs"
  vpc_id = "${module.ecs-vpc.vpc_id}"
}

resource "aws_launch_configuration" "private-slave-config" {
  lifecycle {
    create_before_destroy = true
  }
  name_prefix = "online-judge-ecs-"
  image_id = "${var.image_id}"
  instance_type = "${var.instance_type}"
  key_name = "${var.admin_key_name}"
  security_groups = ["${aws_security_group.ecs_communication.id}"]
  associate_public_ip_address = false
  root_block_device {
    volume_size = 20
  }
}

resource "aws_autoscaling_group" "private-slave-asg" {
  name = "private-slave-ecs"
  launch_configuration = "${aws_launch_configuration.private-slave-config.id}"
  vpc_zone_identifier = ["${split(",", module.ecs-vpc.subnet_private_ids)}"]
  max_size = "${var.worker_pool_max_size}"
  min_size = "${var.worker_pool_min_size}"
  desired_capacity = "${var.worker_pool_desired}"
  health_check_type = "EC2"
  tag = {
    key = "Name"
    value = "${var.servicename}-${var.environment}"
    propagate_at_launch = true
  }
  tag = {
    key = "environment"
    value = "${var.environment}"
    propagate_at_launch = true
  }
  tag = {
    key = "servicename"
    value = "${var.servicename}"
    propagate_at_launch = true
  }
}