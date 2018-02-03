from wq.db import rest
from django.contrib.auth.models import User

from .models import FeelingLeaf, NeedLeaf, Entry, FeelingSubCategory, FeelingMainCategory, NeedCategory
from .serializers import UserSerializer, EntrySerializer, FeelingMainCategorySerializer, FeelingSubCategorySerializer

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
        # fields="__all__",
        serializer=FeelingMainCategorySerializer,
        # children=[{
        #     "name": "feelingsubcategory",
        #     "label": "FeelingSubCategory",
        #     "bind": {
        #         "required": True
        #     },
        #     "type": "string",
        #     "wq:ForeignKey": "feelingsubcategory"
        # }],
        cache="all",
)
rest.router.register_model(
        FeelingSubCategory,
        fields="__all__",
        serializer=FeelingSubCategorySerializer,
        # children=[{
        #     "name": "feelingleaf",
        #     "label": "FeelingLeaf",
        #     "bind": {
        #         "required": True
        #     },
        #     "type": "string",
        #     "wq:ForeignKey": "feelingleaf"
        # }],
        cache="all",
        list=False,
)
rest.router.register_model(
        FeelingLeaf,
        # serializer=FeelingLeafSerializer,
        fields="__all__",
        cache="all",
        list=False,
)
rest.router.register_model(
        NeedCategory,
        fields="__all__",
        children=[{
            "name": "needleaf",
            "label": "Need Leaf",
            "bind": {
                "required": True
            },
            "type": "string",
            "wq:ForeignKey": "needleaf"
        }],
        cache="all",
)
rest.router.register_model(
        NeedLeaf,
        fields="__all__",
        cache="all",
        list=False,
)
rest.router.register_model(
        Entry,
        # fields="__all__",
        filter=filter_entries,
        cache_filter=filter_entries,
        my_custom_flag=True,
        serializer=EntrySerializer,
        cache="all",
)

"""
deprecated older models
"""
# rest.router.register_model(
#         Feeling,
#         fields="__all__",
# )
# rest.router.register_model(
#         Need,
#         fields="__all__",
# )
# rest.router.register_model(
#         FeelingsNeedsEntry,
#         fields="__all__",
#         viewset=FeelingsNeedsEntryViewSet,
#         filter=filter_entries,
#         cache_filter=filter_entries,
#         my_custom_flag=True,
#         serializer=FeelingsNeedsEntrySerializer,  # this just specifies that public is a choice field
# )
