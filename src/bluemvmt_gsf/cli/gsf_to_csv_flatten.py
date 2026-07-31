import argparse
import csv
import sys
import types

from bluemvmt_gsf.models import GsfSwathBathyPing, RecordType
from bluemvmt_gsf.models.mappings import RECORD_TYPES, SENSOR_TYPES
from bluemvmt_gsf.reader.json_reader import read_from_json

ignore_common_headers = ["sep", "reserved"]


def get_headers(body: GsfSwathBathyPing) -> tuple[list[str], list[str]]:
    fields = type(body).model_fields
    common_headers: list[str] = [
        "time",
        "latitude",
        "longitude",
        "sensor.id",
        "sensor.name",
        "sensor.model_number",
        "sensor.ping_counter",
        "record_type",
    ]
    list_headers: list[str] = []
    for key, field in fields.items():
        if key in ("sensor_id", "sensor_data"):
            continue

        print(f"{key} = {field.annotation}")
        if key == "ping_flags":
            common_headers.append("ping_flags")
        elif isinstance(field.annotation, types.UnionType):
            value = getattr(body, key)
            if value is not None:
                list_headers.append(key)
        else:
            print(f"Adding {key} to common_headers")
            common_headers.append(key)

    print(f"common_headers = {common_headers}")
    for header in ignore_common_headers:
        if header in common_headers:
            common_headers.remove(header)

    return common_headers, list_headers


def output_json(cli_args: argparse.Namespace) -> None:
    num_records = cli_args.num_records if cli_args.num_records > 0 else sys.maxsize

    records_read = 0
    common_headers: list[str] = []
    list_headers: list[str] = []
    all_headers: list[str] = []

    with open(f"{cli_args.json_file}.csv", "w", newline="") as csvfile:
        with open(
            f"{cli_args.json_file}-flattened.csv", "w", newline=""
        ) as flattened_csvfile:
            for record in read_from_json(cli_args.json_file):
                if records_read >= num_records:
                    break
                if record.record_type != RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING:
                    continue
                if not isinstance(record.json_record, GsfSwathBathyPing):
                    continue

                records_read += 1
                body = record.json_record

                if records_read == 1:
                    common_headers, list_headers = get_headers(body=body)
                    all_headers = common_headers + [
                        f"mb_ping.{h}" for h in list_headers
                    ]
                    print(f"all_headers = {all_headers}")
                    writer = csv.DictWriter(csvfile, fieldnames=all_headers)
                    writer.writeheader()
                    writer = csv.DictWriter(
                        flattened_csvfile, fieldnames=all_headers
                    )
                    writer.writeheader()

                sensor_id = body.sensor_id
                sensor_data = body.sensor_data
                common_row_dict = {
                    "time": record.timestamp,
                    "latitude": record.latitude,
                    "longitude": record.longitude,
                    "record_type": RECORD_TYPES[record.record_type.value],
                    "sensor.name": SENSOR_TYPES[sensor_id].value,
                    "sensor.model_number": (
                        sensor_data.model_number if sensor_data is not None else None
                    ),
                    "sensor.ping_counter": (
                        sensor_data.ping_counter if sensor_data is not None else None
                    ),
                    "sensor.id": sensor_id,
                }
                writer = csv.DictWriter(csvfile, fieldnames=all_headers)
                for header in common_headers[8:]:
                    common_row_dict[header] = getattr(body, header)
                list_row_dict = {}
                for header in list_headers:
                    list_row_dict[f"mb_ping.{header}"] = getattr(body, header)
                row_dict = dict(common_row_dict)
                row_dict.update(list_row_dict)
                writer.writerow(row_dict)

                writer = csv.DictWriter(flattened_csvfile, fieldnames=all_headers)
                list_value_arrays = {
                    header: getattr(body, header) for header in list_headers
                }
                for i in range(body.number_beams):
                    values_dict = {}
                    for key, values in list_value_arrays.items():
                        if values is not None:
                            values_dict[f"mb_ping.{key}"] = values[i]
                    row_dict = dict(common_row_dict)
                    row_dict.update(values_dict)
                    writer.writerow(row_dict)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser("gsf-to-csv-flatten")
    parser.add_argument(
        "--json-file",
        dest="json_file",
        type=str,
        required=True,
        help="NDJSON file of GSF records to convert.",
    )
    parser.add_argument(
        "--num-records",
        dest="num_records",
        type=int,
        help="The number of records to convert (-1 for all).",
        default=-1,
    )
    args = parser.parse_args(argv)
    output_json(args)


if __name__ == "__main__":
    main()
