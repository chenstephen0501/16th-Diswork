import datetime
import os.path
from dotenv import load_dotenv

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
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        print("Getting the upcoming 10 events")
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
            return []

        event_list = []
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            event_list.append({"start": start, "summary": event["summary"]})

        return event_list

    except HttpError as error:
        print(f"An error occurred: {error}")
        return []


if __name__ == "__main__":
    get_calendar_events()
