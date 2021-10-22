from django.urls import path
from . import views

urlpatterns = [
    path('verify_identity/', views.verify_identity),
    path('add_kyc/', views.upload_doc),
    # path('add_bank_details/', views.add_bank_details),
    path('all_address/', views.all_addresses),
    path('address/', views.user_address),
    path('address/<int:user_id>', views.address),
    path('all_profiles/', views.all_user_profile),
    path('profiles/', views.user_profile),
    path('profiles/<int:user_id>', views.profile_detail),
    path('all_handles/', views.all_handles),
    path('social_media_handle/', views.user_social_media),
    path('social_media_handle/<int:user_id>', views.social_media_detail),
    path('employement_history/', views.employment_history),
    path('all_employment_history/', views.all_employment_history),
    path('employement_history/<int:user_id>', views.employement_history_detail),
    path('unemployed/', views.unemployed),
    path('add_tertiary_institution/',views.add_tertiary_institution),
    path('add_high_school/',views.add_high_school),
    path('learning_pathway/',views.add_pathway),
    path('laptop_detail/',views.laptop_detail)
]