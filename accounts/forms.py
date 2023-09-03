from random import randint

from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.template.loader import render_to_string


class UserForm(UserCreationForm):
    """Форма изменения данных пользователя"""

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "email",
                  "password1",
                  "password2",)


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="First Name")

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "email",
            "password1",
            "password2",
        )

    @staticmethod
    def send_code_conf(user, number):
        html_content = render_to_string(
            'registration/conf_email.html',
            {
                'user': user,
                'link': f'{settings.SITE_URL}/accounts/{user.id}/confirmation_signup/',
                'number': number,
            }
        )
        msg = EmailMultiAlternatives(
            subject=f"Код подтверждения email",
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        number = randint(100, 999)
        cache.set(f'code-{user.pk}', number, timeout=300)
        self.send_code_conf(user, number)
        return user


class ConfirmationSignUpForm(forms.ModelForm):
    code = forms.IntegerField()

    class Meta:
        model = User
        fields = ['username',
                  'code',
                  ]

    def clean(self):
        cleaned_data = super().clean()
        username, code = cleaned_data.get('username'), cleaned_data.get('code')
        user = User.objects.get(username=username)
        number = cache.get(f'code-{user.pk}', None)
        if code == number:
            cleaned_data['user'] = user
        else:
            raise ValidationError({
                'code': 'Введен неправильный код или срок действия кода истек. Повторите регистрацию.',
            })
        return cleaned_data