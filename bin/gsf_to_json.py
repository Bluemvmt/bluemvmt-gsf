import argparse

from bluemvmt_gsf.libgsf import open_gsf

from bluemvmt_gsf.models import GsfRecord


def test_nested_yield(file_name: str):
    with open_gsf(file_name) as gf:
        record: GsfRecord
        for record in gf.next_json_record():
            yield record


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
    args = parser.parse_args()

    for record in test_nested_yield(args.gsf_file):
        print(record)

    # with open_gsf(args.gsf_file, mode=FileMode.GSF_READONLY_INDEX) as gf:
    #     with open(f"{args.gsf_file}.json", "w") as f:
    #         record: GsfRecord
    #         for record in gsf_read(gf, args.gsf_file):
    #             f.write(record.model_dump_json() + "\n")
