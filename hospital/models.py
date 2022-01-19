from django.db import models
from django.contrib.auth.models import User
import django_tables2 as tables


departments = [
    ("Cardiologist", "Cardiologist"),
    ("Dermatologists", "Dermatologists"),
    ("Emergency Medicine Specialists", "Emergency Medicine Specialists"),
    ("Allergists/Immunologists", "Allergists/Immunologists"),
    ("Anesthesiologists", "Anesthesiologists"),
    ("Colon and Rectal Surgeons", "Colon and Rectal Surgeons"),
    ("General Physician", "General Physician"),
    ("Other", "Other"),
]

type = [
    ("Food", "Food"),
    ("General", "General"),
    ("Medicine", "Medicine"),
    ("Other", "Other"),
]

covidStatusTypes = [
    ("Fully-Vaccinated", "Fully-Vaccinated"),
    ("Requested Testing", "Requested Testing"),
    ("Covid Positive", "Covid Positive"),
    ("Quarantined", "Quarantined"),
    ("Unvaccinated", "Unvaccinated")
]


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        upload_to="profile_pic/DoctorProfilePic/", default='default.png'
    )
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=True)
    department = models.CharField(
        max_length=50, choices=departments, default="Cardiologist"
    )
    status = models.BooleanField(default=False)

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return "{} {} ({})".format(
            self.user.first_name, self.user.last_name, self.department
        )


class Shopkeeper(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        upload_to="profile_pic/ShopkeeperProfilePic/", default='images/default.png'
    )
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=True)
    type = models.CharField(max_length=50, choices=type, default="Other")
    status = models.BooleanField(default=False)

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return "{} {} ({})".format(self.user.first_name, self.user.last_name, self.type)


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        upload_to="profile_pic/PatientProfilePic/", default='images/default.png'
    )
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=False)
    symptoms = models.CharField(max_length=100, blank=True)
    assignedDoctorId = models.PositiveIntegerField(null=True)
    admitDate = models.DateField(auto_now=True)
    status = models.BooleanField(default=True)
    covidStatus = models.CharField(
        max_length=50, choices=covidStatusTypes, default="Fully Vaccinated"
    )

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return self.user.first_name + " (" + self.covidStatus + ")"


class Appointment(models.Model):
    patientId = models.PositiveIntegerField(null=True)
    doctorId = models.PositiveIntegerField(null=True)
    patientName = models.CharField(max_length=40, null=True)
    doctorName = models.CharField(max_length=40, null=True)
    appointmentDate = models.DateField(auto_now=True)
    description = models.TextField(max_length=500)
    status = models.BooleanField(default=False)


class Order(models.Model):
    patientId = models.PositiveIntegerField(null=True)
    shopkeeperId = models.PositiveIntegerField(null=True)
    patientName = models.CharField(max_length=40, null=True)
    shopkeeperName = models.CharField(max_length=40, null=True)
    orderDate = models.DateField(auto_now=True)
    description = models.TextField(max_length=500)
    status = models.BooleanField(default=True)


class PatientDischargeDetails(models.Model):
    patientId = models.PositiveIntegerField(null=True)
    patientName = models.CharField(max_length=40)
    assignedDoctorName = models.CharField(max_length=40)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=True)
    symptoms = models.CharField(max_length=100, null=True)

    admitDate = models.DateField(null=False)
    releaseDate = models.DateField(null=False)
    daySpent = models.PositiveIntegerField(null=False)

    roomCharge = models.PositiveIntegerField(null=False)
    medicineCost = models.PositiveIntegerField(null=False)
    doctorFee = models.PositiveIntegerField(null=False)
    OtherCharge = models.PositiveIntegerField(null=False)
    total = models.PositiveIntegerField(null=False)

# class PatientTable(tables.Table):
#     class Meta:
#         model = Patient