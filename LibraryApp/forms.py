from django import forms
from . models import *
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm

class UsForm(UserCreationForm):
	password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control my-2","placeholder":"Enter Password"}))
	password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control my-2","placeholder":"Enter Confirm Password"}))
	class Meta:
		model = User
		fields = ["username","eid",'email']
		widgets = {
		"username":forms.TextInput(attrs={
			"class":"form-control my-2",
			"placeholder":"Enter Username",
			}),
		"eid":forms.TextInput(attrs={
			"class":"form-control my-2",
			"placeholder":"Enter Unique Id",
			}),
			"email":forms.EmailInput(attrs={
			"class":"form-control my-2",
			"placeholder":"Enter Mail Id",
			}),
		}

class StdForm(forms.ModelForm):
	
	class Meta:
		model = StdProfile
		fields = ["sage","sgen","sbranch","syear"]
		widgets = {
		"sage":forms.NumberInput(attrs={
			"class":"form-control my-2",
			"placeholder":"Enter Your age",
			}),
		"sgen":forms.Select(attrs={
			"class":"form-control my-2",
			}),
		"sbranch":forms.Select(attrs={
			"class":"form-control my-2",
			}),
		"syear":forms.Select(attrs={
			"class":"form-control my-2",
			}),
		}

class TeacherForm(forms.ModelForm):
	
	class Meta:
		model = TeacherProfile 
		fields = ['tage','tgen','tbranch','texpr','tdesg']
		widgets = {
			"tage" : forms.NumberInput(attrs={
				'class' : 'form-control my-2',
				'placeholder' : 'Enter Age',
			}),
			"tgen" : forms.Select(attrs={
				'class' : 'form-control my-2'
			}),
			"tbranch" : forms.Select(attrs={
				'class' : 'form-control my-2'
			}),
			"texpr" : forms.NumberInput(attrs={
				'class' : 'form-control my-2',
				'placeholder' : 'Enter Experence',
			}),
			"tdesg" : forms.TextInput(attrs={
				'class' : 'form-control my-2',
				'placeholder' : 'Enter Desegnation',
			}),

		}

class AddBookForm(forms.ModelForm):
	
	class Meta:
		model = BookAdd
		fields = ['btitle','bauthor','bedition','bdes','num_copies','bdept']
		widgets = {
			"btitle" : forms.TextInput(attrs={
				"class" : "form-control my-2",
				"placeholder" : "Enter Booktitle",
			}),
			"bauthor" : forms.TextInput(attrs={
				"class" : "form-control my-2",
				"placeholder" : "Enter AuthorName",
			}),
			"bedition" : forms.TextInput(attrs={
				"class" : "form-control my-2",
				"placeholder" : "Edition no",
			}),
			"bdes" : forms.Textarea(attrs={
				"class" : "form-control my-2",
				"placeholder" : "Enter Discription of the book",
				"rows" : 4,
				"cols" : 10,

				
			}),
			"bdept" : forms.Select(attrs={
				'class' : 'form-control my-2'
			}),
			"num_copies" : forms.NumberInput(attrs={
				'class' : 'form-control my-2',
				'placeholder' : 'Enter No.of Copies'
				}),


		}
