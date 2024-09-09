# Project Overview
In this project, you will construct a streaming event pipeline around Apache Kafka and its ecosystem. Using public data from the [Chicago Transit Authority](https://www.transitchicago.com/data/) we will construct an event pipeline around Kafka that allows us to simulate and display the status of train lines in real time.

When the project is complete, you will be able to monitor a website to watch trains move from station to station. So a sample static view of the website page you create might look like this:
![](https://video.udacity-data.com/topher/2019/July/5d352372_screen-shot-2019-07-19-at-10.41.29-am/screen-shot-2019-07-19-at-10.41.29-am.png)


# Project Directions
## Starter Code and Data
Please find in the Resources tab, in the left sidebar of your classroom here, a zip file with all of the starter files and code referred to here in these directions. You can download those files and run your code locally, or you can use the Project Workspace we provide.

## Project Directions
The Chicago Transit Authority (CTA) has asked us to develop a dashboard displaying system status for its commuters. We have decided to use Kafka and ecosystem tools like REST Proxy and Kafka Connect to accomplish this task.

Our architecture will look like so:
![](https://video.udacity-data.com/topher/2019/July/5d320154_screen-shot-2019-07-19-at-10.43.38-am/screen-shot-2019-07-19-at-10.43.38-am.png)

## Directory Layout
The project consists of two main directories, `producers` and `consumers`.

The following directory layout indicates with a * the files that the student is responsible for modifying. Instructions for what is required are present as comments in each file.
![](https://video.udacity-data.com/topher/2019/July/5d3518ca_screen-shot-2019-07-21-at-7.00.34-pm/screen-shot-2019-07-21-at-7.00.34-pm.png)

## Running and Testing
### Running on Your Computer
__NOTE: You must allocate at least 4gb RAM to your Docker-Compose environment to run locally.__

To run the simulation, you must first start up the Kafka ecosystem on your machine utilizing Docker-Compose.
```
%> docker-compose up
```
Docker-Compose will take 3-5 minutes to start, depending on your hardware. Please be patient and wait for the Docker-Compose logs to slow down or stop before beginning the simulation.

Once Docker-Compose is ready, the following services will be available on your local machine:
![](https://video.udacity-data.com/topher/2019/September/5d715921_screen-shot-2019-09-05-at-11.50.46-am/screen-shot-2019-09-05-at-11.50.46-am.png)

Note that to access these services from your own machine, you will always use the Host URL column.

When configuring services that run within Docker-Compose, like Kafka Connect, you must use the `Docker URL`. When you configure the JDBC Source Kafka Connector, for example, you will want to use the value from the `Docker URL` column.

## Running the Simulation
There are two pieces to the simulation, the `producer` and `consumer`. As you develop each piece of the code, it is recommended that you only run one piece of the project at a time.

However, when you are ready to verify the end-to-end system prior to submission, it is critical that you open a terminal window for each piece and run them at the same time. If you do not run both the producer and consumer at the same time you will not be able to successfully complete the project.

__To run the `producer`__: \
If using your computer:
1. cd producers
2. virtualenv venv
3. . venv/bin/activate
4. pip install -r requirements.txt
5. python simulation.py
Once the simulation is running, you may hit `Ctrl+C` at any time to exit.

__To run the Faust Stream Processing Application__: \
If using your computer:
1. cd consumers
2. virtualenv venv
3. . venv/bin/activate
4. pip install -r requirements.txt
5. faust -A faust_stream worker -l info

__To run the KSQL Creation Script__: \
If using your computer:
1. cd consumers
2. virtualenv venv
3. . venv/bin/activate
4. pip install -r requirements.txt
5. python ksql.py

__To run the consumer: (NOTE: Do not run the consumer until you have reached Step 6!)__ \
If using your computer:
1. cd consumers
2. virtualenv venv
3. . venv/bin/activate
4. pip install -r requirements.txt
5. python server.py

Once the server is running, you may hit `Ctrl+C` at any time to exit.


# Step 1: Create Kafka Producer
The first step in our plan is to configure the train stations to emit some of the events that we need. The CTA has placed a sensor on each side of every train station that can be programmed to take an action whenever a train arrives at the station.

To accomplish this, you must complete the following tasks:
1. Complete the code in `producers/models/producer.py`.
2. Define a value schema for the arrival event in `producers/models/schemas/arrival_value.json` with the following attributes:
* station_id
* train_id
* direction
* line
* train_status
* prev_station_id
* prev_direction
3. Complete the code in `producers/models/station.py` so that:
* A topic is created for each station in Kafka to track the arrival events
* The station emits an arrival event to Kafka whenever the Station.run() function is called.
* Ensure that events emitted to Kafka are paired with the Avro key and value schemas
4. Define a value schema for the turnstile event in producers/models/schemas/turnstile_value.json with the following attributes
* station_id
* station_name
* line
5. Complete the code in `producers/models/turnstile.py` so that:
* A topic is created for each turnstile for each station in Kafka to track the turnstile events
* The station emits a turnstile event to Kafka whenever the `Turnstile.run()` function is called.
* Events emitted to Kafka are paired with the Avro key and value schemas

__Note__
* Make sure that you "Save" files after editing. The workspace does not support "AutoSave" functionality.
* You would not be able to edit JSON files directly in the workspace. You can edit them locally and then upload them to the workspace.


# Step 2: Configure Kafka REST Proxy Producer
Our partners at the CTA have asked that we also send weather readings into Kafka from their weather hardware. Unfortunately, this hardware is old and we cannot use the Python Client Library due to hardware restrictions. Instead, we are going to use HTTP REST to send the data to Kafka from the hardware using Kafka's REST Proxy.

To accomplish this, you must complete the following tasks:
1. Define a value schema for the weather event in `producers/models/schemas/weather_value.json` with the following attributes:
* temperature
* status
2. Complete the code in `producers/models/weather.py` so that:
* A topic is created for weather events
* The weather model emits weather event to Kafka REST Proxy whenever the Weather.run() function is called. \
    NOTE: When sending HTTP requests to Kafka REST Proxy, be careful to include the correct Content-Type. Pay close attention to the [examples in the documentation](<https://docs.confluent.io/current/kafka-rest/api.html#post--topics-(string-topic_name>) for more information.
* Events emitted to REST Proxy are paired with the Avro key and value schemas


# Step 3: Configure Kafka Connect
Finally, we need to extract station information from our PostgreSQL database into Kafka. We've decided to use the [Kafka JDBC Source Connector](https://docs.confluent.io/current/connect/kafka-connect-jdbc/source-connector/index.html).

To accomplish this, you must complete the following tasks: \
Complete the code and configuration in producers/connectors.py
* Please refer to the [Kafka Connect JDBC Source Connector Configuration Options](https://docs.confluent.io/current/connect/kafka-connect-jdbc/source-connector/source_config_options.html) for documentation on the options you must complete.
* You can run this file directly to test your connector, rather than running the entire simulation.
* Make sure to use the Kafka Connect API, Kafka-console-consumer, and Kafka-topics CLI tool to check the status and output of the Connector
* To delete a misconfigured connector: `CURL -X DELETE localhost:8083/connectors/stations`


# Step 4: Configure the Faust Stream Processor
We will leverage Faust Stream Processing to transform the raw Stations table that we ingested from Kafka Connect. The raw format from the database has more data than we need, and the line color information is not conveniently configured. To remediate this, we're going to ingest data from our Kafka Connect topic and transform the data.

To accomplish this, you must complete the following tasks: \
Complete the code and configuration in `consumers/faust_stream.py`
Watch Out! You must run this Faust processing application with the following command:
`faust -A faust_stream worker -l info`


# Step 5: Configure the KSQL Table
Next, we will use KSQL to aggregate turnstile data for each of our stations. Recall that when we produced turnstile data, we simply emitted an event, not a count. What would make this data more useful would be to summarize it by station so that downstream applications always have an up-to-date count.

To accomplish this, you must complete the following tasks: \
Complete the queries in `consumers/ksql.py`.

__Tips__
* The KSQL CLI is the best place to build your queries. Try `ksql` in your workspace to enter the CLI.
* You can run this file on its own simply by running `python ksql.py`.
* Made a mistake in table creation? `DROP TABLE <your_table>`. If the CLI asks you to terminate a running query, you can `TERMINATE <query_name>`.


# Step 6: Create Kafka Consumers
With all of the data in Kafka, our final task is to consume the data in the webserver that is going to serve the transit status pages to our commuters.

To accomplish this, you must complete the following tasks:
1. Complete the code in `consumers/consumer.py`
2. Complete the code in `consumers/models/line.py`
3. Complete the code in `consumers/models/weather.py`
4. Complete the code in `consumers/models/station.py`