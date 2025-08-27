from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Patient, Doctor, PatientDoctorMapping
from .serializers import (
    UserRegistrationSerializer,
    PatientSerializer,
    DoctorSerializer,
    PatientDoctorMappingSerializer,
)
from .permissions import IsAdminOrReadOnly # --- NEW ---

# ... (UserRegistrationView and UserLoginView are unchanged)
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

class UserLoginView(TokenObtainPairView):
    permission_classes = [AllowAny]


# ... (PatientViewSet is unchanged)
class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Patient.objects.filter(created_by=self.request.user)
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


# --- Doctor Management Views (UPDATED) ---
class DoctorViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing doctor instances.
    - All authenticated users can view doctors.
    - Only admin (staff) users can create, update, or delete doctors.
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    # --- PERMISSION UPDATED ---
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


# ... (Mapping views are unchanged)
class PatientDoctorMappingView(generics.ListCreateAPIView):
    # ...
    pass
class PatientDoctorsListView(generics.ListAPIView):
    # ...
    pass
class MappingDeleteView(generics.DestroyAPIView):
    # ...
    pass