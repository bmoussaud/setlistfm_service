
class SetList:
    def __init__(self, json):
        self.json = json
        self.artist = self.json['artist']['name'];

    def dump(self):
        self.title()
        self.dump_set(self.json['sets'])

    @staticmethod
    def dump_set(sets):
        for s in sets['set']:
            for song in s['song']:
                if 'cover' in song:
                    print('*', song['name'], 'from', song['cover']['name'])
                    # print song
                else:
                    print(' ', song['name'])

    def tracks(self):
        """"" Return tracks using this format [(track,artist)....] """
        tracks = []
        for s in self.json['sets']['set']:
            for song in s['song']:
                if 'cover' in song:
                    tracks.append({'name': song['name'], 'artist': song['cover']['name'], 'cover': True})
                else:
                    tracks.append({'name': song['name'], 'artist': self.artist, 'cover': False})

        return tracks

    def title(self):
        return "{0} {1} {2}".format(self.json['artist']['name'], self.json['venue']['name'], self.json['eventDate'])

    def bind(self):
        tracks = self.tracks()
        preview_tracks = ', '.join([t['name'] for t in tracks])
        preview_tracks = (preview_tracks[:256] + '..') if len(preview_tracks) > 256 else preview_tracks
        return {'title': self.title(),
                'tracks': tracks,
                'id': self.json['id'],
                'url': self.json['url'],
                'preview_tracks': preview_tracks,
                'track_len': len(tracks),
                'date': self.json['eventDate'],
                'location': self.json['venue']['name']}


class SetListQuery:
    def __init__(self, api_key, requests_session=True):
        self.api_key = api_key
        if isinstance(requests_session, requests.Session):
            self._session = requests_session
        else:
            if requests_session:  # Build a new session.
                self._session = requests.Session()
            else:  # Use the Requests API module as a "session".
                from requests import api
                self._session = api

    def query_artist(self, artist):
        setlist_api = 'https://api.setlist.fm/rest/1.0'
        headers = {'Accept': 'application/json', 'Accept-Language': 'en', 'x-api-key ': self.api_key}
        payload = {'artistName': artist, 'sort': 'sortName'}
        r = self._session.get('{0}/search/setlists'.format(setlist_api), params=payload, headers=headers)
        data = r.json()
        return [SetList(setlist).bind() for setlist in data['setlist']]

    def query_id(self, setlist_id):
        setlist_api = 'https://api.setlist.fm/rest/1.0'
        headers = {'Accept': 'application/json', 'Accept-Language': 'en', 'x-api-key ': self.api_key}
        r = self._session.get('{0}/setlist/{1}'.format(setlist_api, setlist_id), headers=headers)
        data = r.json()
        return SetList(data).bind()