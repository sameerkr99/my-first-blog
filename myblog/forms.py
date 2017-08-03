from django import forms
from .models import Post, comments
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class loginForm(forms.Form):
	userName = forms.CharField()
	passWord = forms.CharField()

class postForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title', 'text',)
	def __init__(self, *args, **kwargs):
		super(postForm, self).__init__(*args, **kwargs)
		self.fields['title'].required = True
		self.fields['text'].required = True
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({'class': 'form-control'})

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
    def __init__(self, *args, **kwargs):
    	super(SignUpForm, self).__init__(*args, **kwargs)
    	for field in iter(self.fields):
    		self.fields[field].widget.attrs.update({'class': 'form-control'})
