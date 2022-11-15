from rest_framework.serializers import ModelSerializer
from .models import CustomUser,Profile

class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
