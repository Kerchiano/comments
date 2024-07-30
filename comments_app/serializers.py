from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.cache import cache

from comments_app.models import Comment

User = get_user_model()


class CaptchaSerializer(serializers.Serializer):
    captcha_text = serializers.CharField(max_length=10, required=True, label="Captcha Text")

    def validate_captcha_text(self, value):
        if not cache.get(value):
            raise serializers.ValidationError('Invalid captcha text')
        return value


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    captcha_text = serializers.CharField(write_only=True, required=False)
    parent_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Comment
        fields = ['username', 'email', 'parent_id', 'home_page', 'captcha_text', 'text']

    def validate_captcha_text(self, value):
        if not cache.get(value):
            raise serializers.ValidationError('Invalid captcha text')
        return value

    def create(self, validated_data):
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        captcha_text = validated_data.pop('captcha_text')
        parent_id = validated_data.pop('parent_id', None)

        user, created = User.objects.get_or_create(username=username, defaults={'email': email})

        if not created and user.email != email:
            user.email = email
            user.save()

        cache.delete(captcha_text)

        parent = None
        if parent_id:
            try:
                parent = Comment.objects.get(id=parent_id)
            except Comment.DoesNotExist:
                raise serializers.ValidationError('Parent comment does not exist')

        comment = Comment.objects.create(user=user, parent=parent, **validated_data)
        return comment


class TitleCommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M')

    class Meta:
        model = Comment
        fields = ['username', 'email', 'home_page', 'text', 'created_at']


class CommentDetailSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'home_page', 'text', 'created_at', 'replies']

    def get_replies(self, obj):
        replies = obj.replies.all()
        return TitleCommentSerializer(replies, many=True).data
