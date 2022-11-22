from django.contrib import admin
from django.urls import path

from core.apis import OTS
from core.views import CreateSecretView, ShowSecretView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/<str:secret_id>", OTS.as_view()),
    path("api", OTS.as_view()),
    path("view/<str:secret_id>", ShowSecretView.as_view()),
    path("", CreateSecretView.as_view()),
]
