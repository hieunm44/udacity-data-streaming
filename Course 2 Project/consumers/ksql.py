"""Configures KSQL to combine station and turnstile data"""
import json
import logging

import requests

import topic_check


logger = logging.getLogger(__name__)


KSQL_URL = "http://localhost:8088"

#
# TODO: Complete the following KSQL statements.
# TODO: For the first statement, create a `turnstile` table from your turnstile topic.
#       Make sure to use 'avro' datatype!
# TODO: For the second statment, create a `turnstile_summary` table by selecting from the
#       `turnstile` table and grouping on station_id.
#       Make sure to cast the COUNT of station id to `count`
#       Make sure to set the value format to JSON

KSQL_STATEMENT = """
CREATE TABLE turnstile (
    STATION_ID INTEGER PRIMARY KEY,
    STATION_NAME VARCHAR,
    LINE VARCHAR
) WITH (
    KAFKA_TOPIC='turnstile',
    VALUE_FORMAT='avro'
);

CREATE TABLE turnstile_summary
WITH (
    KAFKA_TOPIC='TURNSTILE_SUMMARY',
    VALUE_FORMAT='json') AS
    SELECT STATION_ID, STATION_NAME, COUNT(STATION_ID) AS COUNT
    FROM turnstile
    GROUP BY STATION_ID, STATION_NAME;
"""


def execute_statement():
    """Executes the KSQL statement against the KSQL API"""
    if topic_check.topic_exists("TURNSTILE_SUMMARY") is True:
        return

    logging.debug("executing ksql statement...")

    resp = requests.post(
        f"{KSQL_URL}/ksql",
        headers={"Content-Type": "application/vnd.ksql.v1+json"},
        data=json.dumps(
            {
                "ksql": KSQL_STATEMENT,
                "streamsProperties": {"ksql.streams.auto.offset.reset": "earliest"},
            }
        ),
    )

    # Ensure that a 2XX status code was returned
    try:
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e: 
        print(e)
        logger.info("Error with KSQL POST request.")


if __name__ == "__main__":
    execute_statement()
