from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import OTP
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken 
from django.contrib.auth import password_validation
from django.contrib.auth import get_user_model
import re

User=get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length =250)
    address = serializers.ReadOnlyField()
    employment_details = serializers.ReadOnlyField()
    profile = serializers.ReadOnlyField()
    social_media_handle =  serializers.ReadOnlyField()
    tertiary_institution= serializers.ReadOnlyField()
    high_school = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields =['id', 'firstname', 'lastname', 'email', 'phone','password','how_did_you_hear_about_us', 'is_admin', 'is_active', 'has_work_experience','identity_verification', 'has_laptop','take_laptop_loan','has_verified_email','has_added_address', 'has_added_handles', 'has_added_profile', 'has_added_employment_detail','has_added_academic_detail', 'has_added_training_pathway','has_added_laptop_detail','has_added_kyc','checklist_count', 'auth_provider', 'address','profile','social_media_handle','employment_details','tertiary_institution','high_school','completed_nysc','nysc_not_applicable_reason','training_path','kyc_detail','date_joined']
        
        
    # def validate_password(self, value):
    #     if re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', value):
    #         return value
    #     else:
    #         raise serializers.ValidationError(detail='Please enter a strong password. At least 8 characters.')

class ChangePasswordSerializer(serializers.Serializer):
    old_password  = serializers.CharField(max_length=200)
    new_password  = serializers.CharField(max_length=200)
    confirm_password  = serializers.CharField(max_length=200)
    
    
    def check_pass(self):
        """ checks if both passwords are the same """
        if self.validated_data['new_password'] != self.validated_data['confirm_password']:
            raise serializers.ValidationError({"error":"Please enter matching passwords"})
        return True
            
 


# class CookieTokenRefreshSerializer(TokenRefreshSerializer):
#     refresh = None
#     def validate(self, attrs):
#         attrs['refresh'] = self.context['request'].COOKIES.get('refresh')
#         if attrs['refresh']:
#             return super().validate(attrs)
#         else:
#             raise InvalidToken('No valid token found in cookie \'refresh_token\'')