from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.contrib import messages
import re



@login_required(login_url="login")
# Create your views here.
def Home(request):
    

    accepted_claims = Claims.objects.filter(user=request.user, status='Accepted').count()
    rejected_claims = Claims.objects.filter(user=request.user, status='Rejected').count()
    initiated_claims = Claims.objects.filter(user=request.user, status='Initiated').count()


    count_of_claims=Claims.objects.filter(user=request.user).count()
    count_of_policys=Policys.objects.filter(user=request.user).count()


    context={"accepted_claims":accepted_claims,"rejected_claims":rejected_claims,"count_of_claims":count_of_claims,"count_of_policys":count_of_policys,"initiated_claims":initiated_claims}
    return render(request, "index.html",context)




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
                    # Check if the username contains at least one non-numeric character
                    if re.search("[a-zA-Z]", user):
                        user = User.objects.create_user(
                            username=user, email=e_mail, password=password1,
                            first_name=first_name, last_name=last_name
                        )
                        user.save()
                        messages.success(request, "Account Created!")
                        return redirect("login")
                    else:
                        messages.error(request, "Username must contain at least one non-numeric character.")
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
            if user.is_staff:
                return redirect("AdminHome")
            else:   
                return redirect("home")
        # premail,password)
        else:
            messages.error(request, "Error please check your credentials!")
            return redirect("login")
    else:
        return render(request, "login.html")


@login_required(login_url="login")
def logoutpage(request):
    # pr"logout")
    logout(request)
    messages.success(request, "Logged out successfully.")
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
                        claim.status = 'Initiated'
                        claim.res_amt = remaining_amt
                        claim.save()
                        messages.success(request, "Claim initiated successfully.")
                        
                        return redirect('getclaim')
                    else:
                        # If remaining_amt is negative, reject the claim
                        claim.status = 'Rejected'
                        claim.res_amt = latest_claim_instance.res_amt
                        claim.save()
                        messages.error(request, "Claim amount exceeds policy coverage. Claim rejected.")
                        
                        return redirect('getclaim')
                else:
                    # If no previous claims exist, deduct claim amount and save the claim
                    claim.status = 'Initiated'
                    claim.res_amt -= claim.amt
                    claim.save()
                    messages.success(request, "Claim initiated successfully.")
                   
                    return redirect('getclaim')
            
            # If claim amount exceeds res_amt, reject the claim
            claim.status = 'Rejected'
            claim.save()
            messages.error(request, "Claim amount exceeds policy coverage. Claim rejected.")
            return redirect('getclaim')
                
    context = {"form": form}
    return render(request, "addclaim.html", context)

