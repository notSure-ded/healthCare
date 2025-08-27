from rest_framework import serializers
from .models import User, Patient, Doctor, PatientDoctorMapping

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password')

    # --- NEW VALIDATION ---
    def validate_email(self, value):
        """
        Check that the email is not already in use.
        """
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email address already exists.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ('id', 'name', 'specialization', 'created_at')

class PatientSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.email')

    class Meta:
        model = Patient
        fields = ('id', 'name', 'date_of_birth', 'address', 'created_by', 'created_at')

class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    patient_id = serializers.IntegerField(write_only=True)
    doctor_id = serializers.IntegerField(write_only=True)
    
    patient = PatientSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = ('id', 'patient_id', 'doctor_id', 'patient', 'doctor', 'assigned_at')
        
    # --- NEW VALIDATION ---
    def validate(self, data):
        """
        Check that the mapping does not already exist.
        """
        patient_id = data.get('patient_id')
        doctor_id = data.get('doctor_id')
        if PatientDoctorMapping.objects.filter(patient_id=patient_id, doctor_id=doctor_id).exists():
            raise serializers.ValidationError("This patient is already assigned to this doctor.")
        return data

