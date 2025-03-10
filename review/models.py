from django.db import models
from user.models import CustomUser
from book.models import Book

class Review(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # 작성자
    book = models.ForeignKey(Book, on_delete=models.CASCADE)  # 대상 도서
    content = models.TextField(null=True, blank=True)  # 감상문 내용
    rating = models.FloatField(null=True, blank=True)  # 평점
    created_at = models.DateTimeField(auto_now_add=True)  # 작성 시간

    class Meta:
        db_table = 'review'

    def __str__(self):
        return f"{self.user.username}'s review of {self.book.title}"