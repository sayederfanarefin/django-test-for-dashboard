
from dash.models import Document
from dash.models import LatLng
import json
import requests
import math

class ServiceLatLng():
    Limit = 100
    ApiKey = "AIzaSyCOeAzlHTG2XxZNm4nrnj8NS1J8XLA0nOQ"

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

        returnSplitList = self.splitList(self.listRawLocations, self.getSplitCount())


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

    def getSplitCount(self):
        return math.ceil(len(self.listRawLocations)/self.Limit)