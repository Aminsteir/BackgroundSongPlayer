import pyttsx3
import webbrowser
import speech_recognition as sr
import os
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[len(voices) - 1].id)

spotify = spotipy.Spotify()
spotify.trace = False

client_credentials_manager = SpotifyClientCredentials(client_id='client_id',
                                                      client_secret='client_secret')
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def speak(audio):
    print(('Computer: {}').format(audio))
    engine.say(audio)
    engine.runAndWait()


def returned_query(defaultReturnVal="Senorita by Shawn Mendes"):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.dynamic_energy_adjustment_ratio = 1.3
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language='en-us')
        print('User: ' + query + '\n')
    except sr.UnknownValueError:
        query = defaultReturnVal
    return query


def get_search_query():
    speak('What song do you want?')
    query = returned_query().lower()
    return query


def main():
    query = returned_query().lower()
    while True:
        if 'play song' in query:
            query = get_search_query()
            if 'album' in query or 'album by' in query:
                album(query)
            elif 'by ' in query:
                track_by(query)
            elif query == 'cancel':
                exit()
            else:
                print("Defaulting to track with query")
                track(query)
        elif query == 'cancel':
            exit()
        else:
            query = returned_query().lower()
        print("\n")


def album(query):
    print("Album --------")
    parsed_bf, parsed_af = query.split('album', 1);
    results = spotify.search(q="album:" + parsed_bf, type="album")
    try:
        album_id = results['albums']['items'][0]['id']
    except IndexError:
        speak('No such album exists, please try again')
        query = get_search_query()
        album(query)
    album_url = ("http://open.spotify.com/album/{}").format(album_id)
    print(('{} URL: {}').format(query, album_url))
    webbrowser.open(album_url, new=2)


def track_by(query):
    print("Track --------")
    parsed_bf, parsed_af = query.split('by ', 1)
    results = spotify.search(q="track:" + parsed_bf, type="track")
    track_list = results['tracks']['items']
    if len(track_list) == 0:
        speak('No such track exists, please try again')
        query = get_search_query()
        track(query)
    else:
        sug_list = ['nope'] * len(track_list)
        i = 0
        for x in range(len(track_list)):
            for artist in range(len(track_list[x]['artists'])):
                if parsed_af.lower() == track_list[x]['artists'][artist]['name'].lower():
                    sug_list[i] = track_list[x]['id']
                    i += 1
        if sug_list[0] == 'nope':
            sug_list[0] = track_list[0]['id']
        track_url = ("http://open.spotify.com/track/{}").format(sug_list[0])
        print(('{} URL: {}').format(query, track_url))
        webbrowser.open(track_url, new=2)


def track(query):
    print("Track --------")
    if 'by ' in query:
        track_by(query)
        return
    results = spotify.search(q="track:" + query, type="track")
    if len(results['tracks']['items']) != 0:
        track_id = results['tracks']['items'][0]['id']
        album_url = ("http://open.spotify.com/track/{}").format(track_id)
        print(('{} URL: {}').format(query, album_url))
        webbrowser.open(album_url, new=2)
    else:
        speak('No such track exists, please try again')
        query = get_search_query()
        track(query)


if __name__ == '__main__':
    os.system('clear')
    speak("Spotify Search Startup")
    main()
