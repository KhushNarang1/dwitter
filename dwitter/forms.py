from django import forms
from .models import Dweet, Comment, DweetCategory

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
    
    categories = forms.ModelMultipleChoiceField(
        queryset = DweetCategory.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        required = True,
        label = "Categories",
    )
    

    class Meta:
        model = Dweet # explains which model is associated with the class
        exclude = ("user","likes" )

class CommentForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        widget = forms.widgets.Textarea(
            attrs = {
                "placeholder" : "Comment Something...",
                "class" : "textarea is-success is-medium",
            }
        ),
        label = "",
        )

    class Meta:
        model = Comment # explains which model is associated with the class
        exclude = ("user","dweet" )

class SearchForm(forms.Form):
    search_query = forms.CharField(label='Search by Name', max_length=100)
