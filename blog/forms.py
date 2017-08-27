from django import forms
from .models import Post
from pagedown.widgets import PagedownWidget
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
	dis = forms.CharField(widget=PagedownWidget(show_preview=False))
	class Meta:
		model = Post
		fields = [
			"title",
			"Type",
			"company",
			"case",
			"dis",
			"image",
			"image1",
			"image2",
			"price",
			"city",
			"address",
			"draft",
		]


class ContactForm(forms.Form):
	contact_name = forms.CharField(required=True)
	contact_email = forms.EmailField(required=True)
	content = forms.CharField(
	    required=True,
	    widget=forms.Textarea
	)
	def __init__(self, *args, **kwargs):
		super(ContactForm, self).__init__(*args, **kwargs)
		self.fields['contact_name'].label = "Your name:"
		self.fields['contact_email'].label = "Your email:"
		self.fields['content'].label = "What do you want to say?"

class BuyForm(forms.Form):
	code_name = forms.CharField(required=True)
	buy_number = forms.CharField(required=True)
	card_expiry_date = forms.DateTimeField(required=True)
	# card_expiry_date2 = forms.CharField(required=True)
	card_Cvv = forms.CharField(required=True)

	def __init__(self, *args, **kwargs):
		super(BuyForm, self).__init__(*args, **kwargs)
		self.fields['code_name'].label = "Your Name"
		self.fields['buy_number'].label = "Your Card Number"
		self.fields['card_expiry_date'].label = "Card Expiry Date"
		self.fields['card_Cvv'].label = "Card CVV"



class EditProfileForm(UserChangeForm):
	class Meta:
		model = User
		fields=(
			"email",
			"first_name",
			"last_name",
			"password"
			)


# class ContactForm(forms.Form):
# 	from_email = forms.EmailField(required=True)
# 	subject = forms.CharField(required=True)
# 	message = forms.CharField(widget=forms.Textarea)