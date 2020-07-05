from django.http import JsonResponse, HttpResponseBadRequest, Http404
from .validator import Validator
from .models import Company, PhoneNumber, Website
from .businessdataservice import BusinessDataService


# "business_id": "<business id>",
# "name": "<company name>",
# "address": "<street address, postal code and city>",
# "phone": "<company primary phone number>",
# "website": "<company website url>"


def index(request, company_id):

    if Validator.is_valid_company_id(company_id) is False:
        return HttpResponseBadRequest(
            "Bad request, please give valid company id.")

    service = BusinessDataService()
    service.get_results(company_id)

    # Return 404 response if no results
    if service.number_of_results() == 0:
        raise Http404()

    business_id = service.get_business_id()
    name = service.get_name()

    # Check if Company already exists in local db
    try:
        company = Company.objects.get(business_id=business_id)
    except Company.DoesNotExist:
        # If not, store it
        company = Company(business_id, name)
        company.save()

    address = service.getAddressAndSaveToDb(company)
    phone = service.getDetailAndSaveToDb("Matkapuhelin", PhoneNumber,
                                         company)
    website = service.getDetailAndSaveToDb("Kotisivun www-osoite", Website,
                                           company)

    filteredResponse = {"business_id": business_id,
                        "name": name,
                        "address": address,
                        "phone": phone,
                        "website": website}

    return JsonResponse(filteredResponse, safe=False)
