from django.urls import path, include
from rest_framework import routers

from module.ApiBlog import views_didivu as blogViews
from module.ApiBlog import views_fxeater as blogFXViews

from core.user.viewsets import UserViewSet, CurrentUserViewSet, UserProfileImageViewset
from core.auth.viewsets import LoginViewSet, RegistrationViewSet, RefreshViewSet

from module.ApiBlog import urls as MypageBlogUrls

from module.ApiBlog.test import TestView

router = routers.DefaultRouter()

# AUTHENTICATION
router.register(r'auth/login', LoginViewSet, basename='auth-login')
router.register(r'auth/register', RegistrationViewSet,
                basename='auth-register')
router.register(r'auth/refresh', RefreshViewSet, basename='token-refresh')

# USER
router.register(r'users', UserViewSet, basename='user')
router.register(r'me', CurrentUserViewSet, basename='me')
router.register(r'img/profile', UserProfileImageViewset,
                basename='user-profile-img')

# BLOG
router.register(r'api-blog', blogViews.BlogViewset, basename='blog-all')
router.register(r'my-blog', blogViews.MyBlogViewset, basename='my-blog')
router.register(r'api-publish-blog', blogViews.UpdateBlogStatusViewset,
                basename='blog-publish')

router.register(r'api-blog-home', blogViews.BlogHomeViewset,
                basename='blog-home')
router.register(r'api-blog-like',
                blogViews.BlogLikeCountViewSet, basename='blog-like')
router.register(r'api-reply', blogViews.ReplyViewset, basename='blog-reply')
router.register(r'api-series', blogViews.SeriesViewset, basename='blog-series')

# BLOG FXEATER
router.register(r'api-blog-fxeater', blogFXViews.BlogViewset,
                basename='blog-all-fxeater')
router.register(r'my-blog-fxeater', blogFXViews.MyBlogViewset,
                basename='my-blog-fxeater')
router.register(r'api-publish-blog-fxeater', blogFXViews.UpdateBlogStatusViewset,
                basename='blog-publish-fxeater')

router.register(r'api-blog-fxeater-home', blogFXViews.BlogHomeViewset,
                basename='blog-home-fxeater')
router.register(r'api-blog-fxeater-like',
                blogFXViews.BlogLikeCountViewSet, basename='blog-like-fxeater')
router.register(r'api-reply-fxeater', blogFXViews.ReplyViewset,
                basename='blog-reply-fxeater')
router.register(r'api-series-fxeater', blogFXViews.SeriesViewset,
                basename='blog-series-fxeater')


router.register(r'test', TestView,
                basename='test-view')

urlpatterns = [
    path('', include(router.urls)),
    path('mypage/', include(MypageBlogUrls.router.urls)),
]
