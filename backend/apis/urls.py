from django.conf.urls import url
from .views import (
back
)


urlpatterns = [
    url(r"^(?P<token>[\w|\d]+?)/back$", back)
]
