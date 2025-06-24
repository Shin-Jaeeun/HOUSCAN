from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/accounts/', include('accounts.urls')),  
    path('api/v1/products/', include('products.urls')),
    path('api/v1/houses/', include('houses.urls')),
    path('api/v1/community/', include('community.urls')),
]
