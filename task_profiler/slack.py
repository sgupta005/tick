from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

def send_slack_message(message,task):
    channel = task.topic.slack_channel
    assignee_slack_user = task.assignee.slack_user
    slack_bot_token = task.topic.workspace.bot_token

    client = WebClient(slack_bot_token)
    message_with_slack_user = f"<@{assignee_slack_user}> {message}"

    try:
        response = client.chat_postMessage(
            channel=channel,
            text=message_with_slack_user
        )
        return {"slack_response":response, "ts":response["ts"]}
    except SlackApiError as e:
        assert e.response["error"]   
        return {"slack_response":None, "ts":None}

def get_question_replies_from_slack(channel, question_ts, slack_bot_token):
    client = WebClient(slack_bot_token)
    try:
        response = client.conversations_replies(
            channel=channel,
            ts=question_ts
        )
        # The first message in the response is the original message, so we skip it.
        # The subsequent messages are the replies in the thread.
        replies = [
            {
                "text": msg["text"],
                "ts": msg["ts"]
            }
            for msg in response["messages"][1:]
        ]
        return {"replies":replies, "slack_response":response}
    except SlackApiError as e:
        print(f"Error fetching replies: {e.response['error']}")
        return {"replies":[], "slack_response":None}