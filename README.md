# Testing Repository

This repository is not for having a working job, it is actually only used to show basics in Python.

## Set Up firestore

You can access the firestore using base Url:

```shell
https://console.firebase.google.com/u/1/project/testing-repository-e403c/settings/general 
```
![Firestore](/images/firestore.PNG)
Generate a private key and put the file in the ./config/ folder.  
And Set the environment variable for the service account key in the ./src/firestore.py file using the generated file name.

## Installation

Ensure you have installed docker in your machine.

## How to run

Create a docker Network to ensure that redis and flask app containers can communicate.

```shell
docker network create my_network
```
Pull a redis image and run it.

```shell
docker pull redis
docker run --name redis --network my_network -p 6379:6379 -d redis
```
Build the Dockerfile and run the image of the flask application

```shell
docker build -t flask-app .
docker run --name flask-app --network my_network -p 8888:8888 flask-app
```
![Graph1](/images/graph1.png)

# Analysis

- Using a file to store users is very limiting, since if many users access the file it might end up corrupting it. Aditionnaly reading and writing to a file isn't very scalable for thousands of users. So it is recomended to use a database for example "Amazon DynamoDB" but since I don't have an AWS account I will use Firestore which is free.
- To Optimize the performance using ElastiCache to store frequently requested data is recommended. This reduces the number of database queries and improves execution speed. Since I don't have an AWS account I will use redis to implement caching. We will run a docker image of redis and make it communicate with our flask application.
- To guarantee that the application will be easily portable and run smoothly we will dockerize it. Then we will run the image using AWS Fargate that automatically provisions and scales the compute capacity required for the application. It can also automatically replace failed containers, ensuring high availability.
- To define and provision this AWS infrastructure we use Terraform or AWS CloudFormation.
- We can also use AWS CodePipeline to automate builds, tests, and deployments. Specifically, we can integrate it with GitHub to trigger a pipeline on every push, build a Docker image based on the newly pushed code, and then deploy it to AWS Fargate to replace the old application.
- Finally we can use AWS CloudWatch to monitore the application by adding alarms for error rates or latency spikes.

![Graph2](/images/graph2.png)