# Django
Speech and Text Summariser WebApp using Django

--Web App to Convert Speech and Text to Summary and Lists with Hindi and English support using python libraries and Google SpeechtoText API with login and register utility--
--Python 3.7.9--
--Django v2.2--
--PostgreSQL v13.0--
--pgAdmin 4 v4.26--
--psycopg2 (via C++ Microsoft Tools)--

--Functions--
::maketextsummary(HTTP request)::
converts text to summary using string input via HTTP POST
requires - nltk
returns - HTTP page render via output string in Jinja format inside html page

::maketextlist(HTTP request)::
converts text to list using string input via HTTP POST
requires - nltk
returns - HTTP page render via output string in Jinja format inside html page

::makespeechsum(HTTP request)::
converts speech to summary using audio input via mic
requires - nltk,  speech_recognition, os, pyttsx3
returns - HTTP page render via output string in Jinja format inside html page

::makespeechlist(HTTP request)::
converts speech to list using audio input via mic
requires - nltk,  speech_recognition, os, pyttsx3
returns - HTTP page render via output string in Jinja format inside html page


Basic Steps - 

1. --workon [virtual environment name]--
2. Move to the folder where you want to set up the project
3. --django-admin startproject [project-name]--
3. Go inside project folder
4. To check if its running:: --python manage.py runserver--
5. Now gotta start an app that represents a module inside the project, division of module is up to us
6. To start an app: --python manage.py startapp [app-name]--
7. A folder should be created
8. In the app folder, create a file  - urls.py
9. In urls.py, define a path and function to handle that path(start with homepage) - 
urlpatterns = [
    path('', views.home, name = "homes"),
]

10. In views.py, define a function home to handle this
def home(request):
    return HttpResponse("Hello")

11. Now we need to tell the main urls.py of the project to redirect to this app for homepage - 
urlpatterns = [
    path('', include('main_app.urls')),
    path('admin/', admin.site.urls),
]
have to import "include" from django.urls (from django.urls import path, include)

12. Now we need to add templates for pages that we have to add -
create a folder in the project main directory (can give any name)
13. Inside that we can make html files
14. Make a file home.html
15. We have to make changes to settings.py to make sure django knows where to find templates - 

16. Using pgadmin and postgres DB
17. Make changes in settings.py - 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hciproject',
        'USER': 'postgres',
        'PASSWORD' : '1234',
        'HOST': 'localhost',
    }
}
18. Define a model - 
class ListStorage(models.Model):
    username = models.CharField(max_length = 200)
    user_list = models.TextField()
19. Mention appname in settings.py - 
INSTALLED_APPS = [
    'app_main.apps.AppMainConfig',

20. Migration file will be formed
21. Now migrate using this file to DB - 
--python manage.py sqlmigrate [appname] [migration file name]\--
22. Python manage.py migrate
23. For admin portal - localhost:8000/admin
24 Need to create superuser:: --python manage.py createsuperuser--
25. In admin.py  need to list model
