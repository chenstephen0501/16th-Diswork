from datetime import datetime, timedelta
import os.path
from dotenv import load_dotenv
import html

load_dotenv()

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def get_calendar_events():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(
                {
                    "installed": {
                        "client_id": os.environ.get("CLIENT_ID"),
                        "project_id": os.environ.get("PROJECT_ID"),
                        "auth_uri": os.environ.get("AUTH_URI"),
                        "token_uri": os.environ.get("TOKEN_URI"),
                        "auth_provider_x509_cert_url": os.environ.get(
                            "AUTH_PROVIDER_X509_CERT_URL"
                        ),
                        "client_secret": os.environ.get("CLIENT_SECRET"),
                        "redirect_uris": os.environ.get("REDIRECT_URIS"),
                    }
                },
                SCOPES,
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        # Call the Calendar API
        now = datetime.utcnow()
        three_years_ago = now - timedelta(days=365 * 3)
        three_years_later = now + timedelta(days=365 * 3)
        now = datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time

        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=three_years_ago.isoformat() + "Z",  # 從三年前開始
                timeMax=three_years_later.isoformat() + "Z",  # 到三年後結束
                maxResults=1000,  # 最多返回 1000 個事件，你可以根據需要調整
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            return []

        event_list = []
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            end = event["end"].get("dateTime", event["end"].get("date"))
            event_list.append(
                {
                    "start": start,
                    "end": end,
                    "summary": event["summary"],
                }
            )

        return event_list

    except HttpError as error:
        print(f"An error occurred: {error}")
        return []


if __name__ == "__main__":
    get_calendar_events()
