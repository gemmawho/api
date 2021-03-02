from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import (
    CommentViewSet,
    ReviewViewSet,
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    UserViewSet,
    get_jwt_token,
    send_confirmation_code
)

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet)
router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('titles/(?P<title_id>[0-9]+)/reviews', ReviewViewSet, basename='reviews')
router_v1.register('titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments', CommentViewSet,
                   basename='comments')

auth_patterns = [
    path('email/', send_confirmation_code, name='send_confirmation_code'),
    path('token/', get_jwt_token, name='get_jwt_token')
]

urlpatterns = [
    path('v1/auth/', include(auth_patterns)),
    path('v1/', include(router_v1.urls)),
]
