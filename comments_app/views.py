from django.core.cache import cache
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser

from comments_app.filters import CommentFilter
from comments_app.models import Comment
from comments_app.serializers import CommentSerializer, TitleCommentSerializer, \
    CommentDetailSerializer
from comments_app.utils import generate_captcha_text, get_captcha_image


class GenerateCaptchaView(APIView):
    def get(self, request, *args, **kwargs):
        text = generate_captcha_text()
        cache.set(text, True, timeout=300)

        image = get_captcha_image(text)
        return HttpResponse(image, content_type='image/png')


class CommentCreateView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    parser_classes = [MultiPartParser]


class CommentListView(ListAPIView):
    queryset = Comment.objects.filter(parent__isnull=True).order_by('-created_at')
    serializer_class = TitleCommentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CommentFilter
    ordering_fields = ['user__username', 'user__email', 'created_at']


class CommentDetailView(RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer
