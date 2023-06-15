

from aws_helpers.s3 import s3, read_from_s3, write_to_s3, save_df_as_csv


def test_init():
    assert s3 is not None

