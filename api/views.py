from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from home.models import Policys, Claims
from home.forms import ClaimForm
from home.serializers import *
import re

@api_view(['GET'])
def get_policys(request):
    if request.method == 'GET':
        policys = Policys.objects.filter(user=request.user)
        serializer = PolicySerializer(policys, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@api_view(['GET'])
def get_claims(request):
    if request.method == 'GET':
        claims = Claims.objects.filter(user=request.user)
        serializer = ClaimCreateSerializer(claims, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['POST'])
def post_create_claim(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ClaimForm(user=request.user, data=request.data)
            if form.is_valid():
                claim = form.save(commit=False)
                claim.user = request.user
                selected_policy = Policys.objects.get(policy_number=form.cleaned_data['policy_number'])
                claim.policy_number = form.cleaned_data['policy_number']
                claim.res_amt = selected_policy.coverage
                
                if claim.amt <= claim.res_amt:
                    if Claims.objects.filter(policy_number=form.cleaned_data['policy_number']).exists():
                        latest_claim_instance = Claims.objects.filter(policy_number=claim.policy_number).latest('created_at')
                        remaining_amt = latest_claim_instance.res_amt - claim.amt
                        if remaining_amt >= 0:
                            claim.status = 'Initiated'
                            claim.res_amt = remaining_amt
                            claim.save()
                            serializer = ClaimCreateSerializer(claim)
                            return Response(serializer.data, status=status.HTTP_201_CREATED)
                        else:
                            claim.status = 'Rejected'
                            claim.res_amt = latest_claim_instance.res_amt
                            claim.save()
                            serializer = ClaimCreateSerializer(claim)
                            return Response(serializer.data, status=status.HTTP_201_CREATED)
                    else:
                        claim.status = 'Initiated'
                        claim.res_amt -= claim.amt
                        claim.save()
                        serializer = ClaimCreateSerializer(claim)
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    claim.status = 'Rejected'
                    claim.save()
                    serializer = ClaimCreateSerializer(claim)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("User not authenticated", status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response("Method not allowed", status=status.HTTP_405_METHOD_NOT_ALLOWED)
    



@api_view(['POST'])
def signup_api(request):
    if request.method == "POST":
        first_name = request.data.get("firstname")
        last_name = request.data.get("lastname")
        user = request.data.get("Username")
        e_mail = request.data.get("email")
        password1 = request.data.get("password")
        confirmpassword = request.data.get("confirmpassword")

        # Check if any field is empty
        if not all([first_name, last_name, user, e_mail, password1, confirmpassword]):
            return Response({"error": "Please fill out all fields."}, status=400)

        if password1 == confirmpassword:
            if not User.objects.filter(username=user).exists():
                if not User.objects.filter(email=e_mail).exists():
                    # Check if the username contains at least one non-numeric character
                    if re.search("[a-zA-Z]", user):
                        # Check if the password is strong enough
                        if (len(password1) >= 8) and any(char.isdigit() for char in password1) and any(char.isalnum() for char in password1) and any(not char.isalnum() for char in password1):
                            user = User.objects.create_user(
                                username=user, email=e_mail, password=password1,
                                first_name=first_name, last_name=last_name
                            )
                            user.save()
                            return Response({"message": "Account Created!"}, status=201)
                        else:
                            return Response({"error": "Password must be at least be 8 characters long and contain at least one digit, one letter, and one special character."}, status=400)
                    else:
                        return Response({"error": "Username must contain at least one non-numeric character."}, status=400)
                else:
                    return Response({"error": "Email is already in use."}, status=400)
            else:
                return Response({"error": "Username is already taken."}, status=400)
        else:
            return Response({"error": "Passwords do not match."}, status=400)

    return Response({"error": "Method not allowed"}, status=405)



@api_view(['POST'])
def login_api(request):
    if request.method == "POST":
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"message": "Login successful!"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({"error": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)











# Admin API's
    
@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_policy_list(request):
    policies = Policys.objects.all()
    serializer = PolicySerializer(policies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_claim_list(request):
    claims = Claims.objects.all()
    serializer = ClaimSerializer(claims, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_policy(request):
    serializer = PolicySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_claim(request):
    serializer = ClaimSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_policy(request, pk):
    try:
        policy = Policys.objects.get(policy_id=pk)
    except Policys.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = PolicySerializer(policy, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_claim(request, pk):
    try:
        claim = Claims.objects.get(claim_id=pk)
    except Claims.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ClaimSerializer(claim, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_policy(request, pk):
    try:
        policy = Policys.objects.get(policy_id=pk)
    except Policys.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    policy.delete()
    return Response(status=status.HTTP_202_ACCEPTED)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_claim(request, pk):
    try:
        claim = Claims.objects.get(claim_id=pk)
    except Claims.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    claim.delete()
    return Response(status=status.HTTP_202_ACCEPTED)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_user_list(request):
    """
    Retrieve a list of all users.
    """
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
def claim_approval(request, pk):
    try:
        claim = Claims.objects.get(claim_id=pk)
        claim.status=request.data.get("status")
        claim.save()
        # print(claim)
        return Response(status=status.HTTP_201_CREATED)
    except Claims.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # print(request.data)
