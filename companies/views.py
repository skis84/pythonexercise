from django.http import HttpResponse
import requests


# Create your views here.


def index(request, company_id):
    response = requests.get("https://avoindata.prh.fi/bis/v1/" + company_id)
    # Print the status code of the response.
    print(response.status_code)

    return HttpResponse(response, content_type="application/json")
