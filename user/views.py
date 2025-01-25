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
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            nickname = data.get('nickname')
            email = data.get('email')

            # 유효성 검사
            if CustomUser.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already exists'}, status=400)
            if CustomUser.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email already exists'}, status=400)
            if CustomUser.objects.filter(nickname=nickname).exists():
                return JsonResponse({'error': 'Nickname already exists'}, status=400)

            # 사용자 생성
            user = CustomUser.objects.create(
                username=username,
                password=make_password(password),  # 비밀번호 암호화
                nickname=nickname,
                email=email
            )

            return JsonResponse({
                "id": user.id,
                "username": user.username,
                "nickname": user.nickname,
                "email": user.email
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

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
    user = request.user
    user.delete()
    return Response(status=204)
