import os


def test_config():
    import config.settings
    assert os.environ['SLACK_CHANNEL'] is not None

