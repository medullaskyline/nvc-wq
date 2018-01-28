from wq.db.rest.serializers import ModelSerializer
from rest_framework import serializers


class FeelingsNeedsEntrySerializer(ModelSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xlsform_types[serializers.BooleanField] = 'boolean'
        # self.serializers.ChoiceField is already the key for 'select one'

    class Meta:
        # this adds to the configuration set in the rest.router.register_model
        wq_field_config = {
            'public': {'type': 'select one'}
        }



class UserSerializer(ModelSerializer):
    pass


user_form = [
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