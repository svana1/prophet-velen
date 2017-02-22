output "vpc_id" {
  value = "${aws_vpc.default.id}"
}

output "subnet_admin_id" {
  value = "${aws_subnet.public_subnet.0.id}"
}

output "subnet_public_ids" {
  value = "${join(",", aws_subnet.public_subnet.*.id)}"
}

output "subnet_private_ids" {
  value = "${join(",",aws_subnet.private_subnet.*.id)}"
}

output "route_table_private_zone_ids" {
  value = "${join(",", aws_route_table.private_zone.*.id)}"
}

output "route_table_public_id" {
  value = "${aws_route_table.public.id}"
}
