from wq.db.rest.views import ModelViewSet
from django.db.models.fields import FieldDoesNotExist
from rest_framework.decorators import detail_route

from wq.db.rest.model_tools import get_by_identifier
from rest_framework.response import Response


from rest_framework.routers import Route
from wq.db.rest.views import ModelViewSet
from wq.db.rest.models import get_ct
from wq.db.patterns.relate.models import get_related_parents, get_related_children




