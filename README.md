This is a company API project with python and Django.

The application exposes endpoint /api/company/<business_id> where you can get details from a company.

Example usage (replace 1234567-1 with valid business id):
GET /api/company/1234567-1

Response:
{
"business_id": "1234567-1",
"name": "Example company",
"address": "Example street 1, 12345 City",
"phone": "123456789",
"website": "https://example.com"
}

Company data is fetched from the open data api by the Finnish business information system: http://avoindata.prh.fi/ytj.html
The application also keeps local copies of the data in SQLite3 database
