resource "aws_vpc" "default" {
  cidr_block = "${var.vpc_cidr}"
  enable_dns_hostnames = true
  tags {
    Name = "${var.vpc_name}"
    "environment" = "${var.environment}"
    "service" = "${var.servicename}"
  }
}

resource "aws_subnet" "public_subnet" {
  count = "${length(split(",", var.public_cidrs))}"
  vpc_id = "${aws_vpc.default.id}"
  cidr_block = "${element(split(",", var.public_cidrs), count.index)}"
  availability_zone = "${var.aws_region}${element(split(",",var.zones), count.index)}"
  tags {
    Name = "Public Subnet ${count.index + 1}"
    "environment" = "${var.environment}"
    "service" = "${var.servicename}"
  }
}

resource "aws_subnet" "private_subnet" {
  count = "${length(split(",", var.private_cidrs))}"
  vpc_id = "${aws_vpc.default.id}"
  cidr_block = "${element(split(",", var.private_cidrs), count.index)}"
  availability_zone = "${var.aws_region}${element(split(",",var.zones), count.index)}"
  tags {
    Name = "Private Subnet ${count.index + 1}"
    "environment" = "${var.environment}"
    "service" = "${var.servicename}"
  }
}

resource "aws_internet_gateway" "default" {
  vpc_id = "${aws_vpc.default.id}"
  tags {
    Name = "Gateway"
    "environment" = "${var.environment}"
    "service" = "${var.servicename}"
  }
}

resource "aws_route_table" "public" {
  vpc_id = "${aws_vpc.default.id}"
  tags {
    Name = "Public"
    "environment" = "${var.environment}"
    "service" = "${var.servicename}"
  }
}

resource "aws_route" "public" {
  route_table_id = "${aws_route_table.public.id}"
  destination_cidr_block = "0.0.0.0/0"
  gateway_id = "${aws_internet_gateway.default.id}"
  depends_on = ["aws_route_table.public"]
}

resource "aws_eip" "nat" {
  count = "${length(split(",", var.zones))}"
  vpc = true
}

resource "aws_nat_gateway" "private_subnet_gw" {
  count = "${length(split(",", var.zones))}"
  subnet_id = "${element(aws_subnet.public_subnet.*.id, count.index)}"
  allocation_id = "${element(aws_eip.nat.*.id, count.index)}"
  depends_on = ["aws_internet_gateway.default"]
}

resource "aws_route_table" "private_zone" {
  vpc_id = "${aws_vpc.default.id}"
  count = "${length(split(",", var.zones))}"
  tags {
    Name = "Private"
    "environment" = "${var.environment}"
    "service" = "${var.servicename}"
  }
}

resource "aws_route" "private_zone" {
  count = "${length(split(",", var.zones))}"
  route_table_id = "${element(aws_route_table.private_zone.*.id, count.index)}"
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id = "${element(aws_nat_gateway.private_subnet_gw.*.id, count.index)}"
}

resource "aws_route_table_association" "public_subnet" {
  count = "${length(split(",", var.public_cidrs))}"
  subnet_id = "${element(aws_subnet.public_subnet.*.id, count.index)}"
  route_table_id = "${aws_route_table.public.id}"
}

resource "aws_route_table_association" "private_subnet" {
  count = "${length(split(",", var.private_cidrs))}"
  subnet_id = "${element(aws_subnet.private_subnet.*.id, count.index)}"
  route_table_id = "${element(aws_route_table.private_zone.*.id, count.index)}"
}

resource "aws_vpc_endpoint" "private-s3" {
  vpc_id = "${aws_vpc.default.id}"
  service_name = "com.amazonaws.${var.aws_region}.s3"
  route_table_ids = ["${concat(split(",", aws_route_table.public.id), aws_route_table.private_zone.*.id)}"]
}