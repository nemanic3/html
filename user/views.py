from django.shortcuts import render

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
import json
from .models import CustomUser

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            nickname = request.POST.get('nickname')
            email = request.POST.get('email')
            student_id = request.POST.get('student_id')

            # 유효성 검사
            if CustomUser.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already exists'}, status=400)
            if CustomUser.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email already exists'}, status=400)
            if CustomUser.objects.filter(nickname=nickname).exists():
                return JsonResponse({'error': 'Nickname already exists'}, status=400)
            if CustomUser.objects.filter(student_id=student_id).exists():
                return JsonResponse({'error': 'Student ID already exists'}, status=400)

            # 사용자 생성
            user = CustomUser.objects.create(
                username=username,
                password=make_password(password),  # 비밀번호 암호화
                nickname=nickname,
                email=email,
                student_id=student_id
            )

            return redirect('signup_success')
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    elif request.method == 'GET':
        return render(request, 'user/signup.html')

def signup_success(request):
    return render(request, 'user/signup_success.html')


from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            # 사용자 인증
            user = authenticate(username=username, password=password)
            if user is None:
                return JsonResponse({'error': 'Invalid credentials'}, status=401)

            # JWT 토큰 발급
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                "token": str(refresh.access_token)
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return render(request, 'user/login.html')

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_user(request):
    logout(request)
    return redirect('/')


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user
    return Response({
        "id": user.id,
        "username": user.username,
        "nickname": user.nickname,
        "email": user.email
    })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    confirm = request.data.get('confirm')
    if confirm != "yes":
        return Response({"error": "Please confirm account deletion by sending 'confirm: yes' in the request body."}, status=400)

    user = request.user
    username = user.username
    user.delete()
    return Response({"message": f"The account '{username}' has been successfully deleted."}, status=200)

from django.contrib.auth.decorators import login_required

@login_required
def my_page(request):
    return render(request, 'user/mypage.html', {'user': request.user})



def home(request):
    return render(request, 'home.html')
