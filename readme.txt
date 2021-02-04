1. create db mysitedb at postgres

2. go to your main folder, i.e my code is in c:\learn\django\mysite
   cd c:\learn\django\mysite
   run these commands:
   python -m virtualenv virtual
   .\virtual\Scripts\activate
   pip install -r requirements.txt
   python manage.py migrate

3. if you want to run development server, just run the run-env.bat,
   or else run the production server, run-server.bat