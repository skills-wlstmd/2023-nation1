ssh-add ./2023-nation1.pem
ssh ec2-user@<bastion_public_ip>

#!/bin/bash
yum install jq curl git -y --allowerasing

curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
aws --version

sudo yum install docker -y
sudo systemctl enable docker
sudo usermod -aG docker ec2-user
sudo usermod -aG docker root
sudo systemctl start docker
sudo chmod 666 /var/run/docker.sock

docker --version

sudo dnf update -y
sudo dnf install -y mariadb105

mysql -h <ENDPOINT> -P 3306 -u admin -p
source insert.sql

sed -i 's/#Port 22/Port 4272/' /etc/ssh/sshd_config
systemctl restart sshd

aws lambda add-permission \
  --function-name wsi-bastion-sg \
  --statement-id "AddConfigPermission" \
  --action lambda:InvokeFunction \
  --principal config.amazonaws.com
