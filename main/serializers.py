from django.db.models.fields import TextField
from rest_framework import serializers
from .models import KYC, Address, BankDetails, HighSchool, SocialMedia, TertiaryInstitution, TrainingPathway, UserEmploymentDetail,  UserIdentity, UserProfile
from django.contrib.auth import get_user_model
import requests
from django.core.signing import Signer
from config import settings
import cloudinary

baseurl = 'https://vapi.verifyme.ng/v1/verifications/identities'
User = get_user_model()


def list_to_queryset(model, data):
    from django.db.models.base import ModelBase

    if not isinstance(model, ModelBase):
        raise ValueError(
            "%s must be Model" % model
        )
    if not isinstance(data, list):
        raise ValueError(
            "%s must be List Object" % data
        )

    pk_list = [obj.pk for obj in data]
    return model.objects.filter(pk__in=pk_list)

signer = Signer(key=settings.Common.SECRET_KEY)

class VerifyIdentity(serializers.ModelSerializer):

    class Meta:
        model = UserIdentity
        fields = '__all__'
        
        
    def check_identity(self, validated_data, request):
        
        user = request.user
        
        if user.identity_verification == True:
            raise serializers.ValidationError({"message":"Identity already verified"})
        else:
            
            identity_type =validated_data['identity_type'].lower()
            if identity_type == 'bvn':
                if len(validated_data['identity']) == 11:
                    url = baseurl+'/bvn/{}'.format(validated_data['identity'])
                    
                    data = {
                        "firstname":request.user.firstname,
                        "lastname":request.user.lastname,
                    }
                    
                    response = requests.post(url,headers={"Authorization": "Bearer {}".format(settings.Common.VERIFY_ME_KEY)}, data=data)
                else:
                    raise serializers.ValidationError({"bvn":["Invalid BVN"]})
            elif identity_type == 'nin':
                url = baseurl+'/nin/{}'.format(validated_data['identity'])
                data = {
                    "firstname":request.user.firstname,
                    "lastname":request.user.lastname,
                }
                
                response = requests.post(url,headers={"Authorization": "Bearer {}".format(settings.Common.VERIFY_ME_KEY)}, data=data)
                    
            else:
                raise serializers.ValidationError({"identity_type":"Must be either 'nin' or 'bvn'"})

            if response.json()["status"] == "success":
                identity = signer.sign_object(validated_data['identity'])
                UserIdentity.objects.create(identity_type = identity_type, identity=identity, user=user)
                user.identity_verification = True
                user.checklist_count+=1
                user.save()
                
                res = {
                    'status':True,
                    "message":"Identity Confirmed"
                }
                
            else:
                
                res = {
                    'status':False,
                    "message" : f"Unable to confirm your identity. Please ensure you have used your correct {identity_type}."
                }
                
            return res

class FileUploadSerializer(serializers.ModelSerializer):
    file = serializers.FileField()
    password = serializers.CharField()

    class Meta:
        model=KYC
        fields = ('id','file','state_of_residence', 'address', 'city', 'local_gov', 'doc_url', 'password')

    def upload(self, validated_data, request):
        if request.user.has_added_kyc==False:
            if 'user' in validated_data.keys():
                validated_data.pop('user')
            if 'doc_url' in validated_data.keys():
                validated_data.pop('doc_url')

            file = validated_data['file'] #get the image file from the request 
            img = cloudinary.uploader.upload(file, folder = 'SkillUP KYC/') #upload the image to cloudinary
            KYC.objects.create(**validated_data, doc_url=img['secure_url'], user=request.user)
            request.user.has_added_kyc =True
            request.user.checklist_count+=1
            request.user.save()
            

            return request.user
        else:
            raise serializers.ValidationError(detail="This checkpoint has been completed.")
        


class BankDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankDetails
        fields = '__all__'
        

class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserProfile
        fields = '__all__'
        

class AddressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Address
        fields = '__all__'
        
        
class SocialMediaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SocialMedia
        fields = '__all__'
        

class EmployeeListSerializer(serializers.ListSerializer):
    
    def save_data(self, validated_data, request):
        
        employment_detail = []
        for data in validated_data:
            if 'user' in data.keys():
                data.pop('user')
            employment_detail.append(UserEmploymentDetail.objects.create(**data, user=request.user))
         
        # request.user.has_work_experience = True
        # request.user.checklist_count+=1
        # request.user.save()   
        return list_to_queryset(UserEmploymentDetail,employment_detail)
    
    
class UserEmploymentDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserEmploymentDetail
        fields = '__all__'
        list_serializer_class = EmployeeListSerializer
        
    
class TertiaryInstitutionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TertiaryInstitution
        fields = '__all__'
  
class HighSchoolSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = HighSchool
        fields = '__all__'   
           

class AddInstitutionSerializer(serializers.Serializer):
    tertiary = TertiaryInstitutionSerializer(many=True)
    completed_nysc = serializers.CharField(max_length=200)
    nysc_not_applicable_reason = serializers.CharField(required=False, max_length=5000)
    
    
    def save_institution(self, validated_data,request):
        if request.user.has_added_academic_detail == False:
            institutions = validated_data.pop('tertiary')
            for institution in institutions:
                i = []
                if 'user' in institution.keys():
                    institution.pop('user')
                i.append(TertiaryInstitution(**institution, user=request.user))
            TertiaryInstitution.objects.bulk_create(i)
            request.user.completed_nysc = validated_data['completed_nysc']
            request.user.nysc_not_applicable_reason = validated_data['nysc_not_applicable_reason']
            request.user.has_added_academic_detail=True
            request.user.checklist_count+=1
            request.user.save()
            return request.user 
        else:
            raise serializers.ValidationError(detail="This checkpoint has been completed.")
        

class AddHighSchoolSerializer(serializers.Serializer):
    highschool = HighSchoolSerializer(many=True)
    
    def save_highschool(self, validated_data,request):
        if request.user.has_added_academic_detail == False:
            schools = validated_data.pop('highschool')
            for school in schools:
                i = []
                if 'user' in school.keys():
                    school.pop('user')
                i.append(HighSchool(**school, user=request.user))
            HighSchool.objects.bulk_create(i)
            request.user.has_added_academic_detail=True
            request.user.checklist_count+=1
            request.user.save()
            return request.user 
        else:
            raise serializers.ValidationError(detail="This checkpoint has been completed.")
          

class PathWaySerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingPathway
        fields = '__all__'
        
        
    def save_pathway(self, validated_data,request):
        if request.user.has_added_training_pathway == False:

            if 'user' in validated_data.keys():
                validated_data.pop('user')
            TrainingPathway.objects.create(**validated_data, user=request.user)
            request.user.has_added_training_pathway=True
            request.user.checklist_count+=1
            request.user.save()
            return request.user 
        else:
            raise serializers.ValidationError(detail="This checkpoint has been completed.")
        
        
class LaptopLoanSerializer(serializers.Serializer):
    has_laptop = serializers.BooleanField()
    take_laptop_loan = serializers.BooleanField(required=False)
    
    def save_laptop_detail(self, validated_data, request):
        if request.user.has_added_laptop_detail == False:
            request.user.has_laptop = validated_data['has_laptop']
            request.user.take_laptop_loan = validated_data['take_laptop_loan']
            request.user.has_added_laptop_detail = True
            request.user.checklist_count +=1
            request.user.save()
            
            return request.user
        else:
            raise serializers.ValidationError(detail="This checkpoint has been completed.")
        

  
