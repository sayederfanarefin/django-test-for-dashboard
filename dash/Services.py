
from dash.models import Document
from dash.models import LatLng
import json
import requests

class ServiceLatLng():
    Limit = 100
    ApiKey = "AIzaSyDRCwA5q9usmoR6Ts1xBLjhFnhdkhfPK3o"

    listRawLocationsJson = []
    listRawLocations = []

    def __init__(self, document):

        with open(document.filename()) as f:
            for x in json.load(f):
                newLatLng = LatLng(x['latitude'], x['longitude'])
                newLatLngJson = json.dumps(newLatLng.__dict__)
                self.listRawLocationsJson.append(newLatLngJson)
                self.listRawLocations.append(newLatLng)

    def getRawLocation(self):
        return self.listRawLocationsJson

    def getSnappedLocation(self):


        returnSplitList = self.splitList(self.listRawLocations, 6)

        for splittedList in returnSplitList:
            urlBase = 'https://roads.googleapis.com/v1/snapToRoads?path=';
            count = 0
            for location in splittedList:
                if(count < len(splittedList)-1):
                    urlBase = urlBase + str(location.getLat()) + ',' + str(location.getLng()) + '|'
                else:
                    urlBase = urlBase + str(location.getLat()) + ',' + str(location.getLng())
                count = count+1
            urlBase = urlBase + '&interpolate=true&key='+self.ApiKey
            print(urlBase)
            # r = requests.get(urlBase)
            # print (r.json())

    def splitList(self, alist, wantedParts):
        length = len(alist)
        return [alist[i * length // wantedParts: (i + 1) * length // wantedParts]
                for i in range(wantedParts)]


