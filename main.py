from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

import requests

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def getCalendarService():
    """
    if show this error
    google.auth.exceptions.RefreshError:
            ('invalid_grant: Bad Request', {'error': 'invalid_grant', 'error_description': 'Bad Request'})
    remove the file token.json and rerun
    """
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('calendar', 'v3', credentials=creds)
    return service

def getURLS():
    url = 'https://www.fcf.cat/resultats/2324/futbol-11/quarta-catalana/grup-23/jornada-'
    all_urls = []
    for i in range(1,27):
        all_urls.append(f'{url}{i}')
    # return all_urls[0:1] #remove this line
    return all_urls

def getLocalTeam(game_line):
    return game_line.find_all("td", {"class": "p-5 resultats-w-equip tr"})[0].text.strip()

def getVisitorTeam(game_line):
    return game_line.find_all("td", {"class": "p-5 resultats-w-equip tl"})[0].text.strip()

def getLocation(game_line):
    return game_line.find_all("td", {"class": "p-0 resultats-w-text1 tc fs-9 capitalize ml-20 d-n_ml"})[1].find("a").get("href")

def getDate(game_line):
    url_date = game_line.find_all("td", {"class": "p-5 resultats-w-resultat tc"})[0].find("a").get("href")
    page = requests.get(url_date)
    soup = BeautifulSoup(page.content, "html.parser")
    date_str = soup.find_all("div", {"class": "acta-info print-acta-data"})[0].text.strip()
    date_str = date_str.replace("Data: ", "").replace(", ", "").replace("h", "")
    date = datetime.strptime(date_str, "%d-%m-%Y %H:%M")
    return date

def getEventFromUrl(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    game_line = soup.find(lambda tag: tag.text == 'RAYO VILADECANS, ASSOC. DEPORT.  A').parent.parent
    event_info = {}
    local_team = getLocalTeam(game_line)
    visitor_team = getVisitorTeam(game_line)
    location = getLocation(game_line)
    date = getDate(game_line)
    event = {
        'summary': f'{local_team} vs {visitor_team}',
        'location': location,
        'description': 'Partidazo de la semana',
        'start': {
            'dateTime': date.isoformat(),
            'timeZone': 'Europe/Madrid',
        },
        'end': {
            'dateTime': (date + timedelta(hours=2)).isoformat(),
            'timeZone': 'Europe/Madrid',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 60},
            ],
        },
    }
    return event

def getEvents():
    urls = getURLS()
    events = []
    for url in urls:
        event = getEventFromUrl(url)
        events.append(event)
    return events


def main():
    service = getCalendarService()
    events = getEvents()

    for event in events:
        pass
        print(event)
        service.events().insert(calendarId="92968a2bc13b4fc5ad0e75294650004ef1e069449440914adbb80892626d18f5@group.calendar.google.com", body=event).execute()


if __name__ == '__main__':
    main()