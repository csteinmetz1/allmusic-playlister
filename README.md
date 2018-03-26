# allmusic-playlister
Save all the album credits from an artist/engineer/producer to a Spotify playlist.

I wanted an easy way to build playlists that contained all of the work from accomplished audio engineers so this set of scripts will scrape the credit lists from [allmusic.com][http://allmusic.com] and then build Spotify playlists containing all of the albums/singles that they contributed to. 

## Setup

Install dependancies

$ pip install --upgrade -r requirements.txt

Setup the environment

$ python setup_eny.py

Edit the `keys.json` file and set your `client_id` and `client_secret` after creating a Spotify API app [here](https://beta.developer.spotify.com/dashboard/applications).

## Usage

Since [allmusic.com][http://allmusic.com] does not allow web scrapping anymore you first need to save the .html file from each credits page first via your browser. Save these files into the `pages` directory. Then set the correct info in the top of the `playlister.py` script and run it.

$ python playlister.py

This will generate a .csv file with all of the collected data as well as save a new playlist to your Spotify account.

