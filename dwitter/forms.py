from django import forms
from .models import Dweet

class DweetForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        widget = forms.widgets.Textarea(
            attrs = {
                "placeholder" : "Dweet Something...",
                "class" : "textarea is-success is-medium",
            }
        ),
        label = "",
        )

    class Meta:
        model = Dweet # explains which model is associated with the class
        exclude = ("user", )

class SearchForm(forms.Form):
    search_query = forms.CharField(label='Search by Name', max_length=100)
