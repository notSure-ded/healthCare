from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, Patient, Doctor, PatientDoctorMapping
from .serializers import (
    UserRegistrationSerializer,
    PatientSerializer,
    DoctorSerializer,
    PatientDoctorMappingSerializer,
)
# Make sure this import is present
from .permissions import IsAdminOrReadOnly 

# --- Authentication Views ---
class UserRegistrationView(generics.CreateAPIView):
    """
    API view for user registration.
    Allows any user (authenticated or not) to access this endpoint.
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

class UserLoginView(TokenObtainPairView):
    """
    API view for user login.
    Uses DRF Simple JWT's view to handle token generation.
    """
    permission_classes = [AllowAny]


# --- Patient Management Views ---
class PatientViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing patient instances.
    - Requires authentication.
    - Users can only see and manage patients they have created.
    """
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the patients
        for the currently authenticated user.
        """
        return Patient.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        """
        Assign the logged-in user as the creator of the patient.
        """
        serializer.save(created_by=self.request.user)


# --- Doctor Management Views ---
class DoctorViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing doctor instances.
    - All authenticated users can view doctors.
    - Only admin (staff) users can create, update, or delete doctors.
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    # Correct permission class to restrict editing to admins
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


# --- Patient-Doctor Mapping Views ---
class PatientDoctorMappingView(generics.ListCreateAPIView):
    """
    API view to create and list patient-doctor mappings.
    """
    queryset = PatientDoctorMapping.objects.all()
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            patient = Patient.objects.get(id=request.data.get('patient_id'), created_by=request.user)
        except Patient.DoesNotExist:
            return Response(
                {"error": "Patient not found or you do not have permission."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            doctor = Doctor.objects.get(id=request.data.get('doctor_id'))
        except Doctor.DoesNotExist:
            return Response(
                {"error": "Doctor not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        mapping = PatientDoctorMapping.objects.create(patient=patient, doctor=doctor)
        response_serializer = self.get_serializer(mapping)
        headers = self.get_success_headers(response_serializer.data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class PatientDoctorsListView(generics.ListAPIView):
    """
    API view to retrieve all doctors assigned to a specific patient.
    """
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

    # This method is now correctly indented within the class
    def get_queryset(self):
        patient_id = self.kwargs['patient_id']
        try:
            patient = Patient.objects.get(id=patient_id, created_by=self.request.user)
            doctor_ids = PatientDoctorMapping.objects.filter(patient=patient).values_list('doctor_id', flat=True)
            return Doctor.objects.filter(id__in=doctor_ids)
        except Patient.DoesNotExist:
            return Doctor.objects.none()

class MappingDeleteView(generics.DestroyAPIView):
    """
    API view to delete a specific patient-doctor mapping.
    """
    permission_classes = [IsAuthenticated]
    
    # Correctly indented get_queryset method
    def get_queryset(self):
        # Users can only delete mappings for patients they own.
        user = self.request.user
        return PatientDoctorMapping.objects.filter(patient__created_by=user)

