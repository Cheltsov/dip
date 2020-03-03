from django import forms
from .models import Adminer

class AdminerForm(forms.ModelForm):

    class Meta:
        model = Adminer
        fields = "__all__"
