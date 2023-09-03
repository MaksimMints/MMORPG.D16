from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Response, Bulletin


@receiver(post_save, sender=Response)
def send_msg(instance, created, **kwargs):
    """функция-сигнал, которая срабатывает, когда в модель Response (отклики) вносятся изменения
    если создается новая запись (if created), то автору объявления отправляется письмо-уведомление,
    если автор объявления принимает отклик (elif instance.status_add), то автору отклика идет письмо"""
    user = User.objects.get(pk=instance.respAuthor_id)
    pk_response = instance.id
    if created:

        pk_note = instance.respBulletin_id
        user = f'{user.first_name}'
        user_id = Bulletin.objects.get(pk=pk_note).user_id
        bull_title = Bulletin.objects.get(pk=pk_note).title
        response_text = Response.objects.get(pk=pk_response).respText

        # формирование письма автору объявления
        title = f'У вас новый отклик от {str(user)[:15]}'
        msg = f'На ваше объявление "{bull_title}" пришел новый отклик\n' \
              f'от {user} следующего содержания: ' \
              f'{response_text}. Перейти в отклики http://127.0.0.1:8000/bulletin_board/response/'
        email = 'forsendfromNP@yandex.ru'
        bull_email = User.objects.get(pk=user_id).email

        send_mail(subject=title, message=msg, from_email=email, recipient_list=[bull_email, ])

    elif instance.status_ok:
        # если отклик принят, то автору отклика отправить письмо-уведомление

        bull_title = Bulletin.objects.get(pk=Response.objects.get(pk=pk_response).respBulletin_id).title
        bull_id = Bulletin.objects.get(pk=Response.objects.get(pk=pk_response).respBulletin_id).id

        title = f'У вас одобренный отклик'
        msg = f'На ваш отклик на объявление "{bull_title}" пришло положительное ' \
              f'подтверждение. Перейти на объявление http://127.0.0.1:8000/bulletin_detail/{bull_id}'
        email = 'forsendfromNP@yandex.ru'
        resp_email = User.objects.get(pk=Response.objects.get(pk=pk_response).respAuthor_id).email

        send_mail(subject=title, message=msg, from_email=email, recipient_list=[resp_email, ])
