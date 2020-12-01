from django.http import HttpResponse

import os 
import pytest
def home(request):
    return HttpResponse(
        'Please go to <a href="/api/company/1">api/company/<business_id></>')
