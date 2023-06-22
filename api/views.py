from django.shortcuts import render
from passlib.hash import django_pbkdf2_sha256 as handler
from django.db.models import F, Q
from rest_framework.views import APIView
from rest_framework.response import Response
import api.usable as uc
from .models import *
from decouple import config
import datetime
from datetime import datetime, date
import jwt


# User Registration View
class Register(APIView):
   def post (self,request):
        requireFields = ['firstname','lastname','email','password','contact']
        validator = uc.keyValidation(True,True,request.data,requireFields)

        if validator:
            return Response(validator,status = 200)

        else:
            firstname = request.data.get('firstname')
            lastname = request.data.get('lastname')
            email = request.data.get('email')
            password = request.data.get('password')
            contact = request.data.get('contact')
            role=request.data.get('role')


            if uc.checkemailforamt(email):
                if not uc.passwordLengthValidator(password):
                    return Response({"status":False, "message":"password should not be than 8 or greater than 20"})

                checkemail=Account.objects.filter(email=email).first()
                if checkemail:
                    return Response({"status":False, "message":"email already exists"})

                checkphone=Account.objects.filter(contact=contact).first()
                if checkphone:
                    return Response({"status":False, "message":"phone no already existsplease try different number"})

                data = Account(firstname = firstname, lastname = lastname, email=email, password=handler.hash(password), contact=contact,role=role)

                data.save()

                return Response({"status":True,"message":"Account Created Successfully"})
            else:
                return Response({"status":False,"message":"Email Format Is Incorrect"})




class login(APIView):

    def post (self,request):

        email = request.data.get('email')
        password = request.data.get('password')

        fetchAccount = Account.objects.filter(email=email).first()
        if fetchAccount:
            if handler.verify(password,fetchAccount.password):
                if fetchAccount.role == "admin":
                    # print('=============================================s=======admin token')
                    access_token_payload = {
                                    'firstname':fetchAccount.firstname, 
                                    'lastname':fetchAccount.lastname, 
                                    'email':fetchAccount.email, 
                                    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=22),
                                    'iat': datetime.datetime.utcnow(),

                            }

                    access_token = jwt.encode(access_token_payload,config('adminkey'),algorithm = 'HS256')
                    data = {'firstname':fetchAccount.firstname,'lastname':fetchAccount.lastname,'email':fetchAccount.email,'contact':fetchAccount.contact,'role':fetchAccount.role}
                    return Response({"status":True,"message":"Login Successlly","token":access_token,"admindata":data},200)

            
                # USER LOGIN API
                else: 
                    access_token_payload = {
                                'firstname':fetchAccount.firstname, 
                                'lastname':fetchAccount.lastname, 
                                'email':fetchAccount.email, 
                                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=22),
                                'iat': datetime.datetime.utcnow(),

                        }

                    access_token = jwt.encode(access_token_payload,config('adminkey'),algorithm = 'HS256')
                    data = {'firstname':fetchAccount.firstname,'email':fetchAccount.email,'contact':fetchAccount.contact,'role':fetchAccount.role}
                    return Response({"status":True,"message":"Login Successlly","token":access_token,"userdata":data},200)

            else:
                return Response({"status":False,"message":"Invalid crediatials"},200)

        else:
            return Response({"status":False,"message":"Account doesnot access"}) 
        

# loan request 

class LoanRequest(APIView):
    def post(self, request):
        amount = int(request.data.get('amount')) 
        role = request.data.get('role')

        if amount % 500 != 0:
            return Response({"status": False, "message": "Loan amount must be a multiple of 500."})
        
        today = date.today()
        existing_loan = loan.objects.filter(date__date=today).first()  # Correct model name to Loan
        if existing_loan:
            return Response({"status": False, "message": "You have already created a loan request today."})
        
        data = loan(amount=amount, date=datetime.now(), role=role)  # Correct model name to Loan
        data.save()
        
        return Response({"status": True, "message": "Loan request successfully sent."})


# Get Loan Detail

class LoanShow(APIView):
    def get(self, request):
        uid = request.GET.get('uid')

        data = loan.objects.filter(userdetails__uid=uid).values('amount', 'date','loanstatus', Firstname=F('userdetails__firstname'),Uid=F('userdetails__uid'))

        return Response({"status": True, "data": data})



#Update LoanStatus

class LoanStatus(APIView):
    def put(self,request):
        my_token = uc.admintokenauth(request.META['HTTP_AUTHORIZATION'][7:])
        if my_token:  
       
           loanstatus = request.data.get("loanstatus")
           comment = request.data.get("comment")
           firstname = request.data.get("firstname")

           data = loan.objects.filter(userdetails__firstname=firstname).first()

           if data:
              data.loanstatus=loanstatus
              data.comment=comment

              data.save()
              return Response({'status': True, 'Msg': 'loan details Update Successfully'}) 
        else:
            return Response({"status": False, "msg":"Unauthorized"})




https://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@github.com/muhammadadildeveloper999/Loan-Request-System.git

