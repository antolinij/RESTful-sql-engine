
# django
from django.db import IntegrityError

# django rest
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import NotFound

# project resources 
from api.serializers import GeneralSerializer
import api.models 
from api.exceptions import CustomValidation

# utils tools
import ipdb


class GeneralViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        
        model = self.kwargs.get('table_name').capitalize()
        
        try:
            return getattr(api.models, model).objects.all()         
        except:
            raise NotFound(detail={'detail': 'the resource {model} does not exist', 'status_code': 400}, code=404)

    def get_serializer_class(self):
        
        model = self.kwargs.get('table_name').capitalize()
        fields = self.request.query_params.get("fields")
        
        try:    
            GeneralSerializer.Meta.model =  getattr(api.models, model)            
            if fields:
                GeneralSerializer.Meta.fields = tuple(map(str, fields.split(', ')))
            return GeneralSerializer
        except Exception as e:
            raise CustomValidation(detail=repr(e), status_code=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError as exc:
            raise CustomValidation(detail=repr(exc), status_code=status.HTTP_400_BAD_REQUEST)