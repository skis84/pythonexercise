from django.http import JsonResponse, HttpResponseBadRequest, Http404
from .validator import Validator
from .models import Address, Name, PhoneNumber, Website
from .businessdataservice import BusinessDataService


# Function for endpoint /api/company/<business-id>
def company(request, company_id):

    if Validator.is_valid_company_id(company_id) is False:
        return HttpResponseBadRequest(
            "Bad request, please give valid company id.")

    service = BusinessDataService()
    service.get_results(company_id)

    # Return 404 response if no results
    if service.number_of_results() == 0:
        raise Http404()

    company = service.get_company_from_db(company_id)

    service.save_data_to_db("names", "order", [0], "name", Name,
                            company)
    service.save_data_to_db("addresses", "type", [1, 2], "street",
                            Address, company,
                            service.get_address_from_db,
                            service.create_address)
    service.save_data_to_db("contactDetails", "type",
                            ["Matkapuhelin", "Mobiltelefon", "Mobile phone",
                             "Puhelin", "Telefon", "Telephone"],
                            "value", PhoneNumber, company)
    service.save_data_to_db("contactDetails", "type",
                            ["Kotisivun www-osoite", "www-address",
                             "Website address"], "value",
                            Website, company)

    # Query database to get the result JSON
    # "business_id": "<business id>",
    # "name": "<company name>",
    # "address": "<street address, postal code and city>",
    # "phone": "<company primary phone number>",
    # "website": "<company website url>"
    response = service.form_response_from_db(company_id)

    return JsonResponse(response, safe=False)
