from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    authorFirstName = models.CharField(max_length=50)
    authorLastName = models.CharField(max_length=50)
    publisher = models.CharField(max_length=30)
    publicationDate = models.DateField()
    image = models.ImageField(upload_to='images/')
    genre = models.TextField()
    synopsis = models.TextField()

