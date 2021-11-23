from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import ValidationError
from .models import Address, BankDetails, SocialMedia, UserEmploymentDetail, UserProfile
from .serializers import AddHighSchoolSerializer, AddInstitutionSerializer, AddressSerializer, BankDetailsSerializer, LaptopLoanSerializer, PathWaySerializer, SocialMediaSerializer, UserEmploymentDetailSerializer, UserProfileSerializer, VerifyIdentity, FileUploadSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model, authenticate
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from account.serializers import UserSerializer


from main import serializers

User=get_user_model()
#for all check list, add logic to check if that check list has been done beofre doing it 


@swagger_auto_schema(methods=['POST'], request_body=VerifyIdentity())
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def verify_identity(request):
    if request.method == 'POST':
        
        serializer = VerifyIdentity(data = request.data)

        if serializer.is_valid():
            res = serializer.check_identity(serializer.validated_data, request)
            
            return Response(res, status = status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['POST'], request_body=FileUploadSerializer())
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def upload_doc(request):
    if request.method == 'POST':
        
        
        serializer = FileUploadSerializer(data = request.data)
        

        if serializer.is_valid():
            password = serializer.validated_data.pop('password')
            auth_user = authenticate(request.user.email, password)
            if auth_user and auth_user == request.user:
                user = serializer.upload(serializer.validated_data, request)
                
                user_serializer = UserSerializer(user)
                data = {
                    'status' : True,
                    'message' : 'Upload Successful',
                    'data' : user_serializer.data,
                }
                

                return Response(data, status = status.HTTP_200_OK)
            else:
                raise ValidationError(detail="Password is incorrect.")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# def add_bank_details(request):
#     if request.method == 'POST':
        
        
#         serializer = BankDetailsSerializer(data = request.data)
        

#         if serializer.is_valid():
            
#             serializer.save()

#             data = {
#                 'status' : True,
#                 'message' : 'Upload Successful',
#                 'data' : serializer.data,
#             }
            

#             return Response(data, status = status.HTTP_200_OK)

#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
   
@swagger_auto_schema(method='post', request_body=AddressSerializer())
@api_view(['POST'])     
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_address(request):
    if request.method == 'POST':
        serializer = AddressSerializer(data=request.data)
        
        if serializer.is_valid():
            
            if request.user.has_added_address:
                data = {
                'status' : True,
                'message' : 'cannot add multiple addresses',
                }
                

                return Response(data, status = status.HTTP_400_BAD_REQUEST)
            else:
                if 'user' in serializer.validated_data.keys():
                    serializer.validated_data.pop('user')
                address = Address.objects.create(**serializer.validated_data, user=request.user)
                request.user.has_added_address =True
                request.user.checklist_count+=1
                request.user.save()
            
                serializer = AddressSerializer(address)
                data = {
                    'status' : True,
                    'message' : 'success',
                    'data' : serializer.data,
                }
                

                return Response(data, status = status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    
@api_view(['GET', 'PUT', 'DELETE'])
def address(request, user_id):
    try:
        user=User.objects.get(id=user_id, is_active=True)
        address_=Address.objects.get(user=user, is_active=True)
    except User.DoesNotExist:
        data ={
            'error':'user not found',
            'status':'failed'
        }
        
        return Response(data, status=status.HTTP_404_NOT_FOUND)
    except Address.DoesNotExist:
        data ={
            'error':'no address found for this user',
            'status':'failed'
        }
        
        return Response(data, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = AddressSerializer(address_)
        data = {
            'status' : True,
            'message' : 'success',
            'data' : serializer.data,
        }
        

        return Response(data, status = status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = AddressSerializer(address_, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = {
            'status' : True,
            'message' : 'success',
            'data' : serializer.data,
            }


            return Response(data, status = status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    elif request.method == 'DELETE':
        address_.delete()
        return Response({'message':'success'}, status=status.HTTP_204_NO_CONTENT)
     
    
@api_view(['GET'])
def all_addresses(request):
         
    if request.method == 'GET':
        addresses = Address.objects.filter(is_active=True)
        serializer = AddressSerializer(addresses, many=True)
        data = {
            'status' : True,
            'message' : 'success',
            'data' : serializer.data,
        }
        

        return Response(data, status = status.HTTP_200_OK)
    
    
@api_view(['GET'])
def all_user_profile(request):
    if request.method == 'GET':
        profiles = UserProfile.objects.filter(is_active=True)
        
        serializer = UserProfileSerializer(profiles, many=True)
        data = {
            'status' : True,
            'message' : 'success',
            'data' : serializer.data,
            }
        

        return Response(data, status = status.HTTP_200_OK)

@swagger_auto_schema(method='post',request_body=UserProfileSerializer())
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_profile(request):
    if request.method == 'POST':
        serializer = UserProfileSerializer(data=request.data) 
        
        if serializer.is_valid():
            if 'user' in serializer.validated_data.keys():
                serializer.validated_data.pop('user')
            profile = UserProfile.objects.create(**serializer.validated_data, user=request.user)
            serializer = UserProfileSerializer(profile)
            
            request.user.checklist_count+=1
            request.user.has_added_profile=True
            request.user.save()
            
            data = {
            'status' : True,
            'message' : 'success',
            'data' : serializer.data,
                }
            

            return Response(data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='put', request_body=UserProfileSerializer())
@api_view(['GET', 'PUT', 'DELETE'])
def profile_detail(request, user_id):
    try:
        user=User.objects.get(id=user_id, is_active=True)
        profile=UserProfile.objects.get(user=user, is_active=True)
    except User.DoesNotExist:
        data ={
            'error':'user not found',
            'status':'failed'
        }
        
        return Response(data, status=status.HTTP_404_NOT_FOUND)
    except UserProfile.DoesNotExist:
        data ={
            'error':'no profile found for this user',
            'status':'failed'
        }
        
        return Response(data, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = UserProfileSerializer(profile)
        data = {
            'status' : True,
            'message' : 'success',
            'data' : serializer.data,
        }
        

        return Response(data, status = status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = {
            'status' : True,
            'message' : 'success',
            'data' : serializer.data,
            }


            return Response(data, status = status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    elif request.method == 'DELETE':
        profile.delete()
        return Response({'message':'success'}, status=status.HTTP_204_NO_CONTENT)
     

   
@api_view(['GET'])
def all_handles(request):
    if request.method == 'GET':
        handles = UserProfile.objects.filter(is_active=True)
        
        serializer = SocialMediaSerializer(handles, many=True)
        data = {
            'status' : True,
            'message' : 'success',
            'data' : serializer.data,
            }
        

        return Response(data, status = status.HTTP_200_OK)
    
@swagger_auto_schema(method='post', request_body=SocialMediaSerializer())
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_social_media(request):
    if request.method == 'POST':
        serializer = SocialMediaSerializer(data=request.data) 
        
        if serializer.is_valid():
            if 'user' in serializer.validated_data.keys():
                serializer.validated_data.pop('user')
            handles = SocialMedia.objects.create(**serializer.validated_data, user=request.user)
            request.user.checklist_count+=1
            request.user.has_added_handles=True
            request.user.save()
            
            serializer=SocialMediaSerializer(handles)
            data = {
            'status' : True,
            'message' : 'success',
            'data' : serializer.data,
                }
            

            return Response(data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='put', request_body=SocialMediaSerializer())
@api_view(['GET', 'PUT', 'DELETE'])
def social_media_detail(request, user_id):
    try:
        user=User.objects.get(id=user_id, is_active=True)
        handle=SocialMedia.objects.get(user=user, is_active=True)
    except User.DoesNotExist:
        data ={
            'error':'user not found',
            'status':'failed'
        }
        
        return Response(data, status=status.HTTP_404_NOT_FOUND)
    except SocialMedia.DoesNotExist:
        data ={
            'error':'no social media handle found for this user',
            'status':'failed'
        }
        
        return Response(data, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = SocialMediaSerializer(handle)
        data = {
            'status' : True,
            'message' : 'success',
            'data' : serializer.data,
        }
        

        return Response(data, status = status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = SocialMediaSerializer(handle, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = {
            'status' : True,
            'message' : 'success',
            'data' : serializer.data,
            }

            return Response(data, status = status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    elif request.method == 'DELETE':
        handle.delete()
        return Response({'message':'success'}, status=status.HTTP_204_NO_CONTENT)
    
    
    

@api_view(['GET'])
def all_employment_history(request):
    if request.method == 'GET':
        obj = UserEmploymentDetail.objects.filter(is_active=True)
        
        serializer = UserEmploymentDetailSerializer(obj, many=True)
        data = {
            'status' : True,
            'message' : 'success',
            'data' : serializer.data,
            }
        

        return Response(data, status = status.HTTP_200_OK)
    
    
@swagger_auto_schema(method='post',request_body=UserEmploymentDetailSerializer())
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def employment_history(request):
    if request.method == 'POST':
        serializer = UserEmploymentDetailSerializer(data=request.data, many=True) 
        
        if serializer.is_valid():
            
            if request.user.has_added_employment_detail==False:
                serializer.save_data(serializer.validated_data,request)  
                request.user.has_added_employment_detail=True
                request.user.has_work_experience = True
                request.user.checklist_count+=1
                request.user.save()
                
                data = {
                    'status' : True,
                    'message' : 'success',
                    'data' : serializer.data,
                    }
                

                return Response(data, status = status.HTTP_201_CREATED)
            else:
                raise ValidationError(detail="Employment details already added for this user")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='put', request_body=UserEmploymentDetailSerializer())
@api_view(['GET', 'PUT', 'DELETE'])
def employement_history_detail(request, user_id):
    try:
        user=User.objects.get(id=user_id, is_active=True)
        obj=UserEmploymentDetail.objects.filter(user=user, is_active=True)
    except User.DoesNotExist:
        data ={
            'error':'user not found',
            'status':'failed'
        }
        
        return Response(data, status=status.HTTP_404_NOT_FOUND)
    except UserEmploymentDetail.DoesNotExist:
        data ={
            'error':'no employment history found for this user',
            'status':'failed'
        }
        
        return Response(data, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = UserEmploymentDetailSerializer(obj)
        data = {
            'status' : True,
            'message' : 'success',
            'data' : serializer.data,
        }
        

        return Response(data, status = status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = UserEmploymentDetailSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = {
            'status' : True,
            'message' : 'success',
            'data' : serializer.data,
            }

            return Response(data, status = status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    elif request.method == 'DELETE':
        obj.delete()
        return Response({'message':'success'}, status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def unemployed(request):
    
    if request.method == 'GET':
        
        if request.user.has_added_employment_detail == False:
            request.user.has_work_experience = False
            request.user.has_added_employment_detail=True
            request.user.save()
        
            return Response({'message':'success'}, status=status.HTTP_202_ACCEPTED)
        else:
            raise ValidationError(detail="Employment details already added for this user")
    

@swagger_auto_schema(method='post', request_body=AddInstitutionSerializer())
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])  
def add_tertiary_institution(request):
    if request.method == 'POST':
        serializer = AddInstitutionSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save_institution(serializer.validated_data, request)
            
            data = UserSerializer(user)
            return Response(data.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

@swagger_auto_schema(method='post', request_body=AddHighSchoolSerializer())
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])  
def add_high_school(request):
    if request.method == 'POST':
        serializer = AddHighSchoolSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save_highschool(serializer.validated_data, request)
            
            data = UserSerializer(user)
            return Response(data.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
              

@swagger_auto_schema(method='post', request_body=LaptopLoanSerializer())
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])  
def laptop_detail(request):
    if request.method == 'POST':
        serializer = LaptopLoanSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save_laptop_detail(serializer.validated_data, request)
            
            data = UserSerializer(user)
            return Response(data.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
@swagger_auto_schema(method='post', request_body=PathWaySerializer())
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])  
def add_pathway(request):
    if request.method == 'POST':
        serializer = PathWaySerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save_pathway(serializer.validated_data, request)
            
            data = UserSerializer(user)
            return Response(data.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)