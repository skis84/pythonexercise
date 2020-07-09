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

Instructions to run:
git clone git@github.com:skis84/pythonexercise.git

In project folder, run the following commands:
pip3 install pipenv
pipenv install
pipenv shell
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver

Tests can be run with:
python3 manage.py test
