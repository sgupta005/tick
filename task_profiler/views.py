# views.py
import requests
from django.http import HttpResponse
from django.conf import settings


def slack_oauth_callback(request):
    code = request.GET.get("code")
    if not code:
        return HttpResponse("No code received")

    response = requests.post("https://slack.com/api/oauth.v2.access", data={
        "client_id": settings.SLACK_APP_CLIENT_ID,
        "client_secret": settings.SLACK_APP_CLIENT_SECRET,
        "code": code,
        "redirect_uri": settings.REDIRECT_URI
    })

    data = response.json()
    print(data)
    if data.get("ok"):
        access_token = data.get("authed_user").get("access_token")  # This is your new xoxp token
        return HttpResponse(f"Success! User token: {access_token}")
    else:
        return HttpResponse(f"OAuth failed: {data.get('error')}")
