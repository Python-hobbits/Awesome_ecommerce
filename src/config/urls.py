"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from src.apps.orders.views import ThankYouView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("src.apps.content.urls")),
    path("account/", include("src.apps.user.urls")),
    path("basket/", include("src.apps.basket.urls")),
    path("inventory/", include("src.apps.inventory.urls")),
    path("checkout/", include("src.apps.orders.urls")),
    path("thank_you/<int:order_id>/", ThankYouView.as_view(), name="thank_you"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += path("__debug__/", include("debug_toolbar.urls"))
