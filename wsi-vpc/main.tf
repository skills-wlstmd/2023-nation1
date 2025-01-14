module "vpc" {
  source = "./modules"

  vpc_name = local.vpc.name
  vpc_cidr = local.vpc.cidr

  public_subnet_a_name = "wsi-public-a"
  public_subnet_a_cidr = "10.1.2.0/24"

  public_subnet_b_name = "wsi-public-b"
  public_subnet_b_cidr = "10.1.3.0/24"

  private_subnet_a_name =  "wsi-app-a"
  private_subnet_a_cidr = "10.1.0.0/24"

  private_subnet_b_name =  "wsi-app-b"
  private_subnet_b_cidr = "10.1.1.0/24"

  protected_subnet_a_name =  "wsi-data-a"
  protected_subnet_a_cidr = "10.1.4.0/24"

  protected_subnet_b_name =  "wsi-data-b"
  protected_subnet_b_cidr = "10.1.5.0/24"

  igw_name = "wsi-igw"

  nat_a_name = "wsi-natgw-a"
  nat_b_name = "wsi-natgw-b"

  public_rt_name = "wsi-public-rt"
  private_a_rt_name = "wsi-app-a-rt"
  private_b_rt_name = "wsi-app-b-rt"
  protected_rt_name = "wsi-data-rt"
}