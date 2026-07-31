import argparse
import csv
import sys
import types

from bluemvmt_gsf.models import GsfRecord, GsfSwathBathyPing, RecordType
from bluemvmt_gsf.reader.json_reader import read_from_json


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser("gsf-to-csv")
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
    parser.add_argument(
        "--pretty-print",
        dest="pretty_print",
        action="store_true",
        help="Pretty-print the first matching records to pretty-print.json.",
        default=False,
    )
    args = parser.parse_args(argv)

    num_records = args.num_records if args.num_records > 0 else sys.maxsize

    records_read = 0
    print(f"num_records = {num_records}")
    headers: list[str] = ["time", "latitude", "longitude"]
    pretty_records: list[GsfRecord] = []

    with open(f"{args.json_file}.csv", "w", newline="") as csvfile:
        writer: csv.DictWriter | None = None
        for record in read_from_json(args.json_file):
            if records_read >= num_records:
                break
            if record.record_type != RecordType.GSF_RECORD_SWATH_BATHYMETRY_PING:
                continue
            if not isinstance(record.json_record, GsfSwathBathyPing):
                continue

            records_read += 1
            body = record.json_record
            if args.pretty_print:
                pretty_records.append(record)

            if writer is None:
                fields = type(body).model_fields
                for key, field in fields.items():
                    if isinstance(field.annotation, types.UnionType):
                        value = getattr(body, key)
                        if value is not None:
                            headers.append(key)
                    else:
                        headers.append(key)
                headers = [h for h in headers if h not in ("sep", "reserved")]
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                print(f"headers = {headers}")

            fields = type(body).model_fields
            row_dict = {
                "time": record.timestamp,
                "latitude": record.latitude,
                "longitude": record.longitude,
            }
            for header in headers[3:]:
                row_dict[header] = getattr(body, header)
            writer.writerow(row_dict)

    if args.pretty_print and pretty_records:
        with open("pretty-print.json", "w") as out:
            out.write(
                "[\n"
                + ",\n".join(r.model_dump_json(indent=4) for r in pretty_records)
                + "\n]\n"
            )


if __name__ == "__main__":
    main()
