from django import forms
from .models import Post, catagories
from pagedown.widgets import PagedownWidget

class BlogForm(forms.ModelForm):
    title = forms.CharField()
    detail = forms.CharField(widget=PagedownWidget())
    # tags = forms.ModelMultipleChoiceField(queryset = taggers.objects.all(), widget=forms.CheckboxSelectMultiple())
    class Meta:
        model = Post
        fields = [
            "title",
            "detail",
            # "tags"
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['placeholder'] = 'The Title'
        self.fields['detail'].widget.attrs['placeholder'] = 'The Article'
