from typing import Any
from django import forms
from django.contrib.auth.models import User
from . import models


class ProfileForm(forms.ModelForm):
    birth_date = forms.DateField(
        input_formats=['%d/%m/%Y'], 
        widget=forms.DateInput(format='%d/%m/%Y'))

    class Meta:
        model = models.Profile
        exclude = ('user',)
    

class UserForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
    )
    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Confirm password'
    )
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = user

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'password2'
            )
        
    def clean(self):
        data = self.data
        cleaned = self.cleaned_data
        validation_error_msgs = {}

        user_data = cleaned.get('username')
        password_data = cleaned.get('password')
        password2_data = cleaned.get('password2')
        email_data = cleaned.get('email')

        existing_user = User.objects.filter(username=user_data).first()
        existing_email = User.objects.filter(email=email_data).first()

        required_field_error = 'Este campo é obrigatório. '
        existing_user_error = 'Este usuário já está cadastrado.'
        existing_email_error = 'Este email já está cadastrado.'
        unmatched_passwords_error = 'As senhas informadas não são iguais.'
        short_password_error = 'Sua senha deve conter pelo menos 6 caracteres.'

        # Logged user
        if self.user:
            if existing_user:
                if user_data == existing_user.username and user_data != self.user.username:
                    validation_error_msgs['username'] = existing_user_error

            if existing_email:
                if email_data == existing_email.email and email_data != self.user.email:
                    validation_error_msgs['email'] = existing_email_error

            if password_data:
                if password_data != password2_data:
                    validation_error_msgs['password'] = unmatched_passwords_error
                    validation_error_msgs['password2'] = unmatched_passwords_error

                if len(password_data) < 6:
                    validation_error_msgs['password'] = short_password_error

    
        # Not logged user
        else:

            if not user_data:
                validation_error_msgs['username'] = required_field_error

            if not email_data:
                validation_error_msgs['email'] = required_field_error

            if not password_data:
                validation_error_msgs['password'] = required_field_error

            if not password2_data:
                validation_error_msgs['password2'] = required_field_error

            if existing_user:
                validation_error_msgs['username'] = existing_user_error

            if existing_email:
                validation_error_msgs['email'] = existing_email_error

            if password_data != password2_data:
                validation_error_msgs['password'] = unmatched_passwords_error
                validation_error_msgs['password2'] = unmatched_passwords_error

            if len(password_data) < 6 and password_data:
                validation_error_msgs['password'] = short_password_error


            if validation_error_msgs:
                raise(forms.ValidationError(validation_error_msgs))


