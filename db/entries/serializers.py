from wq.db.rest.serializers import ModelSerializer
from wq.db.patterns import serializers as patterns
from rest_framework import serializers
from rest_framework.utils import model_meta

from .models import FeelingLeaf


class FeelingsNeedsEntrySerializer(ModelSerializer):
    class Meta:
        wq_field_config = {
            'public': {'type': 'select one'}
        }


class EntrySerializer(ModelSerializer):
    class Meta:
        wq_field_config = {
            'public': {'type': 'select one'},
            "feeling": {"wq:ForeignKey": "feelingleaf"},
            "need category": {"children": [
                {
                    "name": "need",
                    "label": "Need",
                    "bind": {
                        "required": True
                    },
                    "type": "string",
                    "wq:ForeignKey": "needleaf"
                },
            ]},
            # "need": {"wq:ForeignKey": "needleaf"}
        }


# class FeelingSerializer(patterns.AttachmentSerializer):
#
#     class Meta(patterns.AttachmentSerializer.Meta):
#         model = FeelingLeaf
#         exclude = ('FeelingSubCategory',)
#         object_field = 'FeelingSubCategory'


class UserSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xlsform_types[serializers.BooleanField] = 'boolean'

    # overriding to prevent permissions and groups
    # or just exclude = ('groups', 'permissions') in Meta?
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
