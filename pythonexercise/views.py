from django.http import HttpResponse


def home(request):
    return HttpResponse(
        'Please go to <a href="/api/company/1">api/company/<business_id></>')
