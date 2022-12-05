import json
import urllib.parse
from typing import List, Literal

import requests

# Extracted API keys -- unclear what these are linked to.
_api_keys: List[str] = [
    'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8',
    'AIzaSyCtkvNIR1HCEwzsqK6JuE6KqpyjusIRI30',
    'AIzaSyA8eiZmM1FaDVjRy-df2KTyQ_vz_yYM39w',
    'AIzaSyC8UYZpvA2eknNex0Pjid0_eTLJoDu6los',
    'AIzaSyCjc_pVEDi4qsv5MtC2dMXzpIaDoRFLsxw',
    'AIzaSyDHQ9ipnphqTzDqZsbtd8_Ru4_kiKVQe2k'
]

_default_clients = {
    'WEB': {
        'context': {
            'client': {
                'clientName': 'WEB',
                'clientVersion': '2.20200720.00.02'
            }
        },
        'api_key': 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8'
    },
    'ANDROID': {
        'context': {
            'client': {
                'clientName': 'ANDROID',
                'clientVersion': '16.20'
            }
        },
        'api_key': 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8'
    },
    'WEB_EMBED': {
        'context': {
            'client': {
                'clientName': 'WEB',
                'clientVersion': '2.20210721.00.00',
                'clientScreen': 'EMBED'
            }
        },
        'api_key': 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8'
    },
    'ANDROID_EMBED': {
        'context': {
            'client': {
                'clientName': 'ANDROID',
                'clientVersion': '16.20',
                'clientScreen': 'EMBED'
            }
        },
        'api_key': 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8'
    }
}


class InnerTube:
    '''A class to interact with the InnerTube API'''

    def __init__(
        self,
        client: Literal['ANDROID', 'WEB',
                        'ANDROID_EMBED', 'WEB_EMBED'] = 'ANDROID'
    ) -> None:
        self.context = _default_clients[client]['context']
        self.api_key = _default_clients[client]['api_key']

    @property
    def base_url(self) -> str:
        '''returns the base url endpoint for the InnerTube API'''
        return 'https://www.youtube.com/youtubei/v1'

    @property
    def base_data(self) -> str:
        '''returns the base json data to send to the InnerTube API'''
        return {
            'context': self.context
        }

    @property
    def base_params(self) -> str:
        '''Return the base query parameters to transmit to the innertube API.'''
        return {
            'key': self.api_key,
            'contentCheckOk': True,
            'racyCheckOk': True
        }

    def _call_api(
        self,
        endpoint: str,
        query: dict,
        data: dict
    ) -> dict:
        '''Make a request to the given endpoint with the query and data'''
        endpoint_url = f'{endpoint}?{urllib.parse.urlencode(query)}'
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
            "accept-language": "en-US,en",
        }

        data = bytes(json.dumps(data), encoding="utf-8")

        response = requests.post(
            endpoint_url,
            headers=headers,
            data=data
        )

        return json.loads(response.text)

    def player(
        self,
        video_id: str
    ) -> dict:
        '''Get details for a Video.

        Parameters
        ----------
        video_id : `str`
            The id of the video to get the player info for.

        Returns
        -------
        response : `dict`
            raw player info json.
        '''
        endpoint = f'{self.base_url}/player'
        query = {
            'videoId': video_id,
        }
        query.update(self.base_params)

        return self._call_api(endpoint, query, self.base_data)

    def search(
        self,
        query: str,
        continuation: bool = None
    ) -> dict:
        '''Search for a track based on a query
        
        Parameters
        ----------
        query: str
            The query to search for.
        continuation: bool
            Weather to autocomplete queries based on suggestions.

        Returns
        -------
        results: List[Tracks]
            A list of search results
        '''
        endpoint = f'{self.base_url}/search'
        query = {
            "query": query,
        }
        query.update(self.base_params)
        if continuation:
            self.base_data['continuation'] = continuation
        
        return self._call_api(endpoint, query, self.base_data)

    def recommendations(
        self,
        video_id: str,
    ) -> dict:
        '''Get recommendations for a tracks complementary to a playlist

        Parameters
        ----------
        video_id : str
            ID of the video to get recommendations for.

        playlist_id : str
            ID of the playlist to get the recommendations relative to

        Returns
        -------
        response : dict
            The response form the API containig the track suggestions
        '''
        endpoint = f'{self.base_url}/music/get_queue'
        query = {
            'videoId': video_id,
            'playlistId': f'RDAMVM{video_id}',
        }
        query.update(self.base_params)

        return self._call_api(endpoint, query, self.base_data)


if __name__ == '__main__':
    tube = InnerTube()

    # player = tube.player('ZJ2RydH1EbE')
    # streams = player['streamingData']['adaptiveFormats'][-1]
    # url = streams['url']
