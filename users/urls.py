from django.urls import path, include

urlpatterns = [
    path('api-auth/', include('djoser.urls')),
    path('token-auth/', include('djoser.urls.jwt')),
]