from django import forms


class PsnSignInForm(forms.Form):
    npsso = forms.CharField(
        max_length=64,
        min_length=64,
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Enter NPSSO token'})
    )
