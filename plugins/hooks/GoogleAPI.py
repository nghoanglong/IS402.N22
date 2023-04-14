from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timedelta, timezone
import os, inspect
import logging
import pandas as pd
import numpy as np
import base64
import urllib.request as ur

# script directory
current_path = os.path.dirname(
	os.path.abspath(
		inspect.getfile(
			inspect.currentframe()
		)
	)
)


class GoogleAPI:
    def __init__(self, type_api, scopes) -> None:
        # If modifying these scopes, delete the file token.json.
        self.type_api = type_api
        self.scopes = scopes
        self.creds = None
        if self.type_api == "gmail":
            name_file_token = os.path.join(current_path, "googletoken", "gmailtoken.json")
        elif self.type_api == "sheets":
            name_file_token = os.path.join(current_path, "googletoken", "sheetstoken.json")
        else:
            raise NameError("Do not known type_api: " + type_api)

        # The file token.json stores the user's access and refresh tokens,
        # and is created automatically when the authorization flow completes
        # for the first time.
        try:
            if os.path.exists(name_file_token):
                self.creds = Credentials.from_authorized_user_file(
                    name_file_token, self.scopes)
        except:
            logging.info('error when create credential')

        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(os.path.join(current_path, "googletoken", "credentials.json"), self.scopes)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(name_file_token, "w") as token:
                token.write(self.creds.to_json())

    def download_sponsered_on_gmail(self, dir_folder_save):
        service = build("gmail", "v1", credentials=self.creds)
        # Call the Gmail API
        service_messages = service.users().messages()
        # Get lists messages in label 'AMZ Advertising'
        list_m = service_messages.list(
            userId="me", labelIds="Label_8397511167865322760"
        ).execute()
        # Catch error there is no message in the label
        try:
            list_m = list_m["messages"]
        except KeyError:
            print("No messages in the label")
        else:
            for message in list_m:
                # Call gmail api to read message
                response = service_messages.get(userId="me", id=message["id"]).execute()
                # Get content of message and decode
                content = response["payload"]["parts"][0]["body"]["data"]
                content = content.replace("-", "+").replace("_", "/")
                decoded_data = base64.b64decode(content).decode().splitlines()
                # Loop line in list decoded_data and get informations
                dict_ = {}
                for line in decoded_data:
                    # Find Report name
                    if "Report name" in line:
                        dict_["Report name"] = line.replace("Report name: ", "")
                    if "Generated on" in line:
                        dict_["Generated on"] = line.replace("Generated on: ", "")
                    if "Download" in line:
                        dict_["Download"] = line.replace("Download: ", "")
                date_generated = datetime.strptime(
                    dict_["Generated on"], "%A, %B %d, %Y"
                )
                # Date report before 'Generated on' one day
                date_report = date_generated + timedelta(days=-1)
                # Because last 30 days include to day, therefore days=-29
                fromdate = date_report + timedelta(days=-29)
                date_report = date_report.strftime("%m%d%Y")
                fromdate = fromdate.strftime("%m%d%Y")
                date_report = fromdate + "-" + date_report
                file_name = (
                    dict_["Report name"].replace(" ", "_") + "_" + date_report + ".xlsx"
                )
                # Download data and save with file_name
                dir_save_name = dir_folder_save + "/" + file_name
                try:
                    ur.urlretrieve(dict_["Download"], dir_save_name)
                except Exception as error:
                    raise NameError("Download file data fail: " + error)
                # Check file download exist?
                if not os.path.exists(dir_save_name):
                    raise NameError(
                        "Do not exist file downloaded in dir: "
                        + dir_save_name
                        + " when check."
                    )
                else:
                    # Check file dowload empty?
                    df = pd.read_excel(dir_save_name)
                    columns = df.columns.to_list()
                    if not columns:
                        raise NameError("File download empty")
                    # Delete message that download completed.
                    try:
                        service_messages.delete(userId="me", id=message["id"]).execute()
                    except Exception as error:
                        raise NameError("Error when delete message: " + error)


    

