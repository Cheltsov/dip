from django import forms
from .models import Doc
from client.models import Client

class DocClientForm(forms.ModelForm):
    title = forms.CharField(required=True, label="Название")
    file = forms.FileField(label="Файл")
    client = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Doc
        fields = ['title', 'file', 'crypth']
        exclude = ['client', 'date_created', 'date_updated', 'active', 'decrypth']

class DocAdminForm(forms.ModelForm):
    title = forms.CharField(required=True, label="Название")
    file = forms.FileField(label="Файл")
    client = forms.ModelChoiceField(queryset=Client.objects.filter(active=1).order_by('fio'), label="Клиент")

    class Meta:
        model = Doc
        fields = ['title', 'file', 'crypth', 'client']
        exclude = ['date_created', 'date_updated', 'active']
