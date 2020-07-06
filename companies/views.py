from django.http import JsonResponse, HttpResponseBadRequest, Http404
from .validator import Validator
from .models import Company, Name, PhoneNumber, Website
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

    # Check if Company already exists in local db
    try:
        company = Company.objects.get(business_id=business_id)
    except Company.DoesNotExist:
        # If not, store it
        company = Company(business_id)
        company.save()

    service.save_data_to_db("names", [], "name", Name,
                            company)
    service.save_addresses_to_db(company)
    service.save_data_to_db("contactDetails", ["Matkapuhelin", "Puhelin"],
                            "value",
                            PhoneNumber, company)
    service.save_data_to_db("contactDetails",
                            ["Kotisivun www-osoite"], "value",
                            Website, company)

    # Query database
    response = service.form_response_from_db(business_id)

    return JsonResponse(response, safe=False)
