from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required,user_passes_test
from django.shortcuts import render
from home.models import *
from .forms import *
def admin_check(user):
    return user.is_staff

@login_required(login_url="login")
@user_passes_test(admin_check)
def AdminHome(request):
    
    total_user = User.objects.all().count()
    # print(total_user)
    accepted_claims = Claims.objects.filter(status='Accepted').count()
    # print(accepted_claims)
    rejected_claims = Claims.objects.filter(status='Rejected').count()
    initiated_claims = Claims.objects.filter(status='Initiated').count()


    count_of_claims=Claims.objects.all().count()
    count_of_policys=Policys.objects.all().count()



    context={"total_user":total_user,"accepted_claims":accepted_claims,"rejected_claims":rejected_claims,"admin_count_of_claims":count_of_claims,"admin_count_of_policys":count_of_policys,"initiated_claims":initiated_claims}
    return render(request, "adminindex.html",context)


@login_required(login_url="login")
@user_passes_test(admin_check)
def AdminReadPolicy(request):
    try:
        admin_policys=Policys.objects.all()
        context = {"admin_policys": admin_policys}
    except:
        context = {"admin_policys":"None"}

    return render(request,"adminpolicytable.html",context)



@login_required(login_url="login")
@user_passes_test(admin_check)
def AdminCreatePolicy(request):
    if request.method == 'POST':
        form = AdminPolicyForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a success page or any other page
            return redirect('ReadAdminPolicy')
    else:
        form = AdminPolicyForm()
    
    context = {'form': form}
    return render(request, 'addpolicy.html', context)



@login_required(login_url="login")
@user_passes_test(admin_check)
def AdminDeletePolicy(request, id):
    policy = get_object_or_404(Policys, policy_number=id)
    
    policy.delete()
    return redirect('ReadAdminPolicy')  # Redirect to the home page or any other desired URL after deletion
    
@login_required(login_url="login")
@user_passes_test(admin_check)
def AdminUpdatePolicy(request, id):
    policy = get_object_or_404(Policys, policy_number=id)
    form = AdminPolicyForm(request.POST or None, instance=policy)
    if form.is_valid():
        form.save()
        return redirect('ReadAdminPolicy')  # Redirect to the home page or any other desired URL after update
    return render(request, 'admin_update_policy.html', {'form': form})





@login_required(login_url="login")
@user_passes_test(admin_check)
def AdminReadClaim(request):
    try:
        admin_claims = Claims.objects.all()
        context = {"admin_claims": admin_claims}
    except:
        context = {"admin_claims": "None"}

    return render(request, "adminclaimtable.html", context)


@login_required(login_url="login")
@user_passes_test(admin_check)
def AdminCreateClaim(request):
    if request.method == 'POST':
        form = AdminClaimForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a success page or any other page
            return redirect('ReadAdminClaim')
    else:
        form = AdminClaimForm()

    context = {'form': form}
    return render(request, 'adminaddclaim.html', context)


@login_required(login_url="login")
@user_passes_test(admin_check)
def AdminDeleteClaim(request, id):
    claim = get_object_or_404(Claims, claim_id=id)

    claim.delete()
    return redirect('ReadAdminClaim')  # Redirect to the home page or any other desired URL after deletion


@login_required(login_url="login")
@user_passes_test(admin_check)
def AdminUpdateClaim(request, id):
    claim = get_object_or_404(Claims, claim_id=id)
    form = AdminClaimForm(request.POST or None, instance=claim)
    if form.is_valid():
        form.save()
        return redirect('ReadAdminClaim')  # Redirect to the home page or any other desired URL after update
    return render(request, 'admin_update_claim.html', {'form': form})
