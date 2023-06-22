from django.urls import path
from api.views import *
urlpatterns = [
    
# ADMIN-SITE-URLS
path('Register',Register.as_view()),
path('login',login.as_view()),
path('LoanRequest',LoanRequest.as_view()),
path('LoanShow',LoanShow.as_view()),
path('LoanStatus',LoanStatus.as_view()),

]