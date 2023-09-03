from django import forms
from .models import Bulletin, Response


class BulletinForm(forms.ModelForm):
    class Meta:
        model = Bulletin
        fields = [
            'title',
            'content',
            'category',
        ]


class DetailFormWithResponse(forms.ModelForm):
    """Форма создания отклика"""

    class Meta:
        model = Response
        fields = ['respText', ]
