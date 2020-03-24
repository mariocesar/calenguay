from django.contrib import admin
from django.urls import path

from calenguay.events.views import landing, category_detail, eventtype_detail, eventtype_make_appointment

urlpatterns = [
    path("admin/", admin.site.urls),
    path("category/<int:pk>/", category_detail, name="category_detail"),
    path("eventtype/<int:pk>/", eventtype_detail, name="eventtype_detail"),
    path("eventtype/<int:pk>/appointment/", eventtype_make_appointment, name="make_appointment"),
    path("", landing)
]
