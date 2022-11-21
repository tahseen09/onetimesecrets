from django.contrib import admin
from django.urls import path

from core.apis import OTS

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/<str:secret_id>', OTS.as_view()),
    path('api', OTS.as_view()),
]
