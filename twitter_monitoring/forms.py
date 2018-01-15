from django import forms

MY_CHOICES = (
    ('del', 'Delete follower'),
    ('add', 'Add follower'),
)

class LoginForm(forms.Form):
    user_name = forms.CharField(label='User name', max_length=40,
                                widget=forms.TextInput(attrs={'class': 'col-12 form-control'}))
    user_pass = forms.CharField(label='Password', max_length=40,
                                widget=forms.PasswordInput(attrs={'class': 'col-12 form-control'}))


class RegForm(forms.Form):
    user_name = forms.CharField(label='User name', max_length=40,
                                widget=forms.TextInput(attrs={'class': 'col-12 form-control', 'placeholder': 'User name'}))
    user_pass = forms.CharField(label='Password', max_length=40,
                                widget=forms.PasswordInput(attrs={'class': 'col-12 form-control', 'placeholder': 'Pasword'}))
    user_rep_pass = forms.CharField(label='Repeat password', max_length=40,
                                    widget=forms.PasswordInput(
                                        attrs={'class': 'col-12 form-control', 'placeholder': 'Repeat pasword'}))
    user_email = forms.CharField(label='Email', max_length=60,
                                 widget=forms.EmailInput(attrs={'class': 'col-12 form-control', 'placeholder': 'Email'}))


class Search(forms.Form):
    search_input = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'class': 'col-12 form-control', 'placeholder': 'Search screen name'}))
    action = forms.ChoiceField(required=False, choices=MY_CHOICES, widget=forms.Select())