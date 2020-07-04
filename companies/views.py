from django.http import JsonResponse
import requests

# Create your views here.
#
# "business_id": "<business id>",
# "name": "<company name>",
# "address": "<street address, postal code and city>",
# "phone": "<company primary phone number>",
# "website": "<company website url>"


def index(request, company_id):
    api_url = "https://avoindata.prh.fi/bis/v1/"
    response = requests.get(api_url + company_id)

    jsondata = response.json()

    result = jsondata["results"][0]

    business_id = result["businessId"]
    name = result["name"]

    street = ""
    postcode = ""
    city = ""
    phone = ""
    website = ""

    addresses = result["addresses"]
    contactDetails = result["contactDetails"]

    for address in addresses:
        if isValid(address) and address["street"] != "":
            street = address["street"]
            postcode = address["postCode"]
            city = address["city"]
            break

    for contact in contactDetails:
        if(isValid(contact)):
            if contact["type"] == "Matkapuhelin":
                phone = contact["value"]

            if contact["type"] == "Kotisivun www-osoite":
                website = contact["value"]

    filteredResponse = {"business_id": business_id,
                        "name": name,
                        "address": f"{street} {postcode} {city}",
                        "phone": phone,
                        "website": website}

    return JsonResponse(filteredResponse, safe=False)


def isValid(data):
    return data["endDate"] is None
