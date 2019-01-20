
from dash.models import Document
from dash.models import LatLng
import json

class ServiceLatLng():
    listRawLocations = []
    def __init__(self, document):

        with open(document.filename()) as f:
            for x in json.load(f):
                newLatLng = LatLng(x['latitude'], x['longitude'])
                newLatLngJson = json.dumps(newLatLng.__dict__)
                self.listRawLocations.append(newLatLngJson)

    def getRawLocation(self):
        return self.listRawLocations