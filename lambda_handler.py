import config

from src.aws_helpers.s3 import read_from_s3
from src.slackbot.messages import send_message_to_slack_channel

def handler(event, context):
    send_message_to_slack_channel("TEST")


if __name__ == '__main__':

    handler({'msg': 'Hello World!'}, None)