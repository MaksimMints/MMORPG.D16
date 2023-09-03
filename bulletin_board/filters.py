from django_filters import FilterSet

from .models import Bulletin, Response


class NoteFilter(FilterSet):
    class Meta:
        model = Bulletin
        fields = ('user', 'category',)


class ResponseFilter(FilterSet):
    class Meta:
        model = Response
        fields = ('respBulletin',)
