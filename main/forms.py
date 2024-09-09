from django import forms
from main.models import RequestDetails

class EditRequestForm(forms.ModelForm):
    class Meta:
        model = RequestDetails
        exclude = ['request']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['meal'].widget.attrs.update({
            'class': 'form-control',
            'require':'true' ,
            'placeholder': 'Enter text here',  
        })
        self.fields['meal'].widget.attrs.update({

            'class': 'form-control',
            'require':'true' ,
            'placeholder': 'Enter additional information',
            'rows': 4,  
        })
