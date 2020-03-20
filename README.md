# Of A Feather
Of a Feather is a dating app designed to maximize compatibility and improve the odds of relationship success by leveraging concepts found in psychology.  Based on their score, the user will be matched with users with compatible scores. The user can then accept or reject matches, view users, and see matches where both users have accepted the match. 

## Steps to Install this App

Clone this repo onto your computer
- ` git clone git@github.com:melliemuse/of-a-feather-react.git `

Create Virtual Environment
- ` cd of-a-feather-API `
- ` python -m venv OfAFeatherEnv `

Activate Virtual Environment
 For Mac: 
- ` source ./OfAFeatherEnv/bin/activate `

 For Windows:
- ` source ./OfAFeatherEnv/Scripts/activate `

Install Dependencies
- ` pip install -r requirements.txt `

Build Database from Models 
- ` python manage.py makemigrations `
- ` python manage.py migrate `

Create a Superuser 
- ` python manage.py createsuperuser `

Load data from fixtures into your database
- ` python manage.py loaddata `

Run Server 
- ` python manage.py runserver `