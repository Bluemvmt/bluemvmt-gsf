import argparse
import csv
import sys
import types

from bluemvmt_gsf.models import GsfRecord, GsfSwathBathyPing, RecordType
from bluemvmt_gsf.models.mappings import RECORD_TYPES, SENSOR_TYPES  # , SUBRECORDS
from bluemvmt_gsf.reader.json_reader import read_from_json

ignore_common_headers = ["sep", "reserved"]


def get_headers(body: GsfSwathBathyPing) -> (list[str], list[str]):
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
    for key in fields.keys():
        field = fields[key]
        if key == "sensor_id" or key == "sensor_data":
            continue

        print(f"{key} = {field.annotation}")
        if key == "ping_flags":
            common_headers.append("ping_flags")
        else:
            if isinstance(field.annotation, types.UnionType):
                value = getattr(body, key)
                if value is not None:
                    list_headers.append(key)
            else:
                print(f"Adding {key} to common_headers")
                common_headers.append(key)

    print(f"common_headers = {common_headers}")
    for header in ignore_common_headers:
        common_headers.remove(header)

    return common_headers, list_headers


def output_json(cli_args):

    if cli_args.num_records > 0:
        num_records: int = cli_args.num_records
    else:
        num_records: int = sys.maxsize

    record: GsfRecord
    records_read: int = 0
    with open(f"{args.json_file}.csv", "w") as csvfile:
        with open(f"{args.json_file}-flattened.csv", "w") as flattened_csvfile:
            for record in read_from_json(args.json_file):
                if records_read >= num_records:
                    break
                if record.record_type == RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING:
                    records_read += 1

                    body: GsfSwathBathyPing = record.body
                    common_headers: list[str]
                    list_headers: list[str]
                    all_headers: list[str]
                    if records_read == 1:
                        (common_headers, list_headers) = get_headers(body=body)
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
                    common_row_dict = {
                        "time": record.time,
                        "latitude": record.location.latitude,
                        "longitude": record.location.longitude,
                        "record_type": RECORD_TYPES[record.record_type.value],
                        "sensor.name": SENSOR_TYPES[sensor_id].value,
                        "sensor.model_number": body.sensor_data.model_number,
                        "sensor.ping_counter": body.sensor_data.ping_counter,
                        "sensor.id": sensor_id,
                    }
                    writer = csv.DictWriter(csvfile, fieldnames=all_headers)
                    for header in common_headers[8:]:
                        value = getattr(body, header)
                        common_row_dict[header] = value
                    list_row_dict = {}
                    for header in list_headers:
                        value = getattr(body, header)
                        list_row_dict[f"mb_ping.{header}"] = value
                    #                   print(f"list_row_dict = {list_row_dict}")
                    row_dict = dict(common_row_dict)
                    row_dict.update(list_row_dict)
                    writer.writerow(row_dict)

                    writer = csv.DictWriter(flattened_csvfile, fieldnames=all_headers)
                    list_value_arrays = {}
                    for header in list_headers:
                        list_value_arrays[header] = getattr(body, header)
                    for i in range(1, body.number_beams):
                        values_dict = {}
                        # print(f"list_value_arrays = {list_value_arrays}")
                        for key in list_value_arrays.keys():
                            values_dict[f"mb_ping.{key}"] = list_value_arrays[key][i]
                        row_dict = dict(common_row_dict)
                        row_dict.update(values_dict)
                        writer.writerow(row_dict)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("gsf_to_csv")
    parser.add_argument(
        "--json-file", dest="json_file", type=str, help="The JSON file to convert."
    )
    parser.add_argument(
        "--num-records",
        dest="num_records",
        type=int,
        help="The number of records to convert (-1 for all).",
        default=-1,
    )
    args = parser.parse_args()

    output_json(args)
#            print(f"record[{records_read}] = {type(body).model_fields}")
