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
        article_placeholder = '''       Start writing Your Article Here
        
        How to Format!
        ## for Heading
        ### for subheading

        Example 

        ## how to bake
        ### Start here
        ### follow the list
        1. item 1
        2. item 3
        3. item 3
        '''
        self.fields['title'].widget.attrs['placeholder'] = 'The Title'
        self.fields['detail'].widget.attrs['placeholder'] = article_placeholder


class MetaTagForm(forms.ModelForm):
    meta_description = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Post
        fields = [
            "meta_description",
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['meta_description'].widget.attrs['placeholder'] = "Enter Short Description. Less than 160 Characters"

class ReviewForm(forms.ModelForm):
    title = forms.CharField()
    meta_description = forms.CharField(widget=forms.Textarea)
    detail = forms.CharField(widget=PagedownWidget())
    # tags = forms.ModelMultipleChoiceField(queryset = taggers.objects.all(), widget=forms.CheckboxSelectMultiple())
    class Meta:
        model = Post
        fields = [
            "title",
            "meta_description",
            "detail",
            "publish",
            # "tags"
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        article_placeholder = '''       Start writing Your Article Here
        
        How to Format!
        ## for Heading
        ### for subheading

        Example 

        ## how to bake
        ### Start here
        ### follow the list
        1. item 1
        2. item 3
        3. item 3
        '''
        self.fields['title'].widget.attrs['placeholder'] = 'The Title'
        self.fields['detail'].widget.attrs['placeholder'] = article_placeholder
        self.fields['meta_description'].widget.attrs['placeholder'] = "Enter Short Description. Less than 160 Characters"

