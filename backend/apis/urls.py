from django.conf.urls import url
from .views import (
back,
current,
)


urlpatterns = [
    url(r"^(?P<token>[\w|\d]+?)/back$", back),
    url(r"^(?P<token>[\w|\d]+?)/current$", current)
]
