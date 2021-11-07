from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Book

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class NewBookForm(forms.Form):

	class Meta:
		model = Book
		fields = ('Title','Author First Name','Author Last Name','Publisher',
		'Publication Date','Book Cover','Genre', 'Synopsis')
		
	
	