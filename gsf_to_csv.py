import argparse
import csv
import sys
import types

from bluemvmt_gsf.models import GsfAllRecords, GsfRecord, GsfSwathBathyPing, RecordType

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
            if records_read >= num_records:
                break
            if record.record_type == RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING:
                records_read += 1
                writer = csv.DictWriter(csvfile, fieldnames=headers)

                body: GsfSwathBathyPing = record.body
                if records_read == 1:
                    fields = type(body).model_fields
                    for key in fields.keys():
                        field = fields[key]
                        if isinstance(field.annotation, types.UnionType):
                            print(f"list {key} is {field.annotation}")
                            value = getattr(body, key)
                            if value is not None:
                                headers.append(key)
                        else:
                            print(
                                f"{key} is {field.annotation}, {type(field.annotation)}"
                            )
                            headers.append(key)
                    headers.remove("sep")
                    headers.remove("reserved")
                    writer.writeheader()
                    print(f"headers = {headers}")
                fields = type(body).model_fields
                row_dict = {
                    "time": record.time,
                    "latitude": record.location.latitude,
                    "longitude": record.location.longitude,
                }
                for header in headers[3:]:
                    field = fields[header]
                    value = getattr(body, header)
                    row_dict[header] = value
                writer.writerow(row_dict)
#            print(f"record[{records_read}] = {type(body).model_fields}")
