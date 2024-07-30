from django.urls import path, include

from comments_app.views import GenerateCaptchaView, ValidateCaptchaView, CommentCreateView, CommentListView, \
    CommentDetailView

urlpatterns = [
    path('api/generate-captcha/', GenerateCaptchaView.as_view(), name='generate_captcha'),
    path('api/validate-captcha/', ValidateCaptchaView.as_view(), name='validate_captcha'),
    path('api/comments/', CommentCreateView.as_view(), name='comment-create'),
    path('api/title-comments/', CommentListView.as_view(), name='comment-create'),
    path('api/title-comments/<int:pk>/', CommentDetailView.as_view(), name='comment_detail'),
]
