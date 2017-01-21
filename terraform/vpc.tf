resource "aws_vpc" "default" {
  cidr_block = "${var.vpc_cidr}"
  enable_dns_hostnames = true
  tags {
    Name = "${var.vpc_name}"
  }
}

resource "aws_internet_gateway" "default" {
  vpc_id = "${aws_vpc.default.id}"
}

resource "aws_security_group" "nat" {
  name = "vpc_nat"

  ingress {
    from_port = 80
    to_port = 80
    protocol = "tcp"
    cidr_blocks = ["${var.private_subnet_cidr}}"]
  }

  ingress {
    from_port = 443
    to_port = 443
    protocol = "tcp"
    cidr_blocks = ["${var.private_subnet_cidr}}"]
  }

  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port = 80
    to_port = 80
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port = 443
    to_port = 443
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  vpc_id = "${aws_vpc.default.id}"
}

resource "aws_instance" "nat" {
  ami = "${lookup(var.aws_nat_amis, var.aws_region)}"
  key_name = "${var.aws_key_name}"
  instance_type = "${var.vpc_nat_instance_type}"
  vpc_security_group_ids = ["${aws_security_group.nat.id}}"]
  subnet_id = "${aws_subnet.public.id}"
  associate_public_ip_address = true
  source_dest_check = false
  tags {
    Name = "vpc nat"
  }
}

resource "aws_eip" "nat-eip" {
  instance = "${aws_instance.nat.id}"
  vpc = true
}

# - public subnet
resource "aws_subnet" "public" {
  vpc_id = "${aws_vpc.default.id}"
  cidr_block = "${var.public_subnet_cidr}"
  tags {
    Name = "public subnet"
  }
}

resource "aws_route_table" "public-routing-table" {
  vpc_id = "${aws_vpc.default.id}"
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = "${aws_internet_gateway.default.id}"
  }

  tags {
    Name = "public subnet"
  }
}

resource "aws_route_table_association" "public-route-table-association" {
  subnet_id = "${aws_subnet.public.id}"
  route_table_id = "${aws_route_table.public-routing-table.id}"
}

# - private subnet
resource "aws_subnet" "private" {
  vpc_id = "${aws_vpc.default.id}"
  cidr_block = "${var.private_subnet_cidr}"
  tags {
    Name = "private subnet"
  }
}

resource "aws_route_table" "private-routing-table" {
  vpc_id = "${aws_vpc.default.id}"
  route {
    cidr_block = "0.0.0.0/0"
    instance_id = "${aws_instance.nat.id}"
  }
  tags {
    Name = "private subnet"
  }
}

resource "aws_route_table_association" "private-route-table-association" {
  subnet_id = "${aws_subnet.private.id}"
  route_table_id = "${aws_route_table.private-routing-table.id}"
}