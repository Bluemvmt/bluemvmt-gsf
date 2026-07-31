import argparse
from time import perf_counter as pc

from pydantic import ValidationError

from bluemvmt_gsf.libgsf import GsfFile
from bluemvmt_gsf.models import GsfRecord, RecordType, deserialize_record


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser("gsf-to-json")
    parser.add_argument(
        "--gsf-file",
        dest="gsf_file",
        type=str,
        required=True,
        help="The binary GSF file to convert to JSON.",
    )
    parser.add_argument(
        "--num-records",
        dest="num_records",
        type=int,
        help="The number of records to convert (-1 for all).",
        default=-1,
    )
    parser.add_argument(
        "--desired-record",
        dest="desired_record",
        type=int,
        default=RecordType.GSF_NEXT_RECORD,
    )
    args = parser.parse_args(argv)

    print("record_type,size,time")
    records_read = 0
    with GsfFile(args.gsf_file) as gf:
        for record in gf.next_json_record(desired_record=args.desired_record):
            if args.num_records >= 0 and records_read >= args.num_records:
                break
            if record is not None:
                start = pc()
                try:
                    pyrec: GsfRecord = deserialize_record(record)
                    print(f"{pyrec.record_type},{len(record)},{pc() - start}")
                except ValidationError:
                    print(f"Pydantic doesn't validate: {record.decode('utf-8')}")
                records_read += 1


if __name__ == "__main__":
    main()
