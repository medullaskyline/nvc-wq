from wq.db import rest
from django.contrib.auth.models import User

from .models import Feeling, Need, FeelingsNeedsEntry
from .views import FeelingsNeedsEntryViewSet
from .serializers import FeelingsNeedsEntrySerializer


def filter_entries(queryset, request):
    """entries will only be viewable by the user who entered them. except superusers can see all"""
    if request.user.is_superuser:
        return queryset
    return queryset.filter(user_id=request.user.id)


def filter_users(queryset, request):
    """entries will only be viewable by the user who entered them. except superusers can see all"""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return queryset
        return queryset.filter(pk=request.user.id)
    return queryset.filter(pk=0)

'''
 register_model has parameters
 viewset=None, serializer=None, fields=None, queryset=None, filter=None, cache_filter=None
 url=[Model]._meta.verbose_name_plural
 queryset=[Model].objects.all()
 serializer=wq.db.rest.serializers.ModelSerializer -- one of fields or serializer must be set
 # todo: custom serializer so Public can be a boolean
 and add boolean to serializer's xlsformtypes: OrderedDict([(<class 'rest_framework.fields.ImageField'>, 'image'), (<class 'rest_framework.fields.FileField'>, 'binary'), (<class 'rest_framework.fields.DateField'>, 'date'), (<class 'rest_framework.fields.DateTimeField'>, 'dateTime'), (<class 'rest_framework.fields.FloatField'>, 'decimal'), (<class 'wq.db.rest.serializers.GeometryField'>, 'geoshape'), (<class 'rest_framework.fields.IntegerField'>, 'int'), (<class 'rest_framework.fields.CharField'>, 'string'), (<class 'rest_framework.fields.ChoiceField'>, 'select one'), (<class 'rest_framework.fields.TimeField'>, 'time')])
or filter with custom filtering function
'''
rest.router.register_model(
    Feeling,
    fields="__all__",
)
rest.router.register_model(
    Need,
    fields="__all__",
)
rest.router.register_model(
    FeelingsNeedsEntry,
    fields="__all__",
    viewset=FeelingsNeedsEntryViewSet,
    filter=filter_entries,
    cache_filter=filter_entries,  # wq configuration
    my_custom_flag=True,  # Custom configuration
    serializer=FeelingsNeedsEntrySerializer,
)
rest.router.register_model(
    User,
    fields="__all__",
    filter=filter_users,
    cache_filter=filter_users,
    # my_custom_flag=True,  # Custom configuration
    lookup="username",
)


