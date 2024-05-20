from django import forms


class RouteForm(forms.Form):
    source      = forms.CharField(label='', help_text='source')
    destination = forms.CharField(label='', help_text='destination')

    class Meta:
        fields = [
            'source',
            'destination'
        ]
