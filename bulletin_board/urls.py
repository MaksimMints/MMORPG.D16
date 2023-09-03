from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# Импортируем созданное нами представление
from .views import (
   BulletinList, BulletinDetail, BulletinCreate, BulletinUpdate, ResponseList, ResponseRemove, ResponseAccept
)


urlpatterns = [
    path('', BulletinList.as_view(), name='bulletins_list'),
    path('<int:pk>', BulletinDetail.as_view(), name='bulletin_detail'),
    path('bulletin/create/', BulletinCreate.as_view(), name='bulletin_create'),
    path('bulletin/<int:pk>/edit', BulletinUpdate.as_view(), name='bulletin_edit'),
    path('ckeditor', include('ckeditor_uploader.urls')),
    path('response/', ResponseList.as_view(), name='response'),
    path('response_accept/<int:pk>', ResponseAccept.as_view(), name='accept'),
    path('response_remove/<int:pk>', ResponseRemove.as_view(), name='remove'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
