from django.urls import include, path
from admission_enquiry import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', views.enquiry_form, name='home'),  # Default route for enquiry form
    path('admin/', admin.site.urls),
    path('payment/', views.payment, name='payment'),
    path('admission_enquiry/', include('admission_enquiry.urls')),  # Include app URLs
    # path('login/', auth_views.LoginView.as_view(template_name='admission_enquiry/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
