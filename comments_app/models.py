from django.contrib.auth import get_user_model
from django.core.validators import URLValidator, FileExtensionValidator
from django.db import models

User = get_user_model()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    home_page = models.URLField(validators=[URLValidator()], blank=True, null=True)
    text = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='comments/images/', blank=True, null=True, validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif']),
    ])
    file = models.FileField(upload_to='comments/files/', blank=True, null=True, validators=[
        FileExtensionValidator(allowed_extensions=['txt']),
    ])

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        if self.image:
            self.image = self.resize_image(self.image)
        super().save(*args, **kwargs)

    def resize_image(self, image):
        from PIL import Image
        from io import BytesIO
        from django.core.files.uploadedfile import SimpleUploadedFile

        img = Image.open(image)
        if img.height > 320 or img.width > 240:
            output_size = (320, 240)
            img.thumbnail(output_size)
            img_io = BytesIO()
            img.save(img_io, format=img.format)
            image_file = SimpleUploadedFile(image.name, img_io.getvalue(), content_type=image.file.content_type)
            return image_file
        return image
