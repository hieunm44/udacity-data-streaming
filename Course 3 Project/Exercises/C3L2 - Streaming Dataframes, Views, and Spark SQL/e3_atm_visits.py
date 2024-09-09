from pyspark.sql import SparkSession

# TO-DO: create a spark session, with an appropriately named application name

#TO-DO: set the log level to WARN

#TO-DO: read the atm-visits kafka topic as a source into a streaming dataframe with the bootstrap server localhost:9092, configuring the stream to read the earliest messages possible                                    

#TO-DO: using a select expression on the streaming dataframe, cast the key and the value columns from kafka as strings, and then select them

# TO-DO: create a temporary streaming view called "ATMVisits" based on the streaming dataframe

# TO-DO query the temporary view with spark.sql, with this query: "select * from ATMVisits"

# TO-DO: write the dataFrame from the last select statement to kafka to the atm-visit-updates topic, on the broker localhost:9092, and configure it to retrieve the earliest messages 
