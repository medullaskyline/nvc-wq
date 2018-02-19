from wq.db import rest
from django.contrib.auth.models import User

from .models import FeelingLeaf, NeedLeaf, Entry, FeelingSubCategory, FeelingMainCategory, NeedCategory
from .serializers import UserSerializer, EntrySerializer, FeelingMainCategorySerializer, FeelingSubCategorySerializer, NeedCategorySerializer, NeedLeafSerializer
from .views import NoDetailViewset

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

def filter_need_leaves(queryset, request):
    """entries will only be viewable by the user who entered them. except superusers can see all"""
    print(queryset)
    print(request)
    return queryset
    # return queryset.filter(need_category_id=request.get)

rest.router.register_model(
        User,
        fields=['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'last_login', 'date_joined'],
        filter=filter_users,
        cache_filter=filter_users,
        my_custom_flag=True,
        lookup="username",
        can_add=False,
        serializer=UserSerializer,
)

rest.router.register_model(
        FeelingMainCategory,
        serializer=FeelingMainCategorySerializer,
        cache="all",
)
rest.router.register_model(
        FeelingSubCategory,
        serializer=FeelingSubCategorySerializer,
        cache="all",
        viewset=NoDetailViewset,
)
rest.router.register_model(
        FeelingLeaf,
        fields="__all__",
        cache="all",
        viewset=NoDetailViewset,
)
rest.router.register_model(
        NeedCategory,
        fields="__all__",
        cache="all",
        serializer=NeedCategorySerializer,

)

rest.router.register_model(
        NeedLeaf,
        fields="__all__",
        cache="all",
        list=False,
        modes=['list'],
        viewset=NoDetailViewset,
)
rest.router.register_model(
        Entry,
        filter=filter_entries,
        cache_filter=filter_entries,
        my_custom_flag=True,
        serializer=EntrySerializer,
        cache="all",
)