from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

def send_slack_message(message,task):
    channel = task.topic.slack_channel
    slack_bot_token = task.topic.workspace.bot_token

    client = WebClient(slack_bot_token)

    try:
        response = client.chat_postMessage(
            channel=channel,
            text=message
        )
        return {"error":False, "slack_response":response, "ts":response["ts"]}
    except SlackApiError as e:
        assert e.response["error"]   
        return {"error":True, "slack_response":None, "ts":None}
    
def get_user_info(user_id, slack_bot_token):
    client = WebClient(slack_bot_token)
    try:
        response = client.users_info(user=user_id)
        return response["user"]
    except SlackApiError as e:
        print(f"Error fetching user info: {e.response['error']}")
        return None

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
                "replier_slack_user": msg["user"],
                "ts": msg["ts"]
            }
            for msg in response["messages"][1:]
        ]
        for reply in replies:
            user_info = get_user_info(reply["replier_slack_user"], slack_bot_token)
            reply["replier_name"] = user_info.get("real_name")

        return {"error":False, "replies":replies, "thread":response}
    except SlackApiError as e:
        print(f"Error fetching replies: {e.response['error']}")
        return {"error":True, "replies":[], "thread":None}
    
