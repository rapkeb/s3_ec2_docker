# Flask User Registration App

A simple Flask application for user registration with an SQLite database and image serving from AWS S3. 
Dockerized for easy deployment on AWS ec2 instances.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)

## Introduction

This Flask application allows users to register by providing their username, email, and password. 
Upon successful registration, users are greeted on a welcome page that includes an image served from an AWS S3 bucket.

## Installation

### Prerequisites

- AWS account with permissions to create auto scaling groups, launch templates, target groups, and load balancers.
- Basic knowledge of AWS services.

### Steps

1. **Create a Launch Template:**

    - Create a launch template with the necessary configurations, including user data to run the setup script when the instance starts.
    - The scripts used for install git, docker and docker-compose.
    - In addition, to clone the application in the repo and build image and run as a container on the machine.

    User data script:
    ```bash
    #!/bin/bash
    sudo yum update -y
    sudo yum install git -y
    sudo yum install docker -y
    sudo service docker start
    sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose 
    git clone https://github.com/rapkeb/s3_ec2_docker.git
    cd ..
    cd ..
    cd s3_ec2_docker
    sudo docker-compose up -d
    ```

2. **Create an Auto Scaling Group:**

    - Set up an auto scaling group using the launch template created in step 1.
    - Configure scaling policies based on request load to the load balancer. When the number of requests exceeds a certain threshold, the auto scaling group automatically creates additional instances.
    - Implement a basic auto scaling setup with one initial machine and a maximum of two machines.

    Auto Scaling Configuration:
    - **Launch Configuration**: Utilize the launch template created in step 1.
    - **Scaling Policies**: Configure scaling policies to trigger based on the number of requests reaching the load balancer. For example, when the number of requests count exceeds a predefined threshold , scale out by adding another instance.
    - **Initial Capacity**: Start with one instance.
    - **Maximum Capacity**: Set the maximum number of instances to two to control costs and ensure scalability.


3. **Step 3: Create a Load Balancer:**
    
    - Create a load balancer to distribute traffic to instances in the auto scaling group.
    - Choose the appropriate load balancer type (Application Load Balancer) and put him as internet-facing.
    - Configure listeners and routing rules to forward incoming requests to the instances in the auto scaling group(port 80).
    - Ensure the load balancer is associated with the appropriate security groups, subnets and target groups.
     
4. **Step 4: Create Target Groups:**
    
    - Create target groups to group instances within the auto scaling group.
    - Define health checks to monitor the status of instances in the target group.
    - Associate the target group with the load balancer created in step 3.


## Usage

### User Registration

1. Access the application through the load balancer DNS name.
2. Fill out the registration form with your username, email, and password.
3. Submit the form to register.

### Accessing the Welcome Page

After registering, you will be redirected to a welcome page displaying your username and an image served from AWS S3.

Note: The image serving feature may not work with the current implementation of the app. To enable this feature, follow these steps:

1. Create a bucket in Amazon S3.
2. Upload an image to the S3 bucket.
3. Set the S3 bucket permissions to private.
4. Create a new IAM role for the EC2 instances created by the auto scaling group, allowing them access to the S3 bucket.
5. Update the Flask application code to fetch and serve the image from the S3 bucket.

These steps are necessary to enable the image serving functionality from AWS S3. Adjustments may be required based on your specific AWS setup and application requirements.
