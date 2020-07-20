from bs4 import BeautifulSoup
import pandas as pd
import requests
from Bot import settings
# import os


def get_url(track_request):
    """
    The function allows to get the URL with a list of songs based on user's request
    """
    final_link = ''
    track_request_list = track_request.split()
    for i in track_request_list:
        final_link = final_link + '+' + i
    url = 'https://ruq.hotmo.org/search?q=' + str(final_link)
    return url


def get_html(url, params=None):
    """
    The function allows to get the URL's data
    """
    s = requests.Session()
    r = s.get(url, headers=settings.HEADERS, params=params)
    # r=requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    """
    The function collects info about songs (title, singer, time) for user
    """
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='track__info')  # singer and song
    links = soup.find_all('a', class_='track__download-btn')  # link to download

    target_tracks_track = []
    target_tracks_singer = []
    target_tracks_link = []
    target_tracks_time = []

    for item in items:
        target_tracks_singer.append(
            item.find('div', class_='track__desc').get_text().strip()[:13])  # 45 signs max for buttons
        target_tracks_track.append(
            item.find('div', class_='track__title').get_text().strip()[:13])  # 45 signs max for buttons
        target_tracks_time.append(
            item.find('div', class_='track__time').get_text().strip()[:6])  # 45 signs max for buttons

    for link in links:
        target_tracks_link.append(link.get('href'))

    df = pd.DataFrame(target_tracks_singer)
    df.columns = ['target_tracks_singer']
    df['target_tracks_track'] = target_tracks_track
    df['target_tracks_time'] = target_tracks_time
    df['target_tracks_link'] = target_tracks_link
    df['target_tracks_target'] = df['target_tracks_time'] + ' | ' + df['target_tracks_singer'] + ' - ' + df[
        'target_tracks_track']

    # df.to_csv(os.path.join(os.path.dirname(__file__), "../telegrambot_music_final/check.csv"))

    return df


def parse(url):
    """
    The function returns the result of "get_html" and "get_content" functions
    """

    # print(url)
    html = get_html(url)
    if html.status_code == 200:
        return get_content(html.text)
    else:
        return 'Error'


if __name__ == "__main__":
    parse('https://ruq.hotmo.org/search?q=Billie+Bad+Guy')