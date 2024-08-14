from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.cache import cache

from comments_app.models import Comment

User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    captcha_text = serializers.CharField(write_only=True, required=False)
    parent_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    image = serializers.ImageField(required=False, allow_null=True)
    file = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = Comment
        fields = ['username', 'email', 'parent_id', 'home_page', 'captcha_text', 'text', 'image', 'file']

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        captcha_text = attrs.get('captcha_text')
        file = attrs.get('file')
        image = attrs.get('image')

        if str(image) != 'None' and str(image).split('.')[1] not in ['jpg', 'jpeg', 'png', 'gif']:
            raise serializers.ValidationError({'image': 'The image not allowed extension'})

        if file and file.size > 100 * 1024:
            raise serializers.ValidationError({'file': 'The file size should not exceed 100KB.'})
        elif str(file) != 'None' and str(file).split('.')[1] != 'txt':
            raise serializers.ValidationError({'file': 'The file not txt extension'})

        try:
            user = User.objects.get(username=username)
            if user.email != email:
                raise serializers.ValidationError({
                    'email': 'Wrong email for this username'
                })
            elif not cache.get(captcha_text):
                raise serializers.ValidationError({'captcha_text': 'Invalid captcha text'})
        except User.DoesNotExist:
            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError({
                    'email': 'Email already exists'
                })
            elif not cache.get(captcha_text):
                raise serializers.ValidationError({'captcha_text': 'Invalid captcha text'})
        return attrs

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
        fields = ['id', 'username', 'email', 'home_page', 'text', 'created_at']


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentDetailSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    replies = RecursiveField(many=True)

    class Meta:
        model = Comment
        fields = ['id', 'username', 'user', 'home_page', 'text', 'created_at', 'replies']
