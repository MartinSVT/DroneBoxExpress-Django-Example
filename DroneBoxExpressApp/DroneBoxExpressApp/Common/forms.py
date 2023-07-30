from django import forms
from DroneBoxExpressApp.Common.models import NewsModel


class NewsAddForm(forms.ModelForm):
    class Meta:
        model = NewsModel
        fields = ["article_title", "article_content"]
