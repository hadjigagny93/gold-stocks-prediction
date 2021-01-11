from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from app_utils.request_back import return_json
from .models import *
import json
from datetime import datetime

def apiscalltask_register(**kwargs):
    name = kwargs.get('name')
    if name not in ('back' 'current'):
        raise
    now = datetime.now()
    from_tab, created = Mode.objects.get_or_create(name=name)
    apiscallertask_params = {"current_datetime": now, "from_tab": from_tab}
    register_created = ApiCallerTask.objects.create(**apiscallertask_params)
    if not register_created:
        raise
    return

@csrf_exempt
def back(request, token):
    if request.method != "POST":
        result = "You must use POST method request for pushing data in db"
        return return_json(7, result)
    # get data passed as params in request
    # and push them in database
    body_request = request.body.decode("utf-8")
    global_news_headers = json.loads(body_request)
    #print(body_request)
    # register the api call in aspicallertask table in backend
    #now = datetime.now()
    #from_tab = Mode.objects.create(name="back")
    #apiscallertask_params = {"current_datetime": now, "from_tab": from_tab}
    #register_created = ApiCallerTask.objects.create(**apiscallertask_params)
    #if not register_created:
    #    raise
    _ = apiscalltask_register(name="back")
    for news_header in global_news_headers:
        created = Back.objects.create(**news_header)
        #print(created)
    return return_json(1, "object well created")

@csrf_exempt
def current(request, token):
    if request.method != "POST":
        result = "You must use POST method request for pushing data in db"
        return return_json(7, result)
    # get data passed as params in request
    # and push them in database
    body_request = request.body.decode("utf-8")
    global_news_headers = json.loads(body_request)
    #print(body_request)
    #now = datetime.now()
    #from_tab = Mode.objects.create(name="current")
    #apiscallertask_params = {"current_datetime": now, "from_tab": from_tab}
    #register_created = ApiCallerTask.objects.create(**apiscallertask_params)
    #if not register_created:
    #    raise
    result = dict()
    _ = apiscalltask_register(name="current")
    for news_header in global_news_headers:
        # filter hash value for check
        # if the posted news has not been in the db yet
        current_header_hash = news_header.get('header_hash')
        news_header_exists = Current.objects.filter(header_hash=current_header_hash)
        #print(news_header_exists)
        if news_header_exists:
            print("This news header has already been created")
            result = {**result, **{current_header_hash: "updated"}}
            continue
        result = {**result, **{current_header_hash: "created"}}
        created = Current.objects.create(**news_header)
        #print(created)
    return return_json(1, result)
