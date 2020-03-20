# Of A Feather
Of a Feather is a dating app designed to maximize compatibility and improve the odds of relationship success by leveraging concepts found in psychology.  Based on their score, the user will be matched with users with compatible scores. The user can then accept or reject matches, view users, and see matches where both users have accepted the match. 

## Steps to Install this App

1. Clone this repo onto your computer
- ` git clone git@github.com:melliemuse/of-a-feather-API.git `

2. Create Virtual Environment
- ` cd of-a-feather-API `
- ` python -m venv OfAFeatherEnv `

3. Activate Virtual Environment
 For Mac: 
- ` source ./OfAFeatherEnv/bin/activate `

 For Windows:
- ` source ./OfAFeatherEnv/Scripts/activate `

4. Install Dependencies
- ` pip install -r requirements.txt `

5. Build Database from Models 
- ` python manage.py makemigrations capstoneapi `
- ` python manage.py migrate `

6. Create a Superuser 
- ` python manage.py createsuperuser `

7. Load data from fixtures into your database
- ` python manage.py loaddata fixtures/fixtures.json`

8. Run Server 
- ` python manage.py runserver `

9. Front End Dependencies
- Make Sure You Visit the Front End Repo and follow install instructions 
- https://github.com/melliemuse/of-a-feather-react