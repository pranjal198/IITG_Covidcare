from django.contrib import admin
from django.urls import path
from hospital import views
from django.contrib.auth.views import LoginView,LogoutView


#-------------FOR ADMIN RELATED URLS
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view,name=''),


    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view),


    path('adminclick', views.adminclick_view),
    path('doctorclick', views.doctorclick_view),
    path('patientclick', views.patientclick_view),
    path('shopkeeperclick', views.shopkeeperclick_view),

    path('adminsignup', views.admin_signup_view),
    path('doctorsignup', views.doctor_signup_view,name='doctorsignup'),
    path('patientsignup', views.patient_signup_view),
    path('shopkeepersignup', views.shopkeeper_signup_view,name='shopkeepersignup'),
    
    path('adminlogin', LoginView.as_view(template_name='hospital/adminlogin.html')),
    path('doctorlogin', LoginView.as_view(template_name='hospital/doctorlogin.html')),
    path('patientlogin', LoginView.as_view(template_name='hospital/patientlogin.html')),
    path('shopkeeperlogin', LoginView.as_view(template_name='hospital/shopkeeperlogin.html')),


    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='hospital/index.html'),name='logout'),


    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),

    path('admin-doctor', views.admin_doctor_view,name='admin-doctor'),
    path('admin-view-doctor', views.admin_view_doctor_view,name='admin-view-doctor'),
    path('delete-doctor-from-hospital/<int:pk>', views.delete_doctor_from_hospital_view,name='delete-doctor-from-hospital'),
    path('update-doctor/<int:pk>', views.update_doctor_view,name='update-doctor'),
    path('admin-add-doctor', views.admin_add_doctor_view,name='admin-add-doctor'),
    path('admin-approve-doctor', views.admin_approve_doctor_view,name='admin-approve-doctor'),
    path('approve-doctor/<int:pk>', views.approve_doctor_view,name='approve-doctor'),
    path('reject-doctor/<int:pk>', views.reject_doctor_view,name='reject-doctor'),
    path('admin-view-doctor-specialisation',views.admin_view_doctor_specialisation_view,name='admin-view-doctor-specialisation'),


    path('admin-shopkeeper', views.admin_shopkeeper_view,name='admin-shopkeeper'),
    path('admin-view-shopkeeper', views.admin_view_shopkeeper_view,name='admin-view-shopkeeper'),
    path('delete-shopkeeper-from-hospital/<int:pk>', views.delete_shopkeeper_from_hospital_view,name='delete-shopkeeper-from-hospital'),
    path('update-shopkeeper/<int:pk>', views.update_shopkeeper_view,name='update-shopkeeper'),
    path('admin-add-shopkeeper', views.admin_add_shopkeeper_view,name='admin-add-shopkeeper'),
    path('admin-approve-shopkeeper', views.admin_approve_shopkeeper_view,name='admin-approve-shopkeeper'),
    path('approve-shopkeeper/<int:pk>', views.approve_shopkeeper_view,name='approve-shopkeeper'),
    path('reject-shopkeeper/<int:pk>', views.reject_shopkeeper_view,name='reject-shopkeeper'),
    path('admin-view-shopkeeper-type',views.admin_view_shopkeeper_type_view,name='admin-view-shopkeeper-type'),

    path('admin-patient', views.admin_patient_view,name='admin-patient'),
    path('admin-view-patient', views.admin_view_patient_view,name='admin-view-patient'),
    path('delete-patient-from-hospital/<int:pk>', views.delete_patient_from_hospital_view,name='delete-patient-from-hospital'),
    path('update-patient/<int:pk>', views.update_patient_view,name='update-patient'),
    path('admin-add-patient', views.admin_add_patient_view,name='admin-add-patient'),
    path('admin-approve-patient', views.admin_approve_patient_view,name='admin-approve-patient'),
    path('approve-patient/<int:pk>', views.approve_patient_view,name='approve-patient'),
    path('reject-patient/<int:pk>', views.reject_patient_view,name='reject-patient'),
    path('admin-discharge-patient', views.admin_discharge_patient_view,name='admin-discharge-patient'),
    path('discharge-patient/<int:pk>', views.discharge_patient_view,name='discharge-patient'),
    path('download-pdf/<int:pk>', views.download_pdf_view,name='download-pdf'),


    path('admin-appointment', views.admin_appointment_view,name='admin-appointment'),
    path('admin-view-appointment', views.admin_view_appointment_view,name='admin-view-appointment'),
    path('admin-add-appointment', views.admin_add_appointment_view,name='admin-add-appointment'),
    path('admin-approve-appointment', views.admin_approve_appointment_view,name='admin-approve-appointment'),
    path('approve-appointment/<int:pk>', views.approve_appointment_view,name='approve-appointment'),
    path('reject-appointment/<int:pk>', views.reject_appointment_view,name='reject-appointment'),
]


#---------FOR DOCTOR RELATED URLS-------------------------------------
urlpatterns +=[
    path('doctor-dashboard', views.doctor_dashboard_view,name='doctor-dashboard'),
    path('search', views.search_view,name='search'),

    path('doctor-patient', views.doctor_patient_view,name='doctor-patient'),
    path('doctor-view-patient', views.doctor_view_patient_view,name='doctor-view-patient'),
    path('doctor-view-discharge-patient',views.doctor_view_discharge_patient_view,name='doctor-view-discharge-patient'),

    path('doctor-appointment', views.doctor_appointment_view,name='doctor-appointment'),
    path('doctor-view-appointment', views.doctor_view_appointment_view,name='doctor-view-appointment'),
    path('doctor-delete-appointment',views.doctor_delete_appointment_view,name='doctor-delete-appointment'),
    path('delete-appointment/<int:pk>', views.delete_appointment_view,name='delete-appointment'),
]


# TODO:Add patient-order interactions; fix the Group issue which happens 'afterlogin'; improve UI


#---------FOR PATIENT RELATED URLS-------------------------------------
urlpatterns +=[

    path('patient-dashboard', views.patient_dashboard_view,name='patient-dashboard'),
    path('patient-appointment', views.patient_appointment_view,name='patient-appointment'),
    path('patient-order', views.patient_order_view,name='patient-order'),
    path('patient-book-appointment', views.patient_book_appointment_view,name='patient-book-appointment'),
    path('patient-view-appointment', views.patient_view_appointment_view,name='patient-view-appointment'),
    path('patient-book-order', views.patient_book_order_view,name='patient-book-order'),
    path('patient-view-order', views.patient_view_order_view,name='patient-view-order'),
    path('patient-view-doctor', views.patient_view_doctor_view,name='patient-view-doctor'),
    path('patient-view-shopkeeper', views.patient_view_shopkeeper_view,name='patient-view-shopkeeper'),
    path('searchdoctor', views.search_doctor_view,name='searchdoctor'),
    path('searchshopkeeper', views.search_shopkeeper_view,name='searchshopkeeper'),
    path('patient-discharge', views.patient_discharge_view,name='patient-discharge'),

]

#---------FOR SHOPKEEPER RELATED URLS-------------------------------------
urlpatterns +=[
    path('shopkeeper-dashboard', views.shopkeeper_dashboard_view,name='shopkeeper-dashboard'),
    path('search', views.search_view,name='search'),

    path('shopkeeper-patient', views.shopkeeper_patient_view,name='shopkeeper-patient'),
    path('shopkeeper-view-patient', views.shopkeeper_view_patient_view,name='shopkeeper-view-patient'),
    #path('shopkeeper-view-discharge-patient',views.shopkeeper_view_discharge_order_view,name='shopkeeper-view-discharge-order'),

    path('shopkeeper-order', views.shopkeeper_order_view,name='shopkeeper-appointment'),
    path('shopkeeper-view-order', views.shopkeeper_view_order_view,name='shopkeeper-view-order'),
    path('shopkeeper-delete-order',views.shopkeeper_delete_order_view,name='shopkeeper-delete-order'),
    path('delete-order/<int:pk>', views.delete_order_view,name='delete-order'),
]
