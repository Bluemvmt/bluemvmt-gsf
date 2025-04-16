import argparse
import logging
import sys

from kafka import KafkaProducer

from bluemvmt_gsf.libgsf import GsfFile
from bluemvmt_gsf.models import (  # , GsfSwathBathyPing, RecordType
    GsfRecord,
    deserialize_record,
)

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    parser = argparse.ArgumentParser("gsf_to_kafka")
    parser.add_argument(
        "--gsf-file",
        dest="gsf_file",
        type=str,
        help="The GSFS file to output to Kafka.",
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
    parser.add_argument(
        "--desired-record",
        dest="desired_record",
        type=int,
        default=0,
        help="The desired GSF record type.",
    )
    args = parser.parse_args()

    kafka_producer = KafkaProducer(bootstrap_servers=args.kafka_broker)
    print(f"kafka_producer = {kafka_producer}")

    if args.num_records > 0:
        num_records: int = args.num_records
    else:
        num_records: int = sys.maxsize

    records_read: int = 0
    with GsfFile(args.gsf_file, include_denormalized_fields=True) as gf:
        record: GsfRecord
        for record in gf.next_json_record(desired_record=args.desired_record):
            if records_read > num_records:
                break

            if record is not None:
                pyrec = deserialize_record(record)
                print(pyrec)
                kafka_producer.send(args.kafka_topic, record)
                records_read += 1
