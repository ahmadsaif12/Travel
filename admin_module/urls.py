from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Main apps with no prefix — set one base route (e.g. "app_name/")
    path('', include('apps.user_login.urls')),  # Routes like /login/, /dashboard/
    path('', include('apps.tourism_company.urls')),
  
    path('guides/', include('apps.Guides.urls')),
    path('',include('apps.tour_package.urls')),
    path('', include('apps.hotelbooking.urls')),
    path('', include('apps.bookings.urls')),
    path('', include('apps.reviews.urls')),
    path('', include('apps.social_community.urls')),
    path('', include('apps.expense_tracker.urls')),
    path('', include('apps.maps.urls')),
    path('', include('apps.social_stories.urls')),
]

# Serving media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
