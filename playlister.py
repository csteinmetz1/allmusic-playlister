import json
from bs4 import BeautifulSoup
from collections import OrderedDict
import pandas as pd
import spotipy
import spotipy.util as util

artist_id = "tony-doogan"
artist_name = "Tony Doogan"
credits_page = "pages/"+artist_id+".html"

# dict to store columns
database = OrderedDict({'year' : [], 
                        'album' : [],
                        'artist' : [],
                        'credits' : [],
						'album_id' : [],
						'track_ids' : []})

print('Getting credits for {0}...'.format(artist_name))
soup = BeautifulSoup(open(credits_page), 'html.parser')
table = soup.find('body').find('table', {'class' : 'artist-credits'}).find_all('tr')

for entry in table:
	if len(entry.find_all('td')) != 0:
		database['year'].append(entry.find('td', {'class' : 'year'}).text.strip())
		database['album'].append(entry.find('td', {'class' : 'album'}).a.text.strip())
		database['artist'].append(entry.find('td', {'class' : 'artist'}).text.strip())
		database['credits'].append(entry.find('td', {'class' : 'credit'}).text.strip())

keys = json.load(open('keys.json'))
username = ''
scope = 'playlist-modify-public'

token = util.prompt_for_user_token(username, scope, client_id=keys['client_id'], 
									client_secret=keys['client_secret'], redirect_uri=keys['redirect_uri'])

if token:
	sp = spotipy.Spotify(auth=token)
	user_id = sp.me()['id']

	# create new artist/engineer/producer playlist
	playlist_id = sp.user_playlist_create(user_id, artist_name)['id']

	for idx, album in enumerate(database['album']):
		artist = database['artist'][idx]
		if artist == "":
			print("{0} had no artist. Skipping...".format(album))
			database['album_id'].append("")
			database['track_ids'].append("")
		else:
			print("Searching for {0} by {1}...".format(album, artist))
			result = sp.search(album + " " + artist, limit=1, type='album')
			if len(result['albums']['items']) == 1:
				album_id = result['albums']['items'][0]['id']
				database['album_id'].append(album_id)
				print("Adding album ID {0}".format(result['albums']['items'][0]['id']))
				tracks = sp.album_tracks(album_id)
				track_ids = [track['uri'] for track in tracks['items']]
				database['track_ids'].append(",".join(track_ids)) # append track ids as a string
				print("Added {0:d} tracks...".format(len(track_ids)))
				sp.user_playlist_add_tracks(user_id, playlist_id, track_ids)
			else:
				print("{0} by {1} was not found in Spotify...".format(album, artist))
				database['album_id'].append("")
				database['track_ids'].append("")

# create dataframe and save result to csv
dataframe = pd.DataFrame(database)
dataframe.to_csv("data/"+artist_id+".csv", sep=',')
print("Saved {0:d} credits from {1}.".format(len(database['year']), artist_name))