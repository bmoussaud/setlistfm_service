import sys

import betamax
import requests
from betamax_serializers import pretty_json

from service import SetListQuery

if len(sys.argv) == 1:
    print("NO SETLIST_FM_API_KEY...exit...!")
    sys.exit(0)

SETLIST_FM_API_KEY = sys.argv[1]

session = requests.Session()
query = SetListQuery(SETLIST_FM_API_KEY, session)
betamax.Betamax.register_serializer(pretty_json.PrettyJSONSerializer)
recorder = betamax.Betamax(session, cassette_library_dir='cassettes')
with recorder.use_cassette('metallica', serialize_with='prettyjson'):
    query.query_id('6be2ce06')
    lists = query.query_artist('metallica')

print ('-recorded-')
