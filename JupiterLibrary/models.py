from django.db import models
from PIL import Image

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    authorFirstName = models.CharField('Author First Name',max_length=50)
    authorLastName = models.CharField('Author Last Name',max_length=50)
    publisher = models.CharField(max_length=30)
    date = models.DateField()
    image = models.ImageField(upload_to='images/')
    genre = models.TextField()
    synopsis = models.TextField()
    numberAvailable = models.PositiveBigIntegerField('Number Available')
    numberBorrowed = models.PositiveBigIntegerField('Number Borrowed')

    def save(self):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 475 or img.width > 300:
            new_img = (300,475)
            img.thumbnail(new_img)
            img.save(self.image.path)

class BorrowedBook(models.Model):
    username = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    days = models.IntegerField()

class UserInfo(models.Model):
    username = models.CharField(max_length=100)
    fName = models.CharField(max_length=100)
    lName = models.CharField(max_length=100)
    bio = models.TextField()
    email = models.EmailField()
    

