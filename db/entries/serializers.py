from wq.db.rest.serializers import ModelSerializer
from wq.db.patterns import serializers as patterns
from rest_framework import serializers
from rest_framework.utils import model_meta

from .models import (FeelingLeaf, NeedLeaf, Entry, FeelingSubCategory, FeelingMainCategory,
                     NeedCategory)


class FeelingLeafSerializer(ModelSerializer):
    class Meta:
        model = FeelingLeaf
        fields = ('feeling_leaf',)


class FeelingSubCategorySerializer(ModelSerializer):
    feeling_leaves = FeelingLeafSerializer(read_only=True, many=True)

    class Meta:
        model = FeelingSubCategory
        fields = ('feeling_sub_category', 'feeling_leaves')


class FeelingMainCategorySerializer(ModelSerializer):
    feeling_leaves = FeelingLeafSerializer(read_only=True, many=True)
    feeling_sub_categories = FeelingSubCategorySerializer(read_only=True, many=True)

    class Meta:
        model = FeelingMainCategory
        fields = ('feeling_main_category', 'feeling_sub_categories', 'feeling_leaves')


class EntrySerializer(ModelSerializer):
    # feeling_main_category = FeelingMainCategorySerializer(read_only=True)
    # serializer = BookSerializer(queryset, many=True)

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        # user = self.context.get('request').user

    class Meta:
        fields = "__all__"  #('feeling_main_category',)
        wq_field_config = {
            'public': {'type': 'select one'},
            # 'feeling_main_category': {
            #     "children": [
            #         {
            #             "name": "feeling_sub_category",
            #             "label": "FeelingSubCategory",
            #             "bind": {
            #                 "required": True
            #             },
            #             "type": "string",
            #             "wq:ForeignKey": "feeling_sub_category"
            #         },
            #         {
            #             "name": "feeling_leaf",
            #             "label": "FeelingLeaf",
            #             "bind": {
            #                 "required": True
            #             },
            #             "type": "string",
            #             "wq:ForeignKey": "FeelingLeaf"
            #         },
            #     ],
            # }
        }


'''
class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ('order', 'title', 'duration')

class AlbumSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = ('album_name', 'artist', 'tracks')

class ItemSerializer(patterns.AttachmentSerializer):
    class Meta(patterns.AttachmentSerializer.Meta):
        model = Item
        exclude = ('survey',)
        object_field = 'survey'
        wq_config = {
            'initial': 3,
        }

class SurveySerializer(patterns.AttachedModelSerializer):
    items = ItemSerializer(many=True)
    class Meta:
        model = Survey
'''


class UserSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xlsform_types[serializers.BooleanField] = 'boolean'

    # overriding to exclude permissions and groups
    def get_label_fields(self, default_fields):
        if not self.add_label_fields:
            return {}
        fields = {}

        exclude = getattr(self.Meta, 'exclude', [])
        if 'label' not in exclude and 'label' not in default_fields:
            fields['label'] = serializers.ReadOnlyField(source='__str__')

        info = model_meta.get_field_info(self.Meta.model)

        # Add labels for dates and fields with choices
        for name, field in info.fields.items():
            if name in getattr(self.Meta, "exclude", []):
                continue
            if name + '_label' in default_fields:
                continue
            if field.choices:
                fields[name + '_label'] = serializers.ReadOnlyField(
                        source='get_%s_display' % name
                )

        return fields

    class Meta:

        wq_field_config = {
            'is_staff': {'type': 'boolean'},
            'is_active': {'type': 'boolean'}
        }
        wq_config = {
            "fields": ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'last_login',
                       'date_joined'],
            "form": [
                {
                    "name": "username",
                    "label": "Username",
                    "bind": {
                        "required": True
                    },
                    "hint": "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                    "wq:length": 150,
                    "type": "string"
                },
                {
                    "name": "first_name",
                    "label": "First Name",
                    "wq:length": 30,
                    "type": "string"
                },
                {
                    "name": "last_name",
                    "label": "Last Name",
                    "wq:length": 30,
                    "type": "string"
                },
                {
                    "name": "email",
                    "label": "Email address",
                    "wq:length": 254,
                    "type": "string"
                },
                {
                    "name": "is_staff",
                    "label": "Is Staff",
                    "type": "boolean"
                },
                {
                    "name": "is_active",
                    "label": "Is Active",
                    "type": "boolean"
                },
                {
                    "name": "last_login",
                    "label": "Last Login",
                    "type": "dateTime",
                    "can_edit": False
                },
                {
                    "name": "date_joined",
                    "label": "Date Joined",
                    "type": "dateTime"
                }
            ]
        }


class FeelingsNeedsEntrySerializer(ModelSerializer):
    class Meta:
        wq_field_config = {
            'public': {'type': 'select one'}
        }
