from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Review
from .serializers import ReviewSerializer
from book.models import Book

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request):
    book_id = request.data.get('book_id')
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

    data = {
        'user': request.user.id,  # 현재 로그인한 사용자
        'book': book.id,  # book_id 대신 book 객체의 id
        'content': request.data.get('content'),
        'rating': request.data.get('rating'),
    }

    serializer = ReviewSerializer(data=data)  # 변경된 data 사용
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_reviews(request):
    reviews = Review.objects.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)
