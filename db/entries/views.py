from wq.db.rest.views import ModelViewSet
from django.contrib.auth.models import User
from django.db.models.fields import FieldDoesNotExist
# from django.contrib.auth.mixins import LoginRequiredMixin

from wq.db.rest.model_tools import get_ct, get_object_id, get_by_identifier
from rest_framework.response import Response
from rest_framework import status

# from .models import Feeling, Need, FeelingsNeedsEntry


class FeelingsNeedsEntryViewSet(ModelViewSet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def edit(self, request, *args, **kwargs):
        """
        Generates a context appropriate for editing a form
        """
        response = self.retrieve(request, *args, **kwargs)
        obj = self.get_object()
        if obj.user != request.user:
            return response
        serializer = self.get_serializer(obj)
        serializer.add_lookups(response.data)
        return response

    def new(self, request):
        """
        new is a variant of the "edit" action, but with no existing model
        to lookup.
        """
        self.action = 'edit'
        init = request.GET.dict()
        for arg in self.ignore_kwargs:  ## todo: ignore_kwargs should include User
            init.pop(arg, None)
        for key in list(init.keys()):
            try:
                field = self.model._meta.get_field(key)
            except FieldDoesNotExist:
                del init[key]
            else:
                if field.rel:
                    fk_model = field.rel.to
                    try:
                        obj = get_by_identifier(fk_model.objects, init[key])
                    except fk_model.DoesNotExist:
                        del init[key]
                    else:
                        init[key] = obj.pk

        obj = self.model(**init)
        obj.user = request.user
        serializer = self.get_serializer(obj)
        data = serializer.data
        serializer.add_lookups(data)
        resp = Response(data)
        # resp.data['user_list'] = [{'id': request.user.id, 'label': request.user.username, 'selected': True}]
        return resp

    def retrieve(self, request, *args, **kwargs):
        """
        Custom retrieve watches for "new" lookup value and switches modes
        accordingly
        """
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
            return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        response = super().list(
            request, *args, **kwargs
        )
        if not isinstance(response.data, dict):
            return response

        if self.target:
            response.data['target'] = self.target
        ct = get_ct(self.model)
        for pct, fields in ct.get_foreign_keys().items():
            if len(fields) == 1:
                self.get_parent(pct, fields[0], response)
        return response

    def create(self, request, *args, **kwargs):
        # request.data.user_id = [str(request.user.id)]
        # request.data.user_id.append(str(request.user.id))
        response = super().create(
            request, *args, **kwargs
        )
        if not request.accepted_media_type.startswith('text/html'):
            # JSON request, assume client will handle redirect
            return response

        # HTML request, probably a form post from an older browser
        if response.status_code == status.HTTP_201_CREATED:
            return self.postsave(request, response)
        else:
            return self.saveerror(request, response)

