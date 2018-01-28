from wq.db import rest
from django.contrib.auth.models import User

from .models import Feeling, Need, FeelingsNeedsEntry
from .serializers import FeelingsNeedsEntrySerializer, user_form
from .views import FeelingsNeedsEntryViewSet


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
    viewset=FeelingsNeedsEntryViewSet, # disabling bc it doesn't prevent ppl from adding entries with other ppl's user ids
    filter=filter_entries,
    cache_filter=filter_entries,  # wq configuration
    my_custom_flag=True,  # Custom configuration
    serializer=FeelingsNeedsEntrySerializer,  # this just specifies that public is a boolean
)
rest.router.register_model(
    User,
    fields=['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'last_login', 'date_joined'],
    filter=filter_users,
    cache_filter=filter_users,
    my_custom_flag=True,
    lookup="username",
    can_add=False,
    form=user_form,
)



