from rest_framework import routers

from .mypage_blog_edit import MypageBlogViewset

router = routers.DefaultRouter()

router.register(r'blog', MypageBlogViewset, basename='mypage-blog')
