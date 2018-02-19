from wq.db.rest.views import ModelViewSet
from django.db.models.fields import FieldDoesNotExist
from rest_framework.decorators import detail_route

from wq.db.rest.model_tools import get_by_identifier
from rest_framework.response import Response

from rest_framework.routers import Route
from wq.db.rest.views import ModelViewSet
from wq.db.rest.models import get_ct
from wq.db.patterns.relate.models import get_related_parents, get_related_children


class NoDetailViewset(ModelViewSet):

    def list(self, request, *args, **kwargs):

        response = super().list(
            request, *args, **kwargs
        )

        content_type = get_ct(self.model)
        for parent_content_type, fields in content_type.get_foreign_keys().items():
            if len(fields) == 1:
                parent = self.get_parent(parent_content_type, fields[0], response)
                if not parent: continue  # got the grandparent, not the parent
                response.data['parent_url'] = parent_content_type.urlbase
                response.data['parent_label'] = parent_content_type.name + ' list'

                for grandparent_content_type, fields in parent_content_type.get_foreign_keys().items():
                    if len(fields) == 1:
                        grandparent_model_class = grandparent_content_type.model_class()
                        parent_model_class = parent_content_type.model_class()
                        grandparent_field_name = ''
                        for field in parent_model_class._meta.fields:
                            if type(field.rel).__name__ == 'ManyToOneRel':
                                if field.rel.to == grandparent_model_class:
                                    grandparent_field_name = field.name

                        grandparent_id = parent_model_class.objects.values().get(id=response.data['parent_id']).get(
                            grandparent_field_name + '_id')
                        response.data[
                            'parent_url'] = grandparent_content_type.urlbase + '/' + str(
                            grandparent_id) + '/' + parent_content_type.urlbase
                        # the parent_label doesn't work
                        response.data['parent_label'] += ' for ' + str(getattr(parent, grandparent_field_name))

        return response


"""
Feeling SubCategories, NeedLeafs, FeelingLeafs

    def retrieve(self, request, *args, **kwargs):
        '''
        Custom retrieve watches for "new" lookup value and switches modes
        accordingly
        '''
        if hasattr(self, 'lookup_url_kwarg'):
            # New in DRF 2.4?
            lookup = self.lookup_url_kwarg or self.lookup_field
        else:
            lookup = self.lookup_field

        if self.kwargs.get(lookup, "") == "new":
            # new/edit mode
            return self.new(request)
        else:
            # Normal detail view
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
"""
