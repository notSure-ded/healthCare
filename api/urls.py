from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserRegistrationView,
    UserLoginView,
    PatientViewSet,
    DoctorViewSet,
    PatientDoctorMappingView,
    PatientDoctorsListView,
    MappingDeleteView,
)

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'doctors', DoctorViewSet, basename='doctor')

# The API URLs are determined automatically by the router.
urlpatterns = [
    # Authentication URLs
    path('auth/register/', UserRegistrationView.as_view(), name='register'),
    path('auth/login/', UserLoginView.as_view(), name='login'),
    
    # ViewSet URLs
    path('', include(router.urls)),

    # Mapping URLs
    path('mappings/', PatientDoctorMappingView.as_view(), name='patient-doctor-mapping-list-create'),
    path('mappings/<int:patient_id>/', PatientDoctorsListView.as_view(), name='patient-doctors-list'),
    path('mappings/delete/<int:pk>/', MappingDeleteView.as_view(), name='mapping-delete'),
]