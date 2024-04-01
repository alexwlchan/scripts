#!/usr/bin/env python3
"""
Get a list of my Liked videos on YouTube.

It prints the URL of each video, newest first.

Example use:

    $ python3 web/list_liked_youtube_videos.py > liked_videos.$(date +"%Y-%m-%d").txt

"""

import contextlib
import datetime
import json
import sys

import google.oauth2.credentials
import googleapiclient.discovery  # pip install google-api-python-client==1.7.2
import google_auth_oauthlib.flow  # pip install google-auth-oauthlib==0.4.1
import keyring


class YouTubeClient:
    def __init__(self, label: str):
        self.api_service_name = "youtube"
        self.api_version = "v3"
        self.scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

        self.youtube = self.create_youtube_client(label)

    def create_youtube_client(self, label: str):
        """
        Get an authenticated OAuth client for YouTube.

        It gets the OAuth config from the system keychain, and caches
        per-user credentials in the keychain under ("youtube", label).
        """
        # Try to retrieve a stored OAuth access token from the keychain.
        #
        # This saves me going through the in-browser authentication flow
        # if I've already run the script.
        stored_credentials = keyring.get_password("youtube", label)

        if stored_credentials is not None:
            json_credentials = json.loads(stored_credentials)

            if "expiry" in json_credentials:
                expiry = datetime.datetime.fromisoformat(json_credentials["expiry"])
                expiry = expiry.replace(tzinfo=None)
                json_credentials["expiry"] = expiry

            credentials = google.oauth2.credentials.Credentials(**json_credentials)

        # If there are no stored credentials, fetch new ones.
        else:
            # Retrieve the OAuth client credentials from the keychain.
            #
            # This contains the contents of the JSON file that I downloaded
            # from the Google Cloud console, but now those credentials aren't
            # just saved as a plaintext file on disk.
            stored_client_secrets = keyring.get_password("youtube", "client_secrets")
            if stored_client_secrets is None:
                raise ValueError("Could not find OAuth client secrets in keychain!")

            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_config(
                client_config=json.loads(stored_client_secrets), scopes=self.scopes
            )

            with contextlib.redirect_stdout(sys.stderr):
                credentials = flow.run_local_server()

            # Save these credentials in the system keychain, so they can be
            # retrieved later.
            keyring.set_password("youtube", label, credentials.to_json())

        youtube = googleapiclient.discovery.build(
            self.api_service_name, self.api_version, credentials=credentials
        )

        # The OAuth credentials don't last forever -- they seem to expire after
        # a week.  This is a slightly ropey attempt to work around that.
        #
        # If we call the API and the saved token is expired, just delete
        # it and get new creds -- sending me back through the in-browser flow.
        #
        # Notes:
        #
        #   - There are ways to refresh OAuth tokens that don't involve
        #     sending me back through the in-browser flow, but I didn't
        #     look at them as part of this project.
        #   - Catching all exceptions is a bit broad.  This code should really
        #     retry only if it gets a "credentials expired" exception, and
        #     throw any other exceptions immediately.
        #
        try:
            request = youtube.channels().list(part="snippet", mine=True)
            request.execute()
        except Exception:
            keyring.delete_password("youtube", label)
            return self.create_youtube_client(label)
        else:
            return youtube

    def get_liked_videos(self):
        """
        Generate a list of videos that this YouTube account has liked.
        """
        kwargs = {"part": "snippet", "playlistId": "LL", "maxResults": "50"}

        while True:
            request = self.youtube.playlistItems().list(**kwargs)
            response = request.execute()

            for item in response["items"]:
                if item["snippet"]["title"] in {"Deleted video", "Private video"}:
                    continue

                yield item

            try:
                kwargs["pageToken"] = response["nextPageToken"]
            except KeyError:
                break


if __name__ == "__main__":
    youtube = YouTubeClient(label="download_liked_videos")

    for video in youtube.get_liked_videos():
        video_id = video["snippet"]["resourceId"]["videoId"]
        print(f"https://www.youtube.com/watch?v={video_id}")
