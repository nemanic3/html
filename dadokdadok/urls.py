from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView  # ✅ JWT 관련 추가
from user import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('book/', include('book.urls')),  # ✅ 도서 관리 관련 URL
    path('reviews/', include('review.urls')),
    path('goal/', include('goal.urls')),
    path('recommendation/', include('recommendation.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # ✅ JWT 토큰 발급
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # ✅ JWT 토큰 갱신
    path('', views.home, name='home'),  # 루트 URL에 home 뷰 연결
]
