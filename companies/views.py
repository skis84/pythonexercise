from django.http import JsonResponse, HttpResponseBadRequest, Http404
import requests
from .validator import Validator
from .models import Company, Address, PhoneNumber, Website
from datetime import datetime


# "business_id": "<business id>",
# "name": "<company name>",
# "address": "<street address, postal code and city>",
# "phone": "<company primary phone number>",
# "website": "<company website url>"


def index(request, company_id):

    if Validator.is_valid_company_id(company_id) is False:
        return HttpResponseBadRequest(
            "Bad request, please give valid company id.")

    api_url = "https://avoindata.prh.fi/bis/v1/"

    response = requests.get(api_url + company_id)
    jsondata = response.json()

    results = jsondata["results"]
    # Return 404 response if no results
    if len(results) == 0:
        raise Http404()

    result = results[0]

    business_id = result["businessId"]
    name = result["name"]

    # Check if Company already exists in local db
    try:
        company = Company.objects.get(business_id=business_id)
    except Company.DoesNotExist:
        # If not, store it
        company = Company(business_id, name)
        company.save()

    address = getAddressAndSaveToDb(result["addresses"], company)
    phone = getDetailAndSaveToDb(result["contactDetails"],
                                 "Matkapuhelin", PhoneNumber,
                                 company)
    website = getDetailAndSaveToDb(result["contactDetails"],
                                   "Kotisivun www-osoite", Website,
                                   company)

    filteredResponse = {"business_id": business_id,
                        "name": name,
                        "address": address,
                        "phone": phone,
                        "website": website}

    return JsonResponse(filteredResponse, safe=False)


def isValid(data):
    return data["endDate"] is None


def getAddressAndSaveToDb(addresses, company):
    street = ""
    postcode = ""
    city = ""
    for address in addresses:
        if isValid(address) and address["street"] != "":
            street = address["street"]
            postcode = address["postCode"]
            city = address["city"]
            registration_date = address["registrationDate"]

            # Check if address already exists in db
            try:
                Address.objects.get(
                    company=company.business_id)
            except Address.DoesNotExist:
                # Does not exist, create it
                address = Address(street=street, post_code=postcode, city=city,
                                  registration_date=registration_date,
                                  end_date=None, modified_date=datetime.now(),
                                  company=company
                                  )
                address.save()
            return f"{street} {postcode} {city}"
    return ""


def getDetailAndSaveToDb(contactDetails, contactDetailLabel, className,
                         company):
    for contact in contactDetails:
        if(isValid(contact)):
            if contact["type"] == contactDetailLabel:
                value = contact["value"]
                registration_date = contact["registrationDate"]

                # Check if contact detail already exists in db
                try:
                    className.objects.filter(
                        company=company.business_id)

                except className.DoesNotExist:
                    # Does not exist, create it
                    detail = className(value=value,
                                       registration_date=registration_date,
                                       end_date=None,
                                       modified_date=datetime.now(),
                                       company=company)
                    detail.save()
                return value
    return ""
