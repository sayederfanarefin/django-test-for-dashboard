from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.urls import reverse

from dash.models import Document
from dash.forms import DocumentForm
from dash.models import latLng
import json
# Create your views here.

def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()
            listRawLocations = []
            with open(newdoc.filename()) as f:
                for x in json.load(f):
                    newLatLng = latLng (x['latitude'], x['longitude'])
                    newLatLngJson = json.dumps(newLatLng.__dict__)
                    listRawLocations.append(newLatLngJson)

            # Redirect to the document list after POST
            #listRawLocationsJson = json.dumps(listRawLocations)
        return render(request, 'maps.html', {'rawDataVar': listRawLocations})
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()


    # Render list page with the documents and the form
    return render(request, 'list.html', { 'form': form})

