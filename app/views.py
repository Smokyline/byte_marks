from django.shortcuts import render


from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import transaction
# Create your views here.
import json
import datetime
from app.app_logic_foo import *
from django.views.decorators.csrf import csrf_exempt
import os
from byte_marks.settings import BASE_DIR


def index(request):
    f = open(os.path.join(BASE_DIR, 'readme.txt'), 'r')
    file_content = f.read()
    f.close()
    return HttpResponse(file_content, content_type="text/plain")

@csrf_exempt
def push_marks(request):
    """
    {
    "code":"KLI",
    "date0":1659330000,
    "date1":1659333600,
    "action":0,
    "comp":"v3",
    "freq":"min"
    }
    """
    request = json.loads(request.body)
    print(request)
    posting_status = post_marks_to_sql(request)
    if posting_status:
        return JsonResponse({'status': 1}, safe=False)
    else:
        return JsonResponse({'status': 0}, safe=False)

def get_marks(request):
    request = json.loads(request.body)

    get_marks_from_sql(request)
    return JsonResponse({'status': 0}, safe=False)