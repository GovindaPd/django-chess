from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/clearcache/', include('clearcache.urls')),
    path('', include('chesswithfriends.urls')),
    # path('routerhandling/', include('routerhandling.urls')),
]
