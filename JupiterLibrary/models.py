from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=50)
    authorFirstName = models.CharField(max_length=50)
    authorLastName = models.CharField(max_length=50)
    publisher = models.CharField(max_length=30)
    publicationData = models.DateField()
    image = models.ImageField()
    genre = models.TextField()
    synopsis = models.TextField()

