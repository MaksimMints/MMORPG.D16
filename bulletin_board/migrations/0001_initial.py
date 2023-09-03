# Generated by Django 4.2.4 on 2023-08-30 21:03

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bulletin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('tanks', 'Танки'), ('hils', 'Хилы'), ('dd', 'ДД'), ('merchant', 'Торговцы'), ('guildmas', 'Гилдмастеры'), ('questgiv', 'Квестгиверы'), ('smith', 'Кузнецы'), ('leathers', 'Кожевники'), ('potion', 'Зельевары'), ('spellmas', 'Мастера заклинаний')], default='tanks', max_length=8, verbose_name='Категория')),
                ('title', models.CharField(max_length=128, verbose_name='Название')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Содержание')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('respText', models.TextField()),
                ('status_no', models.BooleanField(default=False, verbose_name='Статус отклика - отклонен')),
                ('status_ok', models.BooleanField(default=False, verbose_name='Статус отклика - принят')),
                ('respAuthor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор отклика')),
                ('respBulletin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bulletin_board.bulletin')),
            ],
        ),
    ]