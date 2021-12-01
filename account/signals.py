from account.serializers import UserSerializer
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
import pyotp
from .models import OTP
from config import settings
from rest_framework import serializers
from django.template.loader import render_to_string
import random
from django.utils import timezone
from datetime import datetime

# totp = pyotp.TOTP('base32secret3232', interval=18000)

def generate_code():
    code = [str(random.choice(range(0,10))) for i in range(6)]
    return ''.join(code)
   

User = get_user_model()

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    token = "https://skillupafrica.netlify.app/{}".format(reset_password_token.key)
    
    msg_html = render_to_string('forgot_password.html', {
                        'first_name': str(reset_password_token.user.firstname).title(),
                        'token':token})
    
    message= 'Hello {},\n\nYou are receiving this message because you or someone else have requested the reset of the password for your account.\nPlease click on the following link, or paste this into your browser to complete the process within 24hours of receiving it:\n{}\n\nPlease if you did not request this please ignore this e-mail and your password would remain unchanged.\n\nRegards,\nEDM Support'.format(reset_password_token.user.firstname, token)
    
    send_mail(
        subject = "RESET PASSWORD FOR SKILLUP AFRICA PORTAL",
        message= message,
        html_message=msg_html,
        from_email  = 'SKILLUP SUPPORT <hello@skillup.africa>',
        recipient_list= [reset_password_token.user.email]
    )
    
    
# @receiver(post_save, sender=User)
# def send_otp(sender, instance, created, **kwargs):
        
#     if created and instance.is_staff == False:
#         code = totp.now()
#         print(code)
#         subject = "ACCOUNT VERIFICATION FOR ENTERPRISE DATA MAP PLATFORM"
        
#         message = f"""Hi, {str(instance.firstname).title()}.
# Thank you for signing up!
# Complete your verification on the enterprise data map (EMD) portal with the OTP below:

#                 {code}        

# Expires in 60 seconds!

# Thank you,
# EDM Team                
# """   
#         msg_html = render_to_string('signup_email.html', {
#                         'first_name': str(instance.firstname).title(),
#                         'code':code})
        
#         email_from = settings.Common.DEFAULT_FROM_EMAIL
#         recipient_list = [instance.email]
#         send_mail( subject, message, email_from, recipient_list, html_message=msg_html)
        
#         OTP.objects.create(code=code, user=instance)
    
    

       
class OTPVerifySerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
    email = serializers.EmailField()
    
    
    def verify_otp(self):
        otp = self.validated_data['otp']
        email = self.validated_data['email']
        
        if OTP.objects.filter(code=otp).exists():
            try:
                otp = OTP.objects.get(code=otp, user__email = email)
            except Exception:
                OTP.objects.filter(code=otp).delete()
                raise serializers.ValidationError(detail='Cannot verify otp. Please try later')
            
            if otp.is_expired():
                raise serializers.ValidationError(detail='OTP expired')
                
            else:
                if otp.user.has_verified_email == False:
                    otp.user.has_verified_email=True
                    otp.user.checklist_count+=1
                    otp.user.save()
                    
                    #clear all otp for this user after verification
                    # all_otps = OTP.objects.filter(user=otp.user)
                    # all_otps.delete()
                    
                    serializer = UserSerializer(otp.user)
                    return {'message': 'Verification Complete', 'data':serializer.data}
                else:
                    raise serializers.ValidationError(detail='User with this otp has been verified before.')
                
                    
        
        else:
            raise serializers.ValidationError(detail='Invalid OTP')
        
        
class OtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
     
    def get_otp(self):
        try:
            user = User.objects.get(email=self.validated_data['email'], is_active=True, has_verified_email=False)
        except User.DoesNotExist:
            raise serializers.ValidationError(detail='Please confirm that the email is correct or email has not been verified.')
        
        code = generate_code()
        expiry_date = timezone.now() + timezone.timedelta(minutes=5)
        
        OTP.objects.create(code=code, user=user, expiry_date=expiry_date)
        subject = "Verify Email for Skill Up Application"
        
        message = f"""Hi, {str(user.firstname).title()}.

    Complete your verification on the enterprise data map (EMD) portal with the OTP below:

                    {code}        


    Thank you,
    Skill up Team                
    """
        msg_html = render_to_string('new_otp.html', {
                        'first_name': str(user.firstname).title(),
                        'code':code})
        
        email_from = settings.Common.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        send_mail( subject, message, email_from, recipient_list, html_message=msg_html)
        
        return {'message': 'Please check your email for OTP.'}
        
        
        
        