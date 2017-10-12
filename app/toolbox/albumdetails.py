# webhook.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import sys


def get_song_details(link):
    """
    Gathers the details of each song such as artist name and song name etc...
    :param link: Link to the soundcloud song
    :return: Dictionary including the song url, name, artist and artwork url
    """
    r = requests.get(link)
    song_url = r.url
    if "soundcloud" in urlparse(song_url).netloc:
        song_domain = "soundcloud"
        print("made it to soundcloud", sys.stderr)
    else:
        return {}
        # return {
        # "song_url": "",
        # "song_artist": "",
        # "song_name": "",
        # "song_artwork_url": ""
        # }
    try:
        song_artwork_url, song_name, song_artist = sc_scraper(r.content)
    except Exception as e:
        print(e)
        return {}

    return {
        "song_url": song_url,
        "song_artist": song_artist,
        "song_name": song_name,
        "song_artwork_url": song_artwork_url
    }


def sc_scraper(content):
    """
    Use Beautiful Soup to parse through the content of the doc and find relevant details
    :param content: The content of the request to the song url
    :return: artwork url, song name and song artist
    """
    soup = BeautifulSoup(content, "html.parser")
    images = soup.find_all("img", src=True)
    for image in images:
        if "i1.sndcdn" in image["src"]:
            song_artwork_url = image["src"]
            print("song artwork: " + song_artwork_url, sys.stderr)
            break
    song_name = soup.find("a", itemprop=True).get_text() if not '' else ''
    print("song name: " + song_name, sys.stderr)
    song_artist = soup.find("a", itemprop=True).next_sibling.next_sibling.get_text()
    print("song artist " + song_artist, sys.stderr)
    return song_artwork_url, song_name, song_artist


# details = get_song_details("https://soundcloud.com/acounta/combine-ft-lilac")
# print(details)
