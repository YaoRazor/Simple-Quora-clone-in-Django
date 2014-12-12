from django.contrib.auth.models import User
from django import forms

class RegistrationForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=30)
    email = forms.EmailField(min_length=3, max_length = 30)
    password1 = forms.CharField(min_length=6, max_length=30,label="Password", widget=forms.PasswordInput())
    password2 = forms.CharField(min_length=6, max_length=30,label="Confirm password",widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2:
            if password1 != password2:
                msg = 'Passwords must match'
                self._errors['password1'] = self.error_class([msg])
                self._errors['password2'] = self.error_class([msg])

                del cleaned_data['password1']
                del cleaned_data['password2']

        username = cleaned_data.get('username')
        if username:
            userExists = True
            try:
                User.objects.get(username=username)
            except User.DoesNotExist:
                userExists = False
            if userExists:
                msg = 'That username is already taken'
                self._errors['username'] = self.error_class([msg])
                del cleaned_data['username']


        return cleaned_data

    def save(self, commit=True):
        g = self.clean()
        user = User.objects.create_user(g['username'],g['email'],g['password1'])
        if commit: user.save()
        return user


    class Meta:
        model = User
        fields = {}


class LoginForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=30)
    password = forms.CharField(min_length=3, max_length=30, widget=forms.PasswordInput())
