from django.forms import ModelForm #kljucno za izradu formi
from .models import Predmet, Korisnik, Upisi #importam svoje modele
from django.contrib.auth.hashers import make_password #za password 
from django.contrib.auth.forms import UserCreationForm
from django import forms




class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Korisnik
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            self.add_error('password_confirm', 'Passwords do not match')

        return cleaned_data
    

class KorisnikForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Korisnik
        fields = ['username', 'email', 'password','role','status']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
#__init__ je zapravo konstruktor kojem dajem *args i **kwargs jer nez kolko argumenata ce primit
class PredmetiForm(ModelForm): #nasljeduje iz ModelForm
    def __init__(self, *args, **kwargs):
        super(PredmetiForm, self).__init__(*args, **kwargs)
        self.fields.get('nositelj').queryset = Korisnik.objects.filter(role='prof')

    class Meta:
        model = Predmet
        fields = '__all__'

class UpisiForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UpisiForm, self).__init__(*args, **kwargs)
        self.fields.get('student_id').queryset = Korisnik.objects.filter(role='stu')

    class Meta:
        model = Upisi
        fields = '__all__'

class PredmetProfesoruForm(forms.Form):
    predmet = forms.ModelChoiceField(queryset=Predmet.objects.all())
    profesor = forms.ModelChoiceField(queryset=Korisnik.objects.filter(role='prof'))

class UpisForm(ModelForm):
    class Meta:
        model = Upisi
        fields = ['predmet', 'status']
