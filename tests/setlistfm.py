import unittest

import betamax

from service import SetListQuery


class SetListQueryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.query = SetListQuery("fake_api_key")
        self.recorder = betamax.Betamax(self.query._session, cassette_library_dir='cassettes')

    def tearDown(self):
        pass

    def test_search_artist_metallica(self):
        with self.recorder.use_cassette('metallica'):
            setlist = self.query.query_artist('metallica')
            self.assertEqual(len(setlist), 20)
            entry = setlist[6]
            self.assert_setlist(entry)
            self.assert_setlist(self.query.query_id(entry['id']))

    def assert_setlist(self, entry):
        self.assertEqual(entry['title'], 'Metallica AccorHotels Arena 10-09-2017')
        print(entry['title'])
        self.assertEqual(len(entry['tracks']), 20)
        first_track = entry['tracks'][0]
        self.assertEqual(first_track['name'], 'The Ecstasy of Gold')
        self.assertEqual(first_track['artist'], 'Ennio Morricone')
        self.assertEqual(first_track['cover'], True)
        second_track = entry['tracks'][3]
        self.assertEqual(second_track['name'], 'Atlas, Rise!')
        self.assertEqual(second_track['artist'], 'Metallica')
        self.assertEqual(second_track['cover'], False)
