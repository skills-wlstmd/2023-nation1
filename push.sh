#!/bin/bash

cd /home/ec2-uesr/stress

git add .
git commit -m "$1"
git push origin main