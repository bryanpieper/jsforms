from django import forms


class TestForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(TestForm, self).__init__(*args, **kwargs)
        self.fields['slug'].required = False
        self.fields['hidden'].required = False
    
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    slug = forms.SlugField()
    hidden = forms.CharField(widget=forms.HiddenInput())
