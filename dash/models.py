from django.db import models

import os

# Create your models here.
class Document(models.Model):
    uploadTo = 'uploads'
    docfile = models.FileField(upload_to=uploadTo)

    def filename(self):
        return 'uploads/'+os.path.basename(self.docfile.name)


class LatLng():
    lat = None
    lng = None

    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng

