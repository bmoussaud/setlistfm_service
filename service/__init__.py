#!flask/bin/python
import requests
from flask import Flask, jsonify, make_response, url_for

from service.config import configure_app
from service.utils import get_instance_folder_path

app = Flask(__name__, instance_path=get_instance_folder_path(),
            instance_relative_config=True)
configure_app(app)
SETLIST_FM_API_KEY_ = app.config['SETLIST_FM_API_KEY']


# sample code: https://gist.github.com/shivam5992/8451692
# from https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask

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


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'message': error.description}), 404)


@app.errorhandler(500)
def tech_error(error):
    return make_response(jsonify({'error': 'Technical error.', 'message': error.description}), 500)


def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task


if __name__ == '__main__':
    app.run(debug=True, host=app.config['SETLIST_HOST'], port=app.config['SETLIST_PORT'])
