import argparse
import logging
import sys

from kafka import KafkaProducer

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    parser = argparse.ArgumentParser("load_json")
    parser.add_argument(
        "--json-file",
        dest="json_file",
        type=str,
        help="The JSON file to load.",
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

    print(f"kafka_broker url = {args.kafka_broker}")
    kafka_producer = KafkaProducer(bootstrap_servers=args.kafka_broker)

    if args.num_records > 0:
        num_records: int = args.num_records
    else:
        num_records: int = sys.maxsize

    with open(args.json_file, "rt") as f:
        records_read = 0
        for line in f:
            if records_read >= num_records:
                break
            records_read += 1
            message = line.encode("utf-8")
            print(f"message = {message}")
            kafka_producer.send(args.kafka_topic, message)
