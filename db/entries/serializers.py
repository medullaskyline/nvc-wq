from collections import OrderedDict
import six

from wq.db.rest.serializers import ModelSerializer, LookupRelatedField
from wq.db.patterns.serializers import AttachmentSerializer, AttachedModelSerializer
from wq.db.patterns.base.serializers import AttachmentListSerializer
from rest_framework import serializers
from rest_framework.relations import method_overridden, PKOnlyObject
from rest_framework.utils import model_meta
from rest_framework.fields import empty, Field, iter_options, get_attribute, is_simple_callable, ListField
from smart_selects.form_fields import ChainedModelChoiceField
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import smart_text
from django.db.models import Manager
from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _


from .models import (FeelingLeaf, NeedLeaf, FeelingSubCategory, FeelingMainCategory, NeedCategory)


class NeedLeafSerializer(AttachmentSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = NeedLeaf
        fields = ('need_leaf',)
        object_field = ('need_category',)
        # from super: list_serializer_class = AttachmentListSerializer


class NeedCategorySerializer(AttachedModelSerializer):
    needleaves = NeedLeafSerializer(many=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.is_detail
        # self.bind(<field_name>, self)
        #self.fields
        # if args and self.is_detail:
        #   pk = args[0].pk
        #   self.get_attachment(self.Meta.model, pk)
        # self.build_field(field_name, info, model_class, nested_depth)
        # self.instance
        # self.context
        # self.serializer_url_field

    class Meta:
        model = NeedCategory
        fields = "__all__"

        wq_config = {
            "edit": False,
            "can_add": False,
            "form": {"childUrl": "NeedLeaves"},
            "modes": ["list"],
        }
        wq_field_config = {
            "needleaves": {
                "name": "needleaves",
                "label": "",
                "type": "string",
                "childUrl": "NeedLeaves",
                "children": [{
                    "name": "need_leaf",
                }]
            }
        }

class FeelingLeafSerializer(AttachmentSerializer):
    class Meta:
        model = FeelingLeaf
        fields = ('feeling_leaf',)
        object_field = ('feeling_sub_category',)


class FeelingSubCategorySerializer(AttachedModelSerializer, AttachmentSerializer):
    feelingleaves = FeelingLeafSerializer(many=True)

    class Meta:
        model = FeelingSubCategory
        fields = "__all__"
        object_field = 'feeling_main_category'

        wq_config = {
            "edit": False,
            "can_add": False,
            "form": {"childUrl": "FeelingLeaves"},
            "modes": ["list"],
        }
        wq_field_config = {
            "feelingleaves": {
                "name": "feelingleaves",
                "label": "",
                "type": "string",
                "childUrl": "FeelingLeaves",
                "children": [{
                    "name": "feeling_leaf",
                }]
            }
        }

class FeelingMainCategorySerializer(AttachedModelSerializer):
    feelingsubcategories = FeelingSubCategorySerializer(many=True)

    class Meta:
        model = FeelingMainCategory
        fields = "__all__"

        wq_config = {
            "edit": False,
            "can_add": False,
            "form": {"childUrl": "FeelingSubcategories"},
            "modes": ["list"],
        }
        wq_field_config = {
            "feelingsubcategories": {
                "name": "feelingsubcategories",
                "label": "",
                "type": "string",
                "childUrl": "FeelingSubcategories",
                "children": [{
                    "name": "feeling_subcategory",
                }]
            }
        }


'''
all serializer Fields inherit
    def bind(self, field_name, parent):
    def validators -- getter, setter and property
    def get_initial(self):
    def get_value(self, dictionary):
    def get_attribute(self, instance):
    def get_default(self):
    def validate_empty_values(self, data):
    def run_validation(self, data=empty):  # calls next
    def run_validators(self, value):
    def to_internal_value(self, data):  # all must implement this
    def to_representation(self, value): # all must implement this
    def fail
    def root
    def context
    def __new__
    
'''
class RelatedField(Field):
    queryset = None
    html_cutoff = None
    html_cutoff_text = None

    def __init__(self, **kwargs):
        self.queryset = kwargs.pop('queryset', self.queryset)

        cutoff_from_settings = api_settings.HTML_SELECT_CUTOFF
        if cutoff_from_settings is not None:
            cutoff_from_settings = int(cutoff_from_settings)
        self.html_cutoff = kwargs.pop('html_cutoff', cutoff_from_settings)

        self.html_cutoff_text = kwargs.pop(
            'html_cutoff_text',
            self.html_cutoff_text # or _(api_settings.HTML_SELECT_CUTOFF_TEXT)
        )
        if not method_overridden('get_queryset', RelatedField, self):
            assert self.queryset is not None or kwargs.get('read_only', None), (
                'Relational field must provide a `queryset` argument, '
                'override `get_queryset`, or set read_only=`True`.'
            )
        assert not (self.queryset is not None and kwargs.get('read_only', None)), (
            'Relational fields should not provide a `queryset` argument, '
            'when setting read_only=`True`.'
        )
        kwargs.pop('many', None)
        kwargs.pop('allow_empty', None)
        super().__init__(**kwargs)

    def run_validation(self, data=empty):
        # We force empty strings to None values for relational fields.
        if data == '':
            data = None
        return super().run_validation(data)

    # todo: override this for ChainedField
    def get_queryset(self):
        queryset = self.queryset
        if isinstance(queryset, (QuerySet, Manager)):
            queryset = queryset.all()
        return queryset

    def use_pk_only_optimization(self):
        return False

    def get_attribute(self, instance):
        if self.use_pk_only_optimization() and self.source_attrs:
            # Optimized case, return a mock object only containing the pk attribute.
            try:
                instance = get_attribute(instance, self.source_attrs[:-1])
                value = instance.serializable_value(self.source_attrs[-1])
                if is_simple_callable(value):
                    # Handle edge case where the relationship `source` argument
                    # points to a `get_relationship()` method on the model
                    value = value().pk
                return PKOnlyObject(pk=value)
            except AttributeError:
                pass

        # Standard case, return the object instance.
        return get_attribute(instance, self.source_attrs)

    def get_choices(self, cutoff=None):
        queryset = self.get_queryset()
        if queryset is None:
            # Ensure that field.choices returns something sensible
            # even when accessed with a read-only field.
            return {}

        if cutoff is not None:
            queryset = queryset[:cutoff]

        return OrderedDict([
            (
                self.to_representation(item),
                self.display_value(item)
            )
            for item in queryset
        ])

    @property
    def choices(self):
        return self.get_choices()

    @property
    def grouped_choices(self):
        return self.choices

    def iter_options(self):
        return iter_options(
            self.get_choices(cutoff=self.html_cutoff),
            cutoff=self.html_cutoff,
            cutoff_text=self.html_cutoff_text
        )

    def display_value(self, instance):
        return six.text_type(instance)


class SlugRelatedField(serializers.RelatedField):
    """rest_framework/relations"""
    """
    A read-write field that represents the target of the relationship
    by a unique 'slug' attribute.
    """
    default_error_messages = {
        'does_not_exist': _('Object with {slug_name}={value} does not exist.'),
        'invalid': _('Invalid value.'),
    }

    def __init__(self, slug_field=None, **kwargs):
        assert slug_field is not None, 'The `slug_field` argument is required.'
        self.slug_field = slug_field
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(**{self.slug_field: data})
        except ObjectDoesNotExist:
            self.fail('does_not_exist', slug_name=self.slug_field, value=smart_text(data))
        except (TypeError, ValueError):
            self.fail('invalid')

    def to_representation(self, obj):
        return getattr(obj, self.slug_field)


class LookupRelatedField(serializers.SlugRelatedField):
    """wq/db/rest/serializers"""
    def __init__(self, router, model, **kwargs):
        self.router = router
        self.model = model
        super().__init__(**kwargs)

    @property
    def slug_field(self):
        if not self.router:
            return 'pk'
        return self.router.get_lookup_for_model(self.model)


class ChainedField(LookupRelatedField):
    def __init__(self, router, model, **kwargs):
        super().__init__(router, model, **kwargs)

    def get_choices(self, cutoff=None):
        queryset = self.get_queryset()
        if queryset is None:
            # Ensure that field.choices returns something sensible
            # even when accessed with a read-only field.
            return {}

        if cutoff is not None:
            queryset = queryset[:cutoff]

        return OrderedDict([
            (
                self.to_representation(item),
                self.display_value(item)
            )
            for item in queryset
        ])


class EntrySerializer(ModelSerializer):

    # todo: instead of overriding methods, make a mixin or mixins
    # todo: SerializerMethodField to imitate model methods?
    # todo: from smart_selects.widgets.ChainedSelect adapt the media property to include other areas (in the js =[] list) that chainedfk.js could be besides the django admin static directory
    # todo: also from widgets.ChainedSelect adapt the render() and _get_available_choices() methods
    """
     SerializerMethodField, which is read-only
        class ExampleSerializer(self):
            extra_info = SerializerMethodField()

            def get_extra_info(self, obj):
                return ...  # Calculate some data to return.

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xlsform_types[ChainedField] = 'chained'

    def validate(self, attrs):
        user = self.context.get("request").user  # context also has 'format': 'json' and 'view': <viewset>

        # force save as the user who is making/changing this entry
        if user.is_authenticated:
            if not user.is_superuser:
                attrs['user'] = user

        # later can validate that attrs['feeling_sub_category']
        # has a foreign key pointing to attrs['feeling_main_category'], etc
        return super().validate(attrs)

    class Meta:
        fields = "__all__"
        wq_field_config = {
            'public': {'type': 'select one'}
        }


"""
wq_field_config = {
    'public': {'type': 'select one'},
    'feeling_main_category': {'children': ['feeling_sub_category']}
    'feeling_sub_category': {'children': ['feeling_leaf']},
    // ?? 'feeling_leaf': {'type': 'repeat'},
    'need_category': {'children': ['need_leaf']}
}
"""


# 'feeling_sub_category': {'type': 'chained'}

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

