import argparse
from time import perf_counter as pc

from bluemvmt_gsf.libgsf import GsfFile
from bluemvmt_gsf.models import GsfRecord, RecordType, deserialize_record


if __name__ == "__main__":
    parser = argparse.ArgumentParser("gsf_to_json")
    parser.add_argument(
        "--gsf-file",
        dest="gsf_file",
        type=str,
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
    args = parser.parse_args()

    print("record_type,size,time")
    with GsfFile(args.gsf_file) as gf:
        record: GsfRecord
        for record in gf.next_json_record(desired_record=args.desired_record):
            if record is not None:
                start = pc()
                pyrec: GsfRecord = deserialize_record(record)
                print(f"{pyrec.record_type},{len(record)},{pc() - start}")

    # with open_gsf(args.gsf_file, mode=FileMode.GSF_READONLY_INDEX) as gf:
    #     with open(f"{args.gsf_file}.json", "w") as f:
    #         record: GsfRecord
    #         for record in gsf_read(gf, args.gsf_file):
    #             f.write(record.model_dump_json() + "\n")
