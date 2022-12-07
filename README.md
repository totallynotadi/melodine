# melodine

melo provides consistent data models over Spotify and YouTube Music API objects.
it's main purpose is to model objects from both platforms in a way that requires no distinction based on it's source while using them

for example, a Track object from melo provides the same properties and behaviour irrespective of wether the concerned track is from Spotify or YouTube Music.

# Installation

    pip install melodine

# Usage and Features

## Consistent Data Models

the term "consistent" here implies that the models work the same way without having to care about it's source.

The Spotify and YouTube Music API provide similar attributes related to objects like a song's title, the artists related to the song, the album it's from and so on. However their schemas and the way in which objects interrelate wiht each other is totally different. Thus it becomes a pain when integrating both services into a singe application.

melo tries to solve this problem by internally separating the modelling of objects from both the services with the same structure and exporting them as global melo models, thus resulting in a robust abstraction over both services.

that means that a YouTube Music track and Spotify track can be handled as the same global melo Track object. This is done by having common attributes between the two separate internal models, like a track's name, it's artists and the album it's from, etc. such gloabl attributes that all melo tracks have (wether from Spotify or YouTube Music) are -
  
| attribute           | description                                                                               |
|---------------------|-------------------------------------------------------------------------------------------|
| album               | the melo album object for a track                                                         |
| artists             | the melo artist object for a track                                                        |
| name                | the name of the track                                                                     |
| duration            | duration of the track (in seconds)                                                        |
| href                | link to the track's source page                                                           |
| id                  | the id of the track (the video for the track on ytmusic)                                  |
| uri                 | a uri of the format `source:type:id` for example - `spotify:track:0hz0bTQC2VVb4CEjLxmKiH` |
| url                 | the url to the song playback for streaming                                                |
| images              | a list of `Image` objects (the cover art for the track)                                   |
| get_recommendations | a getter for track recommendations related to this track                                  |

_Note: there are some extra attributes for a spotify track, but are irrelevant to the core attributes_

the same applies to other models as well (artist, album, playlists, vidoes, and shows, etc)

## search

melo allows searching content from both services. Results from specific source or of specific types can be fetched.

### Spotify

```py
import melodine as melo

results = melo.spotify.search('Martin Garrix')
```

### YT Music

```py
import melodine as melo

results = melo.ytmusic.search('Martin Garrix')
```

the `search` function fetches results based on the model used. It returns a `SearchResults` instance. separated the search results based on result types. for example, only tracks results can be accessed as `SearchResults.tracks` which returns an array of Track objects (an empty array if there's no tracks in the results).

```py
results = melo.spotify.search('sewerslvt') 

print(results.tracks)

# [<melo.Track - 'Cyberia Lyr1'>, <melo.Track - 'Ecifircas'>, <melo.Track - 'goodbye'>]
```

to fetch specific types of results

```py
import melo

results = melo.spotify.search('sewerslvt', types=['track', 'playlist'])  

print(results.playlists)

# [<melo.Playlist - 'This Is Sewerslvt'>, <melo.Playlist - 'Breakcore Heaven'>]

print(results.tracks)   

# [<melo.Track - 'Ecifircas'>, <melo.Track - 'goodbye'>, <melo.Track - 'Newlove'>]

print(results.albums)

# []
```

Only the specified types of results are fetched and the other fields remain empty.

```py
import melo

ytsearch = melo.ytmusic.search('sewerslvt', source=['ytmusic'], types=['album']) 

ytsearch.albums  

# [melo.Album - 'Sewer//slvt', melo.Album - "we had good times together, don't forget that"]
```

Only YouTube Music albums will be fetched. Any combination of parameters can be used as per convinience.

## Nested Models

melo models are connected to each other. a track object has an Artist object as it's artist parameter, that artist in turn has it's own top tracks, albums and those albums have the tracks in them which are fully fledged track objects themselves which means they can lead to other recommended tracks.

as extensive as it gets, an artist could also lead to other similar artists with their own tracks tracks and albums. there's a lot of exploring to do out there

it's understandable if all thats too mind boggling, here's a code example

```py
import melo

results = melo.spotify.search('potsu', source=['ytmusic'], types=['artist'])

track_name = results.artists[0].albums[3].get_tracks()[0].name  # 'bird'
```

this crazy chaining implies getting the name of the 1st track from an artist's 3rd album where the artist is the 1st search result for a search term.

each step in fetching the desired metric is done lazily which implies melo's idea usage for using in TUI application where details need to be loaded only on clicks or other interactions.

## Spotify Authorization

melo can be used to access data to a user's spotify data. the user needs to provide consent to the developer to be able to use their spotify data.

The purpose for including this functionality is to be able to use melo's models with a user's spotify library which includes lot of liked tracks, saved albums, artists and curated playlists to extend it to the user's content.

to invoke spotify authorization

```py
import melo

melo.spotify.client.authorize()
```

this is a one-time action and does not need to be repeated once fulfilled. it is this way in order to emulate usage in a CLI or TUI application where user signin needs to be done just once.

Once authorized, the `melo.spotify.client` object can be used to make authenticated requests to the Spotify API to get the user's liked playlsits, saved albums & artists, a user's top & recently played track, and much more.

```py
from melo import spotify.client as client

# assumes the client is already authorized
recent_tracks = client.recently_played()

# [<melo.Track - 'Star Shopping'>, <melo.Track - 'Rum & Her'>, <melo.Track - '違う'>]
```

# Planned Features

- Implementing YouTube OAuth to retrieve a user's YouTube playlists
- fetching the lyrics / captions for a track
- transferring spotify playlists to youtube / youtube music and vice versa
