from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import IsAdminUser, IsAuthenticated
# from rest_framework_jwt.views import JSONWebTokenAPIView





@login_required(login_url="login")
# Create your views here.
def Home(request):
    user_first= request.user.first_name

    accepted_claims = Claims.objects.filter(user=request.user, status='A').count()
    rejected_claims = Claims.objects.filter(user=request.user, status='R').count()
    initiated_claims = Claims.objects.filter(user=request.user, status='I`').count()


    count_of_claims=Claims.objects.filter(user=request.user).count()
    count_of_policys=Policys.objects.filter(user=request.user).count()



    context={"first": user_first,"accepted_claims":accepted_claims,"rejected_claims":rejected_claims,"count_of_claims":count_of_claims,"count_of_policys":count_of_policys,"initiated_claims":initiated_claims}
    return render(request, "index.html",context)



from django.contrib import messages

def signuppage(request):
    if request.method == "POST":
        first_name = request.POST.get("firstname")
        last_name = request.POST.get("lastname")
        user = request.POST.get("Username")
        e_mail = request.POST.get("email")
        password1 = request.POST.get("password")
        confirmpassword = request.POST.get("confirmpassword")

        # Check if any field is empty
        if not all([first_name, last_name, user, e_mail, password1, confirmpassword]):
            messages.error(request, "Please fill out all fields.")
            return redirect("signup")

        if password1 == confirmpassword:
            if not User.objects.filter(username=user).exists():
                if not User.objects.filter(email=e_mail).exists():
                    user = User.objects.create_user(
                        username=user, email=e_mail, password=password1,
                        first_name=first_name, last_name=last_name
                    )
                    user.save()
                    messages.success(request, "Account Created!")
                    return redirect("login")
                else:
                    messages.error(request, "Email is already in use.")
            else:
                messages.error(request, "Username is already taken.")
        else:
            messages.error(request, "Passwords do not match.")

    return render(request, "register.html")


def loginpage(request):
    if request.method == "POST":
        username = request.POST["Name"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # pruser)
            login(request, user)
            return redirect("home")
        # premail,password)
        else:
            # messages.error(request, "Error please check your credentials!")
            return redirect("login")
    else:
        return render(request, "login.html")


@login_required(login_url="login")
def logoutpage(request):
    # pr"logout")
    logout(request)
    return redirect("home")


@login_required(login_url="login")
def Get_Policy(request):
    try:
        policys=Policys.objects.filter(user=request.user)
        context = {"policys": policys}
    except:
        context = {"policys":"None"}

    return render(request,"policytable.html",context)




@login_required(login_url="login")
def Get_Claim(request):
    try:
        claims=Claims.objects.filter(user=request.user)
        policys =Policys.objects.filter(user=request.user)

        context = {"claims": claims, "policys":policys}
    except:
        context = {"claims":"None", "policys":"None"}

    return render(request,"claimtable.html",context)



@login_required(login_url="login")
def Create_Claim(request):
    form = ClaimForm(user=request.user)
    if request.method == 'POST':
        form = ClaimForm(request.user, request.POST)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.user = request.user
            selected_policy = Policys.objects.get(policy_number=form.cleaned_data['policy_number'])
            claim.policy_number = form.cleaned_data['policy_number']
            claim.res_amt = selected_policy.coverage
            
            if claim.amt <= claim.res_amt:
                # Check if any previous claims exist
                if Claims.objects.filter(policy_number=form.cleaned_data['policy_number']).exists():
                    latest_claim_instance = Claims.objects.filter(policy_number=claim.policy_number).latest('created_at')
                    remaining_amt = latest_claim_instance.res_amt - claim.amt
                    if remaining_amt >= 0:
                        # If remaining_amt is non-negative, deduct claim amount and save the claim
                        claim.status = 'I'
                        claim.res_amt = remaining_amt
                        claim.save()
                        return redirect('getclaim')
                    else:
                        # If remaining_amt is negative, reject the claim
                        claim.status = 'R'
                        claim.res_amt = latest_claim_instance.res_amt
                        claim.save()
                        return redirect('getclaim')
                else:
                    # If no previous claims exist, deduct claim amount and save the claim
                    claim.status = 'I'
                    claim.res_amt -= claim.amt
                    claim.save()
                    return redirect('getclaim')
            
            # If claim amount exceeds res_amt, reject the claim
            claim.status = 'R'
            claim.save()
            return redirect('getclaim')
                
    context = {"form": form}
    return render(request, "addclaim.html", context)




# views.py

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Policys, Claims
from .forms import ClaimForm
from .serializers import *

@api_view(['GET'])
def get_policys(request):
    if request.method == 'GET':
        policys = Policys.objects.filter(user=request.user)
        serializer = PolicySerializer(policys, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def get_claims(request):
    if request.method == 'GET':
        claims = Claims.objects.filter(user=request.user)
        serializer = ClaimCreateSerializer(claims, many=True)
        return Response(serializer.data)

# @api_view(['POST'])
# def post_create_claim(request):
#     if request.method == 'POST':
#         form = ClaimForm(user=request.user, data=request.data)
#         if form.is_valid():
#             claim = form.save(commit=False)
#             claim.user = request.user
#             selected_policy = Policys.objects.get(policy_number=form.cleaned_data['policy_number'])
#             claim.policy_number = form.cleaned_data['policy_number']
#             claim.res_amt = selected_policy.coverage
            
#             if claim.amt <= claim.res_amt:
#                 if Claims.objects.filter(policy_number=form.cleaned_data['policy_number']).exists():
#                     latest_claim_instance = Claims.objects.filter(policy_number=claim.policy_number).latest('created_at')
#                     remaining_amt = latest_claim_instance.res_amt - claim.amt
#                     if remaining_amt >= 0:
#                         claim.status = 'I'
#                         claim.res_amt = remaining_amt
#                         claim.save()
#                         serializer = ClaimCreateSerializer(claim)
#                         return Response(serializer.data, status=status.HTTP_201_CREATED)
#                     else:
#                         claim.status = 'R'
#                         claim.res_amt = latest_claim_instance.res_amt
#                         claim.save()
#                         serializer = ClaimCreateSerializer(claim)
#                         return Response(serializer.data, status=status.HTTP_201_CREATED)
#                 else:
#                     claim.status = 'I'
#                     claim.res_amt -= claim.amt
#                     claim.save()
#                     serializer = ClaimCreateSerializer(claim)
#                     return Response(serializer.data, status=status.HTTP_201_CREATED)
#             else:
#                 claim.status = 'R'
#                 claim.save()
#                 serializer = ClaimCreateSerializer(claim)
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
