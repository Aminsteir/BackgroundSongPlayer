import webbrowser
import speech_recognition as sr
import os
from gtts import gTTS
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

spotify = spotipy.Spotify()
spotify.trace = False

client_credentials_manager = SpotifyClientCredentials(client_id='63b5eec3be3f468084c020dff063980f', client_secret='abd1530805fb4884b3738d2f217151a6')
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def speak(audio, fileName="tmp"):
    print(('Computer: {}').format(audio))
    tts = gTTS(text=audio, lang='en')
    tts.save(("{}.mp3").format(fileName))
    os.system(("mpg321 {}.mp3").format(fileName))


def returnedQuery(defaultReturnVal="Senorita by Shawn Mendes"):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.dynamic_energy_adjustment_ratio = 1.3
        r.pause_threshold = 0.75
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language='en-us')
        print('User: ' + query + '\n')
    except sr.UnknownValueError:
        query = defaultReturnVal
    return query


def getSearchQuery():
	speak('\nWhat song do you want?')
	query = returnedQuery().lower()
	return query


def main():
    	query = returnedQuery().lower()
    	while True:
	    	if 'play song' in query:
	    		query = getSearchQuery()
	    		if 'album' in query or 'album by' in query:
	    			album(query)
	    		elif 'by ' in query:
	    			trackBy(query)
	    		elif query == 'cancel':
	    			exit()
	    		else:
	    			print("Defaulting to track with query")
	    			track(query)
	    	elif query == 'cancel':
	    		exit()
	    	else:
	    		query = returnedQuery().lower()
	    	print("\n")


def album(query):
	print("Album --------")
	parsed_bf,parsed_af = query.split('album', 1);
	results = spotify.search(q = "album:" + parsed_bf, type = "album")
	if len(results['albums']['items']) != 0:
		album_id = results['albums']['items'][0]['id']
	else:
		speak('No such album exists, please try again')
		query = getSearchQuery()
		album(query)
	album_url = ("http://open.spotify.com/album/{}").format(album_id)
	print(('{} URL: {}').format(query,album_url))
	webbrowser.open(album_url, new=2)
	

def trackBy(query):
	print("Track --------")
	parsed_bf, parsed_af = query.split('by ', 1)
	results = spotify.search(q = "track:" + parsed_bf, type = "track")
	track_list = results['tracks']['items']
	if len(track_list) == 0:
		speak('No such track exists, please try again')
		query = getSearchQuery()
		trackBy(query)
	else:
		sug_list = ['nope']*len(track_list)
		i = 0
		for x in range(len(track_list)):
			for artist in range(len(track_list[x]['artists'])):
				if parsed_af.lower() == track_list[x]['artists'][artist]['name'].lower():
					sug_list[i] = track_list[x]['id']
					i+=1
		if sug_list[0] == 'nope':
			sug_list[0] = track_list[0]['id']
		track_url = ("http://open.spotify.com/track/{}").format(sug_list[0])
		print(('{} URL: {}').format(query, track_url))
		webbrowser.open(track_url, new=2)


def track(query):
	print("Track --------")
	if 'by ' in query:
		trackBy(query)
		return
	results = spotify.search(q = "track:" + query, type = "track")
	if len(results['tracks']['items']) != 0:
		track_id = results['tracks']['items'][0]['id']
		album_url = ("http://open.spotify.com/track/{}").format(track_id)
		print(('{} URL: {}').format(query, album_url))
		webbrowser.open(album_url, new=2)
	else:
		speak('No such track exists, please try again')
		query = getSearchQuery()
		track(query)


if __name__ == '__main__':
	os.system('clear')
	speak("Spotify Search Startup")
	main()