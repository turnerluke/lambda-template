import config.settings

import os

from slack import WebClient
from slack.errors import SlackApiError

import time


def delete_messages(token, channel):
    client = WebClient(token=token)
    response = client.conversations_history(channel=channel)
    messages = response['messages']
    delete_count = 0

    while len(messages) > 0:
        response = client.conversations_history(channel=channel)
        messages = response['messages']

        for message in messages:
            while True:
                try:
                    timestamp = message['ts']
                    response = client.chat_delete(channel=channel, ts=timestamp)
                    if response['ok']:
                        print("Success: " + str(delete_count))
                        delete_count += 1
                    break
                except SlackApiError as e:
                    print('Failed to delete message:', e.response['error'])
                    if e.response['error'] == 'cant_delete_message':
                        break


if __name__ == '__main__':
    token = os.environ.get('SLACK_TOKEN')
    channel = 'C0528HZC1L0'

    delete_messages(token, channel)