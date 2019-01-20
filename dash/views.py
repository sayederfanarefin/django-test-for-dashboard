from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.urls import reverse

from dash.models import Document
from dash.forms import DocumentForm

from dash.Services import ServiceLatLng
import json
# Create your views here.

def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()
            serviceLatLng = ServiceLatLng(newdoc)


        return render(request, 'maps.html', {'rawDataVar': serviceLatLng.getRawLocation(), 'snappedDataVar': serviceLatLng.getSnappedLocation()})
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()


    # Render list page with the documents and the form
    return render(request, 'list.html', { 'form': form})

