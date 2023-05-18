from src.aws_helpers.s3 import read_from_s3


def handler(event, context):
    print("Version 2:")
    msg = event['msg']
    print("Message: " + msg)

    # read the file
    text = read_from_s3('ziki-analytics-config', 'test.txt')
    print(text)


if __name__ == '__main__':
    handler({'msg': 'Hello World!'}, None)