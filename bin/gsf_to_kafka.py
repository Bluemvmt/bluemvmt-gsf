import argparse
import logging
import sys

from kafka import KafkaProducer

from bluemvmt_gsf.models import (  # , GsfSwathBathyPing, RecordType
    GsfAllRecords,
    GsfRecord,
)

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    parser = argparse.ArgumentParser("gsf_to_kafka")
    parser.add_argument(
        "--json-file",
        dest="json_file",
        type=str,
        help="The JSON file to convert.",
        required=True,
    )
    parser.add_argument(
        "--kafka-topic",
        dest="kafka_topic",
        type=str,
        help="The Kafka topic to publish the GSF data to.",
        required=True,
    )
    parser.add_argument(
        "--kafka-broker",
        dest="kafka_broker",
        type=str,
        help="""
        The hostname:port for the Kafka broker to which
        the GSF records will be published.
        """,
        default="localhost:9092",
    )
    parser.add_argument(
        "--num-records",
        dest="num_records",
        type=int,
        help="The number of records to publish (-1 for all).",
        default=-1,
    )
    args = parser.parse_args()

    kafka_producer = KafkaProducer(bootstrap_servers=args.kafka_broker)
    print(f"kafka_producer = {kafka_producer}")

    all_records: GsfAllRecords
    with open(args.json_file, "rt") as f:
        raw_json = f.read()
        all_records = GsfAllRecords.model_validate_json(raw_json)

    if args.num_records > 0:
        num_records: int = args.num_records
    else:
        num_records: int = sys.maxsize

    record: GsfRecord
    records_read: int = 0
    print(f"num_records = {num_records}")
    headers: list[str] = ["time", "latitude", "longitude"]
    with open(f"{args.json_file}.csv", "w") as csvfile:
        for record in all_records.records:
            records_read += 1
            if records_read >= num_records:
                break

            message = record.model_dump_json().encode("utf-8")
            print(f"message = {message}")
            kafka_producer.send(args.kafka_topic, message)
