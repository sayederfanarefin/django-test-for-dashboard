
from dash.models import Document
from dash.models import LatLng
import json
import requests
import math
from vincenty import vincenty

class ServiceLatLng():
    Limit = 100
    ApiKey = "AIzaSyCOeAzlHTG2XxZNm4nrnj8NS1J8XLA0nOQ"

    listSnappedLocationsJson = []
    listRawLocationsJson = []
    listRawLocations = []

    #first contact
    def __init__(self, document):

        with open(document.filename()) as f:
            for x in json.load(f):
                newLatLng = LatLng(x['latitude'], x['longitude'])
                newLatLngJson = json.dumps(newLatLng.__dict__)
                self.listRawLocationsJson.append(newLatLngJson)
                self.listRawLocations.append(newLatLng)

    #return raw loations
    def getRawLocation(self):
        return self.listRawLocationsJson

    #used snap to road api to snap the locations to road
    def getSnappedLocation(self):

        #filter the list of raw locations in order lower the usage of google roads api
        filteredList = self.filterClosePoints(self.listRawLocations)

        # split the whole list of locations to several lists in order to avoid too large url, the split takes place by the Limit variable
        returnSplitList = self.splitList(filteredList, self.getSplitCount(filteredList))

        #iterate over the chunks of the main list
        for splittedList in returnSplitList:
            urlBase = 'https://roads.googleapis.com/v1/snapToRoads?path=';
            count = 0
            #building the url
            for location in splittedList:
                if(count < len(splittedList)-1):
                    urlBase = urlBase + str(location.getLat()) + ',' + str(location.getLng()) + '|'
                else:
                    urlBase = urlBase + str(location.getLat()) + ',' + str(location.getLng())
                count = count+1
            urlBase = urlBase + '&interpolate=true&key='+self.ApiKey

            #call the google roads api
            roadsApiRequest = requests.get(urlBase)

            #returned snapped points
            arrayOfSnappedPoints = roadsApiRequest.json()['snappedPoints']

            #build our latlng object using the results from google roads api
            for snappedLocation in arrayOfSnappedPoints:
                newSnappedLatLng = LatLng(snappedLocation['location']['latitude'], snappedLocation['location']['longitude'])
                newSnappedLatLngJson = json.dumps(newSnappedLatLng.__dict__)
                self.listSnappedLocationsJson.append(newSnappedLatLngJson)

        return self.listSnappedLocationsJson

    #used for splitting the list
    def splitList(self, alist, wantedParts):
        length = len(alist)
        return [alist[i * length // wantedParts: (i + 1) * length // wantedParts]
                for i in range(wantedParts)]

    #count how many splits does the main list needs to meet the limit
    def getSplitCount(self, list):
        return math.ceil(len(list)/self.Limit)

    #get distance between geo points using vincenty
    def getDistance(self, fromLatlng, toLatLng):
        fr = ( fromLatlng.getLat() , fromLatlng.getLng() )
        to = ( toLatLng.getLat() , toLatLng.getLng() )
        return vincenty(fr, to, miles=True)

    #filter out those raw points which are lower than 0.001 mile
    def filterClosePoints(self, listOfLatLng):
        filteredList = []
        count =0
        for location in listOfLatLng:

            if count==0:
                filteredList.append(location)
            else:
                if(self.getDistance(listOfLatLng[count], listOfLatLng[count-1]) >0.001):
                    filteredList.append(location)

            count = count+1

        return filteredList

