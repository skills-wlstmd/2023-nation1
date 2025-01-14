output "public-a-id" {
  value = aws_subnet.public_subnet_a.id
}
output "public-b-id" {
  value = aws_subnet.public_subnet_b.id
}
output "private-a-id" {
  value = aws_subnet.private_subnet_a.id
}
output "private-b-id" {
  value = aws_subnet.private_subnet_b.id
}
output "protected-a-id" {
  value = aws_subnet.protected_subnet_a.id
}
output "protected-b-id" {
  value = aws_subnet.protected_subnet_b.id
}