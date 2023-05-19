import os

from slack_sdk import WebClient
# from slack_sdk.errors import SlackApiError
# from slack_cleaner2 import SlackCleaner, match

SLACK_TOKEN = os.environ['SLACK_TOKEN']
SLACK_CHANNEL = os.environ['SLACK_CHANNEL']


client = WebClient(token=SLACK_TOKEN)


def send_message_to_slack_channel(message: str, thread_ts: str = None) -> str:
    # Call the conversations.list method using the WebClient
    result = client.chat_postMessage(
        channel="#"+SLACK_CHANNEL,
        text=message,
        link_names=True,
        thread_ts=thread_ts
    )
    return result['ts']


# def clean_history(channel_name: str) -> None:
#     s = SlackCleaner(SLACK_TOKEN)
#
#     for msg in s.msgs(filter(match(f'{channel_name}'), s.conversations)):
#         # delete messages, its files, and all its replies (thread)
#         msg.delete(replies=True, files=True)