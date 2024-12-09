import argparse
import csv
import sys
import types

from bluemvmt_gsf.models import GsfAllRecords, GsfRecord, GsfSwathBathyPing, RecordType

ignore_common_headers = ["sep", "reserved", "sensor_id"]


def get_headers(body: GsfSwathBathyPing) -> (list[str], list[str]):
    fields = type(body).model_fields
    common_headers: list[str] = ["time", "latitude", "longitude"]
    list_headers: list[str] = []
    for key in fields.keys():
        field = fields[key]
        if isinstance(field.annotation, types.UnionType):
            value = getattr(body, key)
            if value is not None:
                list_headers.append(key)
        else:
            common_headers.append(key)

    print(f"common_headers = {common_headers}")
    print(f"list_headers = {list_headers}")

    for header in ignore_common_headers:
        common_headers.remove(header)

    return common_headers, list_headers


def output_json(all_records_py: GsfAllRecords, cli_args):

    if cli_args.num_records > 0:
        num_records: int = cli_args.num_records
    else:
        num_records: int = sys.maxsize

    print(f"num_records = {num_records}")
    record: GsfRecord
    records_read: int = 0
    with open(f"{args.json_file}.csv", "w") as csvfile:
        with open(f"{args.json_file}-flattened.csv", "w") as flattened_csvfile:
            for record in all_records_py.records:
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
                        all_headers = common_headers + list_headers
                        writer = csv.DictWriter(csvfile, fieldnames=all_headers)
                        writer.writeheader()
                        writer = csv.DictWriter(
                            flattened_csvfile, fieldnames=all_headers
                        )
                        writer.writeheader()

                    common_row_dict = {
                        "time": record.time,
                        "latitude": record.location.latitude,
                        "longitude": record.location.longitude,
                    }
                    writer = csv.DictWriter(csvfile, fieldnames=all_headers)
                    for header in common_headers[3:]:
                        value = getattr(body, header)
                        common_row_dict[header] = value
                    list_row_dict = {}
                    for header in list_headers:
                        value = getattr(body, header)
                        list_row_dict[header] = value
                    row_dict = dict(common_row_dict)
                    row_dict.update(list_row_dict)
                    writer.writerow(row_dict)

                    writer = csv.DictWriter(flattened_csvfile, fieldnames=all_headers)
                    list_value_arrays = {}
                    for header in list_headers:
                        list_value_arrays[header] = getattr(body, header)
                    for i in range(1, body.number_beams):
                        values_dict = {}
                        print(f"list_value_arrays = {list_value_arrays}")
                        for key in list_value_arrays.keys():
                            values_dict[key] = list_value_arrays[key][i]
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
    parser.add_argument(
        "--pretty-print",
        dest="pretty_print",
        type=bool,
        help="Flag to pretty print the original JSON file.",
        default=False,
    )
    args = parser.parse_args()

    all_records: GsfAllRecords
    with open(args.json_file, "rt") as f:
        raw_json = f.read()
        all_records = GsfAllRecords.model_validate_json(raw_json)

    if args.pretty_print:
        with open("pretty-print.json", "w") as out:
            out.write(all_records.model_dump_json(indent=4))

    output_json(all_records, args)
#            print(f"record[{records_read}] = {type(body).model_fields}")
