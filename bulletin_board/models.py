from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from ckeditor_uploader.fields import RichTextUploadingField


class Bulletin(models.Model):
    TYPE = (
        ('tanks', 'Танки'),
        ('hils', 'Хилы'),
        ('dd', 'ДД'),
        ('merchant', 'Торговцы'),
        ('guildmas', 'Гилдмастеры'),
        ('questgiv', 'Квестгиверы'),
        ('smith', 'Кузнецы'),
        ('leathers', 'Кожевники'),
        ('potion', 'Зельевары'),
        ('spellmas', 'Мастера заклинаний'),
    )
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Пользователь')
    category = models.CharField(max_length=8, choices=TYPE, default='tanks', verbose_name='Категория')
    title = models.CharField(max_length=128, verbose_name='Название')
    content = RichTextUploadingField(verbose_name='Содержание')
    dateCreationn = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.title.title()}'

    def get_absolute_url(self):
        return reverse('bulletin_detail', args=[str(self.id)])


# модель отклика
class Response(models.Model):
    respAuthor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор отклика')
    respBulletin = models.ForeignKey(Bulletin, on_delete=models.CASCADE)
    respText = models.TextField()
    status_no = models.BooleanField(default=False, verbose_name='Статус отклика - отклонен')
    status_ok = models.BooleanField(default=False, verbose_name='Статус отклика - принят')

    def __str__(self):
        return f'{self.user}'
