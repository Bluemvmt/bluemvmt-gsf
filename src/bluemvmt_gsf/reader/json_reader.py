from bluemvmt_gsf.models import GsfRecord


def read_from_json(json_file: str):
    """
    Read a GSF record, one line at a time and yield it to the
    calling function.

    Args:
        json_file:

    Returns:  Yields a generator that can be used to iterate through
    each line without reading the entire file into memory.
    """
    with open(json_file, "r") as f:
        for line in f:
            yield GsfRecord.model_validate_json(line)
