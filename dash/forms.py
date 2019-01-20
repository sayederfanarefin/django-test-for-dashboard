from django.db import models
from django import forms

class DocumentForm(forms.Form):

    docfile = forms.FileField(

        label='Select a file',

        help_text='Upload a json file with geo co ordinatees'
    )