from django.urls import path

from api.views import GeneralViewSet

general_models = GeneralViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

urlpatterns = [
    path("databases/<str:database_name>/tables/<str:table_name>/", general_models, name="general_models"),
] 
