Project Overview
You work for the data science team at STEDI, a small startup focused on assessing balance for seniors. STEDI has an application that collects data from seniors during a [small exercise](https://youtu.be/XosjuXTCGeg). The user logs in and then selects the customer they are working with. Then the user starts a timer and clicks a button with each step the senior takes. When the senior has reached 30 steps, their test is finished. The data transmitted enables the application to monitor seniors’ balance risk.
![](https://video.udacity-data.com/topher/2020/September/5f68db8a_stedi-application/stedi-application.png)

## A New Product Feature
Your product manager has requested a graph that shows fall risk (will they fall and become injured?) for recent assessments. The development team has built a graph, which is ready to receive risk information from Kafka:
![](https://video.udacity-data.com/topher/2020/September/5f68db1d_stedi-graph/stedi-graph.png)

## The Data
The STEDI data science team has configured some real-time data sources using Kafka Connect. One of those data sources is Redis. When a customer is first assessed in the STEDI application, their record is added to a sorted set called Customer in Redis. Redis is configured as a Kafka source and whenever any data is saved to Redis (including Customer information), a payload is published to the Kafka topic called redis-server.

## The Challenge
The application development team has programmed certain business events to be published automatically to Kafka. Whenever a customer takes an assessment, their risk score is generated, as long as they have four or more completed assessments. The risk score is transmitted to a Kafka topic called `stedi-events` as a JSON object with this format:
```
{"customer":"Jason.Mitra@test.com","score":7.0,"riskDate":"2020-09-14T07:54:06.417Z"}
```
The application development team was not able to complete the feature as the graph is currently not receiving any data. Because the graph is currently not receiving any data, you need to generate a new payload in a Kafka topic and make it available to the STEDI application to consume.


# Project Setup Outside of Classroom
## Cloning the GitHub Repository
The first step to setting up your local workspace is to clone the GitHub repository:
```
git clone git@github.com:udacity/nd029-c2-apache-spark-and-spark-streaming-starter.git
```
Using Docker for your Project
You will need to use Docker to run the project on your own computer. You can find Docker for your operating system here: https://docs.docker.com/get-docker/

It is recommended that you configure Docker to allow it to use up to 2 cores and 6 GB of your host memory for use by the course workspace. If you are running other processes using Docker simultaneously with the workspace, you should take that into account also.

The docker-compose file at the root of the repository creates 9 separate containers:
* Redis
* Zookeeper (for Kafka)
* Kafka
* Banking Simulation
* Trucking Simulation
* STEDI (Application used in Final Project)
* Kafka Connect with Redis Source Connector
* Spark Master
* Spark Worker

It also mounts your repository folder to the Spark Master and Spark Worker containers as a volume `/home/workspace`, making your code changes instantly available within to the containers running Spark.

Let's get these containers started!
```
cd [repositoryfolder]
docker-compose up
```
You should see 9 containers when you run this command:
```
docker ps
```


# Project Instructions
## Submission Deliverables
As part of this project, you will submit the following:
* The `sparkpykafkajoin.py` Python script
* The `sparkpyeventskafkastreamtoconsole.py` Python script
* The `sparkpyrediskafkastreamtoconsole.py` Python script
* The log file from running the `sparkpykafkajoin.py` Python script in Spark: `/home/workspace/spark/logs/kafkajoin.log`
* The log file from running the `sparkpyeventskafkastreamtoconsole.py` Python script in Spark: `/home/workspace/spark/logs/eventstream.log`
* The log file from running the `sparkpyrediskafkastreamtoconsole.py` Python script in Spark: `/home/workspace/spark/logs/redisstream.log`
* The stedi-application sub-folder In the Python script `sparkpykafkajoin.py`, including the `/home/workspace/stedi-application/application.conf` file
* The log files from the Spark master and Spark worker: `/home/workspace/spark/logs`
* At least two screenshots of the working graph showing data flowing to the `/home/workspace/screenshots` folder


# Wireframe Solution
https://www.youtube.com/watch?v=4YSeVNr4ohU&t=8s