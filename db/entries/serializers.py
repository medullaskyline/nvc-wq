from wq.db.rest.serializers import ModelSerializer

from rest_framework.fields import BooleanField, NullBooleanField


class FeelingsNeedsEntrySerializer(ModelSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xlsform_types.update({BooleanField: 'boolean'})
        print(self.xlsform_types)


