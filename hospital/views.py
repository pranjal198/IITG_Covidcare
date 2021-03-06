from re import template
from django.shortcuts import render, redirect, reverse
from . import (forms, models)
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect, JsonResponse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime, timedelta, date
from django.conf import settings
from django.db.models import Q
from django.core import serializers
from django.template import RequestContext
import django_tables2 as tables
from django.contrib import messages

# Create your views here.
def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("afterlogin")
    return render(request, "hospital/index.html")


# for showing signup/login button for admin
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("afterlogin")
    return render(request, "hospital/adminclick.html")


# for showing signup/login button for doctor
def doctorclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("afterlogin")
    return render(request, "hospital/doctorclick.html")


def shopkeeperclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("afterlogin")
    return render(request, "hospital/shopkeeperclick.html")


# for showing signup/login button for patient
def patientclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("afterlogin")
    return render(request, "hospital/patientclick.html")


def admin_signup_view(request):
    form = forms.AdminSigupForm()
    if request.method == "POST":
        form = forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group, created = Group.objects.get_or_create(name="ADMIN")
            my_admin_group.user_set.add(user)
            messages.success(request, "Your account has been created! You are now able to login.")
            return HttpResponseRedirect("adminlogin")
    return render(request, "hospital/adminsignup.html", {"form": form})


def doctor_signup_view(request):
    userForm = forms.DoctorUserForm()
    doctorForm = forms.DoctorForm()
    mydict = {"userForm": userForm, "doctorForm": doctorForm}
    if request.method == "POST":
        userForm = forms.DoctorUserForm(request.POST)
        doctorForm = forms.DoctorForm(request.POST, request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            doctor = doctorForm.save(commit=False)
            doctor.user = user
            doctor = doctor.save()
            my_doctor_group, created = Group.objects.get_or_create(name="DOCTOR")
            my_doctor_group.user_set.add(user)
            messages.success(request, "Your account has been created! You are now able to login.")
            return HttpResponseRedirect("doctorlogin")
    return render(request, "hospital/doctorsignup.html", context=mydict)


def shopkeeper_signup_view(request):
    userForm = forms.ShopkeeperUserForm()
    shopkeeperForm = forms.ShopkeeperForm()
    mydict = {"userForm": userForm, "shopkeeperForm": shopkeeperForm}
    if request.method == "POST":
        userForm = forms.ShopkeeperUserForm(request.POST)
        shopkeeperForm = forms.ShopkeeperForm(request.POST, request.FILES)
        if userForm.is_valid() and shopkeeperForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            shopkeeper = shopkeeperForm.save(commit=False)
            shopkeeper.user = user
            shopkeeper = shopkeeper.save()
            print("form saved")
            my_shopkeeper_group, created = Group.objects.get_or_create(
                name="SHOPKEEPER"
            )
            my_shopkeeper_group.user_set.add(user)
            # print("added to group SHOPKEEPER")
            messages.success(request, "Your account has been created! You are now able to login.")
            return HttpResponseRedirect("shopkeeperlogin")
        else:
            print("some error")
    return render(request, "hospital/shopkeepersignup.html", context=mydict)


def patient_signup_view(request):
    userForm = forms.PatientUserForm()
    patientForm = forms.PatientForm()
    mydict = {"userForm": userForm, "patientForm": patientForm}
    if request.method == "POST":
        userForm = forms.PatientUserForm(request.POST)
        patientForm = forms.PatientForm(request.POST, request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            patient = patientForm.save(commit=False)
            patient.user = user
            patient.status = True
            patient.assignedDoctorId = request.POST.get("assignedDoctorId")
            patient.save()
            my_patient_group, created = Group.objects.get_or_create(name="PATIENT")
            my_patient_group.user_set.add(user)
            messages.success(request, "Your account has been created! You are now able to login.")
            return HttpResponseRedirect("patientlogin")
    return render(request, "hospital/patientsignup.html", context=mydict)


# -----------for checking user is doctor , patient or admin
def is_admin(user):
    return user.groups.filter(name="ADMIN").exists()


def is_doctor(user):
    return user.groups.filter(name="DOCTOR").exists()


def is_shopkeeper(user):
    return user.groups.filter(name="SHOPKEEPER").exists()


def is_patient(user):
    return user.groups.filter(name="PATIENT").exists()

def is_admin_or_patient(user):
    return is_admin(user) or is_patient(user)

def is_admin_or_shopkeeper(user):
    return is_admin(user) or is_shopkeeper(user)


# ---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,DOCTOR OR PATIENT
def afterlogin_view(request):
    print("inside afterlogin")
    if is_admin(request.user):
        return redirect("admin-dashboard")
    elif is_doctor(request.user):
        accountapproval = models.Doctor.objects.all().filter(
            user_id=request.user.id, status=True
        )
        if accountapproval:
            return redirect("doctor-dashboard")
        else:
            return render(request, "hospital/doctor_wait_for_approval.html")
    elif is_shopkeeper(request.user):
        accountapproval = models.Shopkeeper.objects.all().filter(
            user_id=request.user.id, status=True
        )
        if accountapproval:
            return redirect("shopkeeper-dashboard")
        else:
            return render(request, "hospital/shopkeeper_wait_for_approval.html")
    elif is_patient(request.user):
        accountapproval = models.Patient.objects.all().filter(
            user_id=request.user.id, status=True
        )
        if accountapproval:
            return redirect("patient-dashboard")
        else:
            return render(request, "hospital/patient_wait_for_approval.html")
    else:
        print("Error in sign in")
        return redirect("logout")

# ---------------------------------------------------------------------------------
# ------------------------ ADMIN RELATED VIEWS START ------------------------------
# ---------------------------------------------------------------------------------
@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    # for both table in admin dashboard
    doctors = models.Doctor.objects.all().order_by("-id")
    patients = models.Patient.objects.all().order_by("-id")
    shopkeepers = models.Shopkeeper.objects.all().order_by("-id")
    # for three cards
    doctorcount = models.Doctor.objects.all().filter(status=True).count()
    pendingdoctorcount = models.Doctor.objects.all().filter(status=False).count()

    patientcount = models.Patient.objects.all().filter(status=True).count()
    pendingpatientcount = models.Patient.objects.all().filter(status=False).count()

    appointmentcount = models.Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount = (
        models.Appointment.objects.all().filter(status=False).count()
    )

    shopkeepercount = models.Shopkeeper.objects.all().filter(status=True).count()
    pendingshopkeepercount = (
        models.Shopkeeper.objects.all().filter(status=False).count()
    )

    ordercount = models.Order.objects.all().filter(status=True).count()
    pendingordercount = models.Order.objects.all().filter(status=False).count()

    mydict = {
        "doctors": doctors,
        "patients": patients,
        "doctorcount": doctorcount,
        "pendingdoctorcount": pendingdoctorcount,
        "patientcount": patientcount,
        "pendingpatientcount": pendingpatientcount,
        "appointmentcount": appointmentcount,
        "pendingappointmentcount": pendingappointmentcount,
        "shopkeepercount": shopkeepercount,
        "pendingshopkeepercount": pendingshopkeepercount,
        "ordercount": ordercount,
        "pendingordercount": pendingordercount,
    }
    return render(request, "hospital/admin_dashboard.html", context=mydict)


# this view for sidebar click on admin page
@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_doctor_view(request):
    return render(request, "hospital/admin_doctor.html")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_shopkeeper_view(request):
    return render(request, "hospital/admin_shopkeeper.html")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_view_doctor_view(request):
    doctors = models.Doctor.objects.all().filter(status=True)
    return render(request, "hospital/admin_view_doctor.html", {"doctors": doctors})


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_view_shopkeeper_view(request):
    shopkeepers = models.Shopkeeper.objects.all().filter(status=True)
    return render(
        request, "hospital/admin_view_shopkeeper.html", {"shopkeepers": shopkeepers}
    )


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def delete_doctor_from_hospital_view(request, pk):
    doctor = models.Doctor.objects.get(id=pk)
    user = models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    messages.success(request, "Doctor has now been deleted")
    return redirect("admin-view-doctor")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def delete_shopkeeper_from_hospital_view(request, pk):
    shopkeeper = models.Shopkeeper.objects.get(id=pk)
    user = models.User.objects.get(id=shopkeeper.user_id)
    user.delete()
    shopkeeper.delete()
    messages.success(request, "Shopkeeper has now been deleted")
    return redirect("admin-view-shopkeeper")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def update_doctor_view(request, pk):
    doctor = models.Doctor.objects.get(id=pk)
    user = models.User.objects.get(id=doctor.user_id)

    userForm = forms.DoctorUserForm(instance=user)
    doctorForm = forms.DoctorForm(request.FILES, instance=doctor)
    mydict = {"userForm": userForm, "doctorForm": doctorForm}
    if request.method == "POST":
        userForm = forms.DoctorUserForm(request.POST, instance=user)
        doctorForm = forms.DoctorForm(request.POST, request.FILES, instance=doctor)
        if userForm.is_valid() and doctorForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            doctor = doctorForm.save(commit=False)
            doctor.status = True
            doctor.save()
            messages.success(request, "Doctor detail has now been updated")
            return redirect("admin-view-doctor")
    return render(request, "hospital/admin_update_doctor.html", context=mydict)


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def update_shopkeeper_view(request, pk):
    shopkeeper = models.Shopkeeper.objects.get(id=pk)
    user = models.User.objects.get(id=shopkeeper.user_id)

    userForm = forms.ShopkeeperUserForm(instance=user)
    shopkeeperForm = forms.ShopkeeperForm(request.FILES, instance=shopkeeper)
    mydict = {"userForm": userForm, "shopkeeperForm": shopkeeperForm}
    if request.method == "POST":
        userForm = forms.ShopkeeperUserForm(request.POST, instance=user)
        shopkeeperForm = forms.ShopkeeperForm(
            request.POST, request.FILES, instance=shopkeeper
        )
        if userForm.is_valid() and shopkeeperForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            shopkeeper = shopkeeperForm.save(commit=False)
            shopkeeper.status = True
            shopkeeper.save()
            messages.success(request, "Shopkeeper details have now been updated.")
            return redirect("admin-view-shopkeeper")
    return render(request, "hospital/admin_update_shopkeeper.html", context=mydict)


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_add_doctor_view(request):
    userForm = forms.DoctorUserForm()
    doctorForm = forms.DoctorForm()
    mydict = {"userForm": userForm, "doctorForm": doctorForm}
    if request.method == "POST":
        userForm = forms.DoctorUserForm(request.POST)
        doctorForm = forms.DoctorForm(request.POST, request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()

            doctor = doctorForm.save(commit=False)
            doctor.user = user
            doctor.status = True
            doctor.save()

            my_doctor_group = Group.objects.get_or_create(name="DOCTOR")
            my_doctor_group[0].user_set.add(user)
            messages.success(request, "Doctor has been successfully added!")
        return HttpResponseRedirect("admin-view-doctor")
    return render(request, "hospital/admin_add_doctor.html", context=mydict)


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_add_shopkeeper_view(request):
    userForm = forms.ShopkeeperUserForm()
    shopkeeperForm = forms.ShopkeeperForm()
    mydict = {"userForm": userForm, "shopkeeperForm": shopkeeperForm}
    if request.method == "POST":
        userForm = forms.ShopkeeperUserForm(request.POST)
        shopkeeperForm = forms.ShopkeeperForm(request.POST, request.FILES)
        if userForm.is_valid() and shopkeeperForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()

            shopkeeper = shopkeeperForm.save(commit=False)
            shopkeeper.user = user
            shopkeeper.status = True
            shopkeeper.save()

            my_shopkeeper_group = Group.objects.get_or_create(name="SHOPKEEPER")
            my_shopkeeper_group[0].user_set.add(user)
            messages.success(request, "Shopkeeper has been successfully added.")
        return HttpResponseRedirect("admin-view-shopkeeper")
    return render(request, "hospital/admin_add_shopkeeper.html", context=mydict)


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_approve_doctor_view(request):
    # those whose approval are needed
    doctors = models.Doctor.objects.all().filter(status=False)
    return render(request, "hospital/admin_approve_doctor.html", {"doctors": doctors})


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_approve_shopkeeper_view(request):
    # those whose approval are needed
    shopkeepers = models.Shopkeeper.objects.all().filter(status=False)
    return render(
        request, "hospital/admin_approve_shopkeeper.html", {"shopkeepers": shopkeepers}
    )


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def approve_doctor_view(request, pk):
    doctor = models.Doctor.objects.get(id=pk)
    doctor.status = True
    doctor.save()
    messages.success(request, "Doctor has now been approved.")
    return redirect(reverse("admin-approve-doctor"))


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def approve_shopkeeper_view(request, pk):
    shopkeeper = models.Shopkeeper.objects.get(id=pk)
    shopkeeper.status = True
    shopkeeper.save()
    messages.success(request, "Shopkeeper has now been deleted")
    return redirect(reverse("admin-approve-shopkeeper"))


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def reject_doctor_view(request, pk):
    doctor = models.Doctor.objects.get(id=pk)
    user = models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    messages.warning(request, "Doctor has now been rejected")
    return redirect("admin-approve-doctor")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def reject_shopkeeper_view(request, pk):
    shopkeeper = models.Shopkeeper.objects.get(id=pk)
    user = models.User.objects.get(id=shopkeeper.user_id)
    user.delete()
    shopkeeper.delete()
    messages.warning(request, "Shopkeeper has now been rejected.")
    return redirect("admin-approve-shopkeeper")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_view_doctor_specialisation_view(request):
    doctors = models.Doctor.objects.all().filter(status=True)
    return render(
        request, "hospital/admin_view_doctor_specialisation.html", {"doctors": doctors}
    )


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_view_shopkeeper_type_view(request):
    shopkeepers = models.Shopkeeper.objects.all().filter(status=True)
    return render(
        request,
        "hospital/admin_view_shopkeeper_type.html",
        {"shopkeepers": shopkeepers},
    )


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_patient_view(request):
    return render(request, "hospital/admin_patient.html")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_view_patient_view(request):
    patients = models.Patient.objects.all().filter(status=True)
    return render(request, "hospital/admin_view_patient.html", {"patients": patients})


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def delete_patient_from_hospital_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    user = models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect("admin-view-patient")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def update_patient_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    user = models.User.objects.get(id=patient.user_id)

    userForm = forms.PatientUserForm(instance=user)
    patientForm = forms.PatientForm(request.FILES, instance=patient)
    mydict = {"userForm": userForm, "patientForm": patientForm}
    if request.method == "POST":
        userForm = forms.PatientUserForm(request.POST, instance=user)
        patientForm = forms.PatientForm(request.POST, request.FILES, instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            patient = patientForm.save(commit=False)
            patient.status = True
            patient.assignedDoctorId = request.POST.get("assignedDoctorId")
            patient.save()
            messages.success(request, "Patient details successfully updated!")
            return redirect("admin-view-patient")
    return render(request, "hospital/admin_update_patient.html", context=mydict)

@login_required(login_url="patientlogin")
@user_passes_test(is_patient)
def patient_update_patient_view(request):
    patient = models.Patient.objects.get(user_id=request.user.id)
    user = models.User.objects.get(id=patient.user_id)
    if request.method == "POST":
        userForm = forms.PatientUserForm(request.POST, instance=request.user)
        #patientForm = forms.PatientForm(request.FILES, instance=patient)
        #userForm = forms.PatientUserForm(request.POST, instance=user)
        patientForm = forms.PatientUpdateForm(request.POST, request.FILES, instance=patient)
        if patientForm.is_valid():
            patient.save()
            messages.success(request, "Successfully updated your details.")
            return redirect("patient-dashboard")
    else:
        userForm = forms.PatientUserForm(instance=user)
        patientForm = forms.PatientUpdateForm(instance=patient)
    mydict = {
        'userForm': userForm,
        'patientForm': patientForm
    }
    return render(request, "hospital/patient_update_patient.html", context=mydict)


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_add_patient_view(request):
    userForm = forms.PatientUserForm()
    patientForm = forms.PatientForm()
    mydict = {"userForm": userForm, "patientForm": patientForm}
    if request.method == "POST":
        userForm = forms.PatientUserForm(request.POST)
        patientForm = forms.PatientForm(request.POST, request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()

            patient = patientForm.save(commit=False)
            patient.user = user
            patient.status = True
            patient.assignedDoctorId = request.POST.get("assignedDoctorId")
            patient.save()

            my_patient_group = Group.objects.get_or_create(name="PATIENT")
            my_patient_group[0].user_set.add(user)
            messages.success(request, "Patient has been successfully added")
        return HttpResponseRedirect("admin-view-patient")
    return render(request, "hospital/admin_add_patient.html", context=mydict)


# ------------------FOR APPROVING PATIENT BY ADMIN----------------------
@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_approve_patient_view(request):
    # those whose approval are needed
    patients = models.Patient.objects.all().filter(status=False)
    return render(
        request, "hospital/admin_approve_patient.html", {"patients": patients}
    )


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def approve_patient_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    patient.status = True
    patient.save()
    return redirect(reverse("admin-approve-patient"))


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def reject_patient_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    user = models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect("admin-approve-patient")


# --------------------- FOR DISCHARGING PATIENT BY ADMIN START-------------------------
@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_discharge_patient_view(request):
    patients = models.Patient.objects.all().filter(status=True)
    return render(
        request, "hospital/admin_discharge_patient.html", {"patients": patients}
    )


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def discharge_patient_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    days = date.today() - patient.admitDate  # 2 days, 0:00:00
    assignedDoctor = models.User.objects.all().filter(id=patient.assignedDoctorId)
    d = days.days  # only how many day that is 2
    patientDict = {
        "patientId": pk,
        "name": patient.get_name,
        "mobile": patient.mobile,
        "address": patient.address,
        "symptoms": patient.symptoms,
        "admitDate": patient.admitDate,
        "todayDate": date.today(),
        "day": d,
        "assignedDoctorName": assignedDoctor[0].first_name,
    }
    if request.method == "POST":
        feeDict = {
            "roomCharge": int(request.POST["roomCharge"]) * int(d),
            "doctorFee": request.POST["doctorFee"],
            "medicineCost": request.POST["medicineCost"],
            "OtherCharge": request.POST["OtherCharge"],
            "total": (int(request.POST["roomCharge"]) * int(d))
            + int(request.POST["doctorFee"])
            + int(request.POST["medicineCost"])
            + int(request.POST["OtherCharge"]),
        }
        patientDict.update(feeDict)
        # for updating to database patientDischargeDetails (pDD)
        pDD = models.PatientDischargeDetails()
        pDD.patientId = pk
        pDD.patientName = patient.get_name
        pDD.assignedDoctorName = assignedDoctor[0].first_name
        pDD.address = patient.address
        pDD.mobile = patient.mobile
        pDD.symptoms = patient.symptoms
        pDD.admitDate = patient.admitDate
        pDD.releaseDate = date.today()
        pDD.daySpent = int(d)
        pDD.medicineCost = int(request.POST["medicineCost"])
        pDD.roomCharge = int(request.POST["roomCharge"]) * int(d)
        pDD.doctorFee = int(request.POST["doctorFee"])
        pDD.OtherCharge = int(request.POST["OtherCharge"])
        pDD.total = (
            (int(request.POST["roomCharge"]) * int(d))
            + int(request.POST["doctorFee"])
            + int(request.POST["medicineCost"])
            + int(request.POST["OtherCharge"])
        )
        pDD.save()
        return render(request, "hospital/patient_final_bill.html", context=patientDict)
    return render(request, "hospital/patient_generate_bill.html", context=patientDict)


# --------------for discharge patient bill (pdf) download and printing
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    return


def download_pdf_view(request, pk):
    dischargeDetails = (
        models.PatientDischargeDetails.objects.all()
        .filter(patientId=pk)
        .order_by("-id")[:1]
    )
    dict = {
        "patientName": dischargeDetails[0].patientName,
        "assignedDoctorName": dischargeDetails[0].assignedDoctorName,
        "address": dischargeDetails[0].address,
        "mobile": dischargeDetails[0].mobile,
        "symptoms": dischargeDetails[0].symptoms,
        "admitDate": dischargeDetails[0].admitDate,
        "releaseDate": dischargeDetails[0].releaseDate,
        "daySpent": dischargeDetails[0].daySpent,
        "medicineCost": dischargeDetails[0].medicineCost,
        "roomCharge": dischargeDetails[0].roomCharge,
        "doctorFee": dischargeDetails[0].doctorFee,
        "OtherCharge": dischargeDetails[0].OtherCharge,
        "total": dischargeDetails[0].total,
    }
    return render_to_pdf("hospital/download_bill.html", dict)


# -----------------APPOINTMENT START--------------------------------------------------------------------
@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_appointment_view(request):
    return render(request, "hospital/admin_appointment.html")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_view_appointment_view(request):
    appointments = models.Appointment.objects.all().filter(status=True)
    return render(
        request, "hospital/admin_view_appointment.html", {"appointments": appointments}
    )


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_add_appointment_view(request):
    appointmentForm = forms.AppointmentForm()
    mydict = {
        "appointmentForm": appointmentForm,
    }
    if request.method == "POST":
        appointmentForm = forms.AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment = appointmentForm.save(commit=False)
            appointment.doctorId = request.POST.get("doctorId")
            appointment.patientId = request.POST.get("patientId")
            appointment.doctorName = models.User.objects.get(
                id=request.POST.get("doctorId")
            ).first_name
            appointment.patientName = models.User.objects.get(
                id=request.POST.get("patientId")
            ).first_name
            appointment.status = True
            appointment.save()
            messages.success(request, "Appointment has been successfully created")
        return HttpResponseRedirect("admin-view-appointment")
    return render(request, "hospital/admin_add_appointment.html", context=mydict)


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_approve_appointment_view(request):
    # those whose approval are needed
    appointments = models.Appointment.objects.all().filter(status=False)
    return render(
        request,
        "hospital/admin_approve_appointment.html",
        {"appointments": appointments},
    )


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def approve_appointment_view(request, pk):
    appointment = models.Appointment.objects.get(id=pk)
    appointment.status = True
    appointment.save()
    messages.success(request, "Appointment has been successfully approved")
    return redirect(reverse("admin-approve-appointment"))


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def reject_appointment_view(request, pk):
    appointment = models.Appointment.objects.get(id=pk)
    appointment.delete()
    messages.success(request, "Appointment has been rejected")
    return redirect("admin-approve-appointment")


# ---------------------------------------------------------------------------------
# ------------------------ ADMIN RELATED VIEWS END ------------------------------
# ---------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------
# ------------------------ DOCTOR and SHOPKEEPER RELATED VIEWS START ------------------------------
# ---------------------------------------------------------------------------------
@login_required(login_url="doctorlogin")
@user_passes_test(is_doctor)
def doctor_dashboard_view(request):
    # for three cards
    patientcount = (
        models.Patient.objects.all()
        .filter(status=True, assignedDoctorId=request.user.id)
        .count()
    )
    appointmentcount = (
        models.Appointment.objects.all()
        .filter(status=True, doctorId=request.user.id)
        .count()
    )
    patientdischarged = (
        models.PatientDischargeDetails.objects.all()
        .distinct()
        .filter(assignedDoctorName=request.user.first_name)
        .count()
    )

    # for  table in doctor dashboard
    appointments = (
        models.Appointment.objects.all()
        .filter(status=True, doctorId=request.user.id)
        .order_by("-id")
    )
    patientid = []
    for a in appointments:
        patientid.append(a.patientId)
    patients = (
        models.Patient.objects.all()
        .filter(status=True, user_id__in=patientid)
        .order_by("-id")
    )
    appointments = zip(appointments, patients)
    mydict = {
        "patientcount": patientcount,
        "appointmentcount": appointmentcount,
        "patientdischarged": patientdischarged,
        "appointments": appointments,
        "doctor": models.Doctor.objects.get(
            user_id=request.user.id
        ),  # for profile picture of doctor in sidebar
    }
    return render(request, "hospital/doctor_dashboard.html", context=mydict)


@login_required(login_url="shopkeeperlogin")
@user_passes_test(is_shopkeeper)
def shopkeeper_dashboard_view(request):
    # for three cards
    # patientcount=models.Patient.objects.all().filter(status=True,assignedShopkeeperId=request.user.id).count()
    ordercount = (
        models.Order.objects.all()
        .filter(status=True, shopkeeperId=request.user.id)
        .count()
    )
    print(f"SHOPKEEEPER REQUEST ID: {request.user.id}")
    # ordersdischarged=models.OrderDischargeDetails.objects.all().distinct().filter(assignedShopkeeperName=request.user.first_name).count()

    # for  table in Shopkeeper dashboard
    orders = (
        models.Order.objects.all()
        .filter(status=True, shopkeeperId=request.user.id)
        .order_by("-id")
    )
    patientid = []
    for a in orders:
        patientid.append(a.patientId)
    patients = []
    for p in patientid:
        patients.append(models.Patient.objects.filter(user=p))
    # patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    orders = zip(orders, patients)
    # patients = (
    #     models.Patient.objects.all()
    #     .filter(status=True, user_id__in=patientid)
    #     .order_by("-id")
    # )
    # orders = zip(orders, patients)
    mydict = {
        #'patientcount':patientcount,
        "ordercount": ordercount,
        #'ordersdischarged':ordersdischarged,
        "orders": orders,
        "shopkeeper": models.Shopkeeper.objects.get(
            user_id=request.user.id
        ),  # for profile picture of Shopkeeper in sidebar
    }
    return render(request, "hospital/shopkeeper_dashboard.html", context=mydict)


@login_required(login_url="doctorlogin")
@user_passes_test(is_doctor)
def doctor_patient_view(request):
    mydict = {
        "doctor": models.Doctor.objects.get(
            user_id=request.user.id
        ),  # for profile picture of doctor in sidebar
    }
    return render(request, "hospital/doctor_patient.html", context=mydict)


@login_required(login_url="shopkeeperlogin")
@user_passes_test(is_shopkeeper)
def shopkeeper_patient_view(request):
    mydict = {
        "shopkeeper": models.Shopkeeper.objects.get(
            user_id=request.user.id
        ),  # for profile picture of Shopkeeper in sidebar
    }
    return render(request, "hospital/shopkeeper_patient.html", context=mydict)


@login_required(login_url="doctorlogin")
@user_passes_test(is_doctor)
def doctor_view_patient_view(request):
    patients = models.Patient.objects.all().filter(
        status=True, assignedDoctorId=request.user.id
    )
    doctor = models.Doctor.objects.get(
        user_id=request.user.id
    )  # for profile picture of doctor in sidebar
    return render(
        request,
        "hospital/doctor_view_patient.html",
        {"patients": patients, "doctor": doctor},
    )


@login_required(login_url="shopkeeperlogin")
@user_passes_test(is_shopkeeper)
def shopkeeper_view_patient_view(request):
    patients = models.Patient.objects.all().filter(
        status=True, assignedShopkeeperId=request.user.id
    )
    shopkeeper = models.Shopkeeper.objects.get(
        user_id=request.user.id
    )  # for profile picture of Shopkeeper in sidebar
    return render(
        request,
        "hospital/shopkeeper_view_patient.html",
        {"patients": patients, "shopkeeper": shopkeeper},
    )


@login_required(login_url="doctorlogin")
@user_passes_test(is_doctor)
def search_view(request):
    doctor = models.Doctor.objects.get(
        user_id=request.user.id
    )  # for profile picture of doctor in sidebar
    # whatever user write in search box we get in query
    query = request.GET["query"]
    patients = (
        models.Patient.objects.all()
        .filter(status=True, assignedDoctorId=request.user.id)
        .filter(Q(symptoms__icontains=query) | Q(user__first_name__icontains=query))
    )
    return render(
        request,
        "hospital/doctor_view_patient.html",
        {"patients": patients, "doctor": doctor},
    )


# @login_required(login_url='shopkeeperlogin')
# @user_passes_test(is_shopkeeper)
# def search_view(request):
#     Shopkeeper=models.Shopkeeper.objects.get(user_id=request.user.id) #for profile picture of Shopkeeper in sidebar
#     # whatever user write in search box we get in query
#     query = request.GET['query']
#     patients=models.Patient.objects.all().filter(status=True,assignedShopkeeperId=request.user.id).filter(Q(symptoms__icontains=query)|Q(user__first_name__icontains=query))
#     return render(request,'hospital/Shopkeeper_view_patient.html',{'patients':patients,'shopkeeper':Shopkeeper})


@login_required(login_url="doctorlogin")
@user_passes_test(is_doctor)
def doctor_view_discharge_patient_view(request):
    dischargedpatients = (
        models.PatientDischargeDetails.objects.all()
        .distinct()
        .filter(assignedDoctorName=request.user.first_name)
    )
    doctor = models.Doctor.objects.get(
        user_id=request.user.id
    )  # for profile picture of doctor in sidebar
    return render(
        request,
        "hospital/doctor_view_discharge_patient.html",
        {"dischargedpatients": dischargedpatients, "doctor": doctor},
    )


# @login_required(login_url='shopkeeperlogin')
# @user_passes_test(is_shopkeeper)
# def Shopkeeper_view_discharge_patient_view(request):
#     dischargedpatients=models.PatientDischargeDetails.objects.all().distinct().filter(assignedShopkeeperName=request.user.first_name)
#     Shopkeeper=models.Shopkeeper.objects.get(user_id=request.user.id) #for profile picture of Shopkeeper in sidebar
#     return render(request,'hospital/Shopkeeper_view_discharge_patient.html',{'dischargedpatients':dischargedpatients,'shopkeeper':Shopkeeper})


@login_required(login_url="doctorlogin")
@user_passes_test(is_doctor)
def doctor_appointment_view(request):
    doctor = models.Doctor.objects.get(
        user_id=request.user.id
    )  # for profile picture of doctor in sidebar
    return render(request, "hospital/doctor_appointment.html", {"doctor": doctor})


@login_required(login_url="shopkeeperlogin")
@user_passes_test(is_shopkeeper)
def shopkeeper_order_view(request):
    shopkeeper = models.Shopkeeper.objects.get(
        user_id=request.user.id
    )  # for profile picture of Shopkeeper in sidebar
    return render(request, "hospital/shopkeeper_order.html", {"shopkeeper": shopkeeper})


@login_required(login_url="doctorlogin")
@user_passes_test(is_doctor)
def doctor_view_appointment_view(request):
    doctor = models.Doctor.objects.get(
        user_id=request.user.id
    )  # for profile picture of doctor in sidebar
    appointments = models.Appointment.objects.all().filter(
        status=True, doctorId=request.user.id
    )
    patientid = []
    for a in appointments:
        patientid.append(a.patientId)
    patients = models.Patient.objects.all().filter(status=True, user_id__in=patientid)
    appointments = zip(appointments, patients)
    return render(
        request,
        "hospital/doctor_view_appointment.html",
        {"appointments": appointments, "doctor": doctor},
    )


# TODO: fix this to show multiple orders from one patient
@login_required(login_url="shopkeeperlogin")
@user_passes_test(is_shopkeeper)
def shopkeeper_view_order_view(request):
    shopkeeper = models.Shopkeeper.objects.get(
        user_id=request.user.id
    )  # for profile picture of Shopkeeper in sidebar
    orders = models.Order.objects.all().filter(
        status=True, shopkeeperId=request.user.id
    )
    patientid = []
    for o in orders:
        patientid.append(o.patientId)

    patients = []
    for p in patientid:
        patients.append(models.Patient.objects.filter(user=p))
    # patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    orders = zip(orders, patients)
    return render(
        request,
        "hospital/shopkeeper_view_order.html",
        {"orders": orders, "shopkeeper": shopkeeper},
    )


@login_required(login_url="doctorlogin")
@user_passes_test(is_doctor)
def doctor_delete_appointment_view(request):
    doctor = models.Doctor.objects.get(
        user_id=request.user.id
    )  # for profile picture of doctor in sidebar
    appointments = models.Appointment.objects.all().filter(
        status=True, doctorId=request.user.id
    )
    patientid = []
    for a in appointments:
        patientid.append(a.patientId)
    patients = models.Patient.objects.all().filter(status=True, user_id__in=patientid)
    appointments = zip(appointments, patients)
    return render(
        request,
        "hospital/doctor_delete_appointment.html",
        {"appointments": appointments, "doctor": doctor},
    )


@login_required(login_url="shopkeeperlogin")
@user_passes_test(is_shopkeeper)
def shopkeeper_delete_order_view(request):
    shopkeeper = models.Shopkeeper.objects.get(
        user_id=request.user.id
    )  # for profile picture of Shopkeeper in sidebar
    orders = models.Order.objects.all().filter(
        status=True, shopkeeperId=request.user.id
    )
    patientid = []
    for o in orders:
        patientid.append(o.patientId)

    patients = []
    for p in patientid:
        patients.append(models.Patient.objects.filter(user=p))
    # patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    orders = zip(orders, patients)
    return render(
        request,
        "hospital/shopkeeper_delete_order.html",
        {"orders": orders, "shopkeeper": shopkeeper},
    )


@login_required(login_url="doctorlogin")
@user_passes_test(is_doctor)
def delete_appointment_view(request, pk):
    appointment = models.Appointment.objects.get(id=pk)
    appointment.delete()
    doctor = models.Doctor.objects.get(
        user_id=request.user.id
    )  # for profile picture of doctor in sidebar
    appointments = models.Appointment.objects.all().filter(
        status=True, doctorId=request.user.id
    )
    patientid = []
    for a in appointments:
        patientid.append(a.patientId)
    patients = models.Patient.objects.all().filter(status=True, user_id__in=patientid)
    appointments = zip(appointments, patients)
    return render(
        request,
        "hospital/doctor_delete_appointment.html",
        {"appointments": appointments, "doctor": doctor},
    )


@login_required(login_url="shopkeeperlogin")
@user_passes_test(is_shopkeeper)
def delete_order_view(request, pk):
    order = models.Order.objects.get(id=pk)
    order.delete()
    shopkeeper = models.Shopkeeper.objects.get(
        user_id=request.user.id
    )  # for profile picture of Shopkeeper in sidebar
    orders = models.Order.objects.all().filter(
        status=True, shopkeeperId=request.user.id
    )
    
    patientid = []
    for o in orders:
        patientid.append(o.patientId)

    patients = []
    for p in patientid:
        patients.append(models.Patient.objects.filter(user=p))
    # patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    orders = zip(orders, patients)
    return render(
        request,
        "hospital/shopkeeper_delete_order.html",
        {"orders": orders, "shopkeeper": shopkeeper},
    )


# ---------------------------------------------------------------------------------
# ------------------------ DOCTOR and SHOPKEEPER RELATED VIEWS END ------------------------------
# ---------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------
# ------------------------ PATIENT RELATED VIEWS START ------------------------------
# ---------------------------------------------------------------------------------
@login_required(login_url="patientlogin")
@user_passes_test(is_patient)
def patient_dashboard_view(request):
    patient = models.Patient.objects.get(user_id=request.user.id)
    doctor = models.Doctor.objects.get(user_id=patient.assignedDoctorId)
    mydict = {
        "patient": patient,
        "doctorName": doctor.get_name,
        "doctorMobile": doctor.mobile,
        "doctorAddress": doctor.address,
        "symptoms": patient.symptoms,
        "doctorDepartment": doctor.department,
        "admitDate": patient.admitDate,
    }
    return render(request, "hospital/patient_dashboard.html", context=mydict)


@login_required(login_url="patientlogin")
@user_passes_test(is_patient)
def patient_appointment_view(request):
    patient = models.Patient.objects.get(
        user_id=request.user.id
    )  # for profile picture of patient in sidebar
    return render(request, "hospital/patient_appointment.html", {"patient": patient})


@login_required(login_url="patientlogin")
@user_passes_test(is_patient)
def patient_order_view(request):
    patient = models.Patient.objects.get(
        user_id=request.user.id
    )  # for profile picture of patient in sidebar
    return render(request, "hospital/patient_order.html", {"patient": patient})


@login_required(login_url="patientlogin")
@user_passes_test(is_patient)
def patient_book_appointment_view(request):
    appointmentForm = forms.PatientAppointmentForm()
    patient = models.Patient.objects.get(
        user_id=request.user.id
    )  # for profile picture of patient in sidebar
    message = None
    mydict = {
        "appointmentForm": appointmentForm,
        "patient": patient,
        "message": message,
    }
    if request.method == "POST":
        appointmentForm = forms.PatientAppointmentForm(request.POST)
        if appointmentForm.is_valid():
            print(request.POST.get("doctorId"))
            desc = request.POST.get("description")

            doctor = models.Doctor.objects.get(user_id=request.POST.get("doctorId"))

            appointment = appointmentForm.save(commit=False)
            appointment.doctorId = request.POST.get("doctorId")
            appointment.patientId = (
                request.user.id
            )  # ----user can choose any patient but only their info will be stored
            appointment.doctorName = models.User.objects.get(
                id=request.POST.get("doctorId")
            ).first_name
            appointment.patientName = (
                request.user.first_name
            )  # ----user can choose any patient but only their info will be stored
            appointment.status = False
            appointment.save()
            messages.success(request, "Appointment has been successfully created. Please wait for approval.")
        return HttpResponseRedirect("patient-view-appointment")
    return render(request, "hospital/patient_book_appointment.html", context=mydict)


@login_required(login_url="patientlogin")
@user_passes_test(is_patient)
def patient_book_order_view(request):
    orderForm = forms.PatientOrderForm()
    patient = models.Patient.objects.get(
        user_id=request.user.id
    )  # for profile picture of patient in sidebar
    message = None
    mydict = {"orderForm": orderForm, "patient": patient, "message": message}
    if request.method == "POST":
        print("POST REQUEST")
        orderForm = forms.PatientOrderForm(request.POST)
        if orderForm.is_valid():
            print(request.POST.get("shopkeeperId"))
            desc = request.POST.get("description")

            shopkeeper = models.Shopkeeper.objects.get(
                user_id=request.POST.get("shopkeeperId")
            )

            order = orderForm.save(commit=False)
            order.shopkeeperId = request.POST.get("shopkeeperId")
            order.patientId = (
                request.user.id
            )  # ----user can choose any patient but only their info will be stored
            order.shopkeeperName = models.User.objects.get(
                id=request.POST.get("shopkeeperId")
            ).first_name
            order.patientName = (
                request.user.first_name
            )  # ----user can choose any patient but only their info will be stored
            order.status = True
            order.save()
            print("ORDER SAVED")
            messages.success(request, f"Order has been successfully created. Please contact the shopkeeper at {shopkeeper.mobile}.")
        return HttpResponseRedirect("patient-view-order")
    print("SOME ISSUE")
    return render(request, "hospital/patient_book_order.html", context=mydict)


def patient_view_doctor_view(request):
    doctors = models.Doctor.objects.all().filter(status=True)
    patient = models.Patient.objects.get(
        user_id=request.user.id
    )  # for profile picture of patient in sidebar
    return render(
        request,
        "hospital/patient_view_doctor.html",
        {"patient": patient, "doctors": doctors},
    )


def patient_view_shopkeeper_view(request):
    shopkeepers = models.Shopkeeper.objects.all().filter(status=True)
    patient = models.Patient.objects.get(
        user_id=request.user.id
    )  # for profile picture of patient in sidebar
    return render(
        request,
        "hospital/patient_view_shopkeeper.html",
        {"patient": patient, "shopkeepers": shopkeepers},
    )


def search_doctor_view(request):
    patient = models.Patient.objects.get(
        user_id=request.user.id
    )  # for profile picture of patient in sidebar

    # whatever user write in search box we get in query
    query = request.GET["query"]
    doctors = (
        models.Doctor.objects.all()
        .filter(status=True)
        .filter(Q(department__icontains=query) | Q(user__first_name__icontains=query))
    )
    return render(
        request,
        "hospital/patient_view_doctor.html",
        {"patient": patient, "doctors": doctors},
    )


def search_shopkeeper_view(request):
    patient = models.Patient.objects.get(
        user_id=request.user.id
    )  # for profile picture of patient in sidebar

    # whatever user write in search box we get in query
    query = request.GET["query"]
    shopkeepers = (
        models.Shopkeeper.objects.all()
        .filter(status=True)
        .filter(Q(type__icontains=query) | Q(user__first_name__icontains=query))
    )
    return render(
        request,
        "hospital/patient_view_shopkeeper.html",
        {"patient": patient, "shopkeepers": shopkeepers},
    )


@login_required(login_url="patientlogin")
@user_passes_test(is_patient)
def patient_view_appointment_view(request):
    patient = models.Patient.objects.get(
        user_id=request.user.id
    )  # for profile picture of patient in sidebar
    appointments = models.Appointment.objects.all().filter(patientId=request.user.id)
    return render(
        request,
        "hospital/patient_view_appointment.html",
        {"appointments": appointments, "patient": patient},
    )


@login_required(login_url="patientlogin")
@user_passes_test(is_patient)
def patient_view_order_view(request):
    patient = models.Patient.objects.get(
        user_id=request.user.id
    )  # for profile picture of patient in sidebar
    orders = models.Order.objects.all().filter(patientId=request.user.id)
    return render(
        request,
        "hospital/patient_view_order.html",
        {"orders": orders, "patient": patient},
    )


@login_required(login_url="patientlogin")
@user_passes_test(is_patient)
def patient_discharge_view(request):
    patient = models.Patient.objects.get(
        user_id=request.user.id
    )  # for profile picture of patient in sidebar
    dischargeDetails = (
        models.PatientDischargeDetails.objects.all()
        .filter(patientId=patient.id)
        .order_by("-id")[:1]
    )
    patientDict = None
    if dischargeDetails:
        patientDict = {
            "is_discharged": True,
            "patient": patient,
            "patientId": patient.id,
            "patientName": patient.get_name,
            "assignedDoctorName": dischargeDetails[0].assignedDoctorName,
            "address": patient.address,
            "mobile": patient.mobile,
            "symptoms": patient.symptoms,
            "admitDate": patient.admitDate,
            "releaseDate": dischargeDetails[0].releaseDate,
            "daySpent": dischargeDetails[0].daySpent,
            "medicineCost": dischargeDetails[0].medicineCost,
            "roomCharge": dischargeDetails[0].roomCharge,
            "doctorFee": dischargeDetails[0].doctorFee,
            "OtherCharge": dischargeDetails[0].OtherCharge,
            "total": dischargeDetails[0].total,
        }
        print(patientDict)
    else:
        patientDict = {
            "is_discharged": False,
            "patient": patient,
            "patientId": request.user.id,
        }
    return render(request, "hospital/patient_discharge.html", context=patientDict)


# ------------------------ PATIENT RELATED VIEWS END ------------------------------
# ---------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------
# ------------------------ ABOUT US AND CONTACT US VIEWS START ------------------------------
# ---------------------------------------------------------------------------------
def aboutus_view(request):
    return render(request, "hospital/aboutus.html")


def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == "POST":
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data["Email"]
            name = sub.cleaned_data["Name"]
            message = sub.cleaned_data["Message"]
            send_mail(
                str(name) + " || " + str(email),
                message,
                settings.EMAIL_HOST_USER,
                settings.EMAIL_RECEIVING_USER,
                fail_silently=False,
            )
            return render(request, "hospital/contactussuccess.html")
    return render(request, "hospital/contactus.html", {"form": sub})


# ---------------------------------------------------------------------------------
# ------------------------ ADMIN RELATED VIEWS END ------------------------------
# ---------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------
# ------------------------ COVID DASHBOARD RELATED VIEWS ------------------------------
# ---------------------------------------------------------------------------------

def dashboard_with_pivot(request):
    return render(request, 'hospital/dashboard_with_pivot.html', {})

def pivot_data(request):
    labels = ["Fully-Vaccinated", "Requested Testing", "Quarantined", "Covid Positive", "Other"]
    data = [0, 0, 0, 0, 0]

    queryset = models.Patient.objects.all()

    for patient in queryset:
        covStatus = patient.covidStatus
        index = 4
        try:
            index = labels.index(str(covStatus))
        except ValueError:
            index = 4
        data[index] += 1

    return JsonResponse(
        data={
            'labels': labels,
            'data': data
        }
    )

def pivot_data_per_student(request):

    labels = []
    data = []
    queryset = models.Patient.objects.all()

    for patient in queryset:
        labels.append(patient.get_name())
        data.append(patient.covidStatus)

    return JsonResponse(
        data={
            'labels': labels,
            'data': data
        }
    )

# def table_view(request):
#     queryset = models.Patient.objects.all()
#     table = models.PatientTable(queryset)

#     return render_to_response("table_page.html", {"table": table}, context_instance=RequestContext(request))
# class TableView(tables.SingleTableView):
#     table_class = models.PatientTable
#     queryset = models.Patient.objects.all()
#     template_name = "table_page.html"

def table_view(request):
    patients = models.Patient.objects.filter(covidStatus="Covid Positive")
    return render(request, 'hospital/table_page.html', {"patients": patients})

