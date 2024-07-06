from django import forms 
from .models import Contact, Comment
from django_recaptcha.fields import ReCaptchaField 
from django_recaptcha.widgets import ReCaptchaV2Checkbox 
     
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
        captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox) 

class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message']