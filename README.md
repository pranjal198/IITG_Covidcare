
# IITG CovidCare 
### Developed for the Research & Industrial Conclave 2022 Hackathon
### Theme: To manage COVID-19 outbreak in an academic campus
### Created by [Gunjan Dhanuka](https://github.com/GunjanDhanuka) and [Pranjal Singh](https://github.com/pranjal198)
---


## Screenshots
### Homepage
![homepage snap](static/screenshots/home_page.png)
### Admin Dashboard
![dashboard snap](static/screenshots/admin_dashboard.png)
### Resident Dashboard
![dashboard snap](static/screenshots/resident_dashboard.png)

### Covid Statistic
![pie chart](static/screenshots/graph.png)
---
## Functions

### Overall Features
- An all-in-one solution for CRT admins, doctors and nurses, students and campus junta and the shopkeepers.
- Anyone can see the total number of positive cases on the campus and their names on the home page.
- The CRT Admin can add doctors, shopkeepers, patients or approve them if they register themselves.
- The Campus Junta can easily get essential delivered through them by the Order System. (Payment Portal is not present as of now)
- The Doctors can view all of their appointments and patient-data in one place.
- The Student can view his Appointments as well as his Orders. Also they can update their status if they get Covid Positive or Recover from it.
- The CRT Team can also find out who is unvaccinated and encourage them to get it at the earliest.
- Anyone on the campus can create a Resident/Student account.

  
### Admin
- Signup their account. Then Login (No approval Required).
- Can register/view/approve/reject/delete doctor who are available for the Campus Junta.
- Can admit/view/approve/reject/discharge resident/student (discharge patient when treatment is done).
- Can Generate/Download Invoice pdf (Generate Invoice according to medicine cost, room charge, doctor charge and other charge).
- Can view/book/approve Appointment (approve those appointments which is requested by patient).
- Can register/view/approve/reject Shopkeepers (but order amount is hidden from admin).

### Doctor
- Apply on the CovidCare portal. Then Login (Approval required by portal admin, Then only doctor can login).
- Can only view their patient details (symptoms, name, mobile ) assigned to that doctor by admin.
- Can view their discharged(by admin) patient list.
- Can view their Appointments, booked by admin.
- Can delete their Appointment, when doctor attended their appointment.

### Shopkeeper
- Apply on the CovidCare portal. Then Login (Approval required by portal admin, Then only shopkeeper can login).
- Can receive orders from different patients and view their contacts and address.
- Can view their orders and contact the customer incase of any ambiguity.
- Can delete the Order, after they have finished delivering the order.

### Student/ Resident
- Create account in the portal. Then Login. No approval from admin required.
- Can view assigned doctor's details like ( specialization, mobile, address).
- Can view their booked appointment status (pending/confirmed by admin).
- Can book appointments.(approval required by admin)
- Can set their Covid Status (Vaccinated, Quarantined, Requested Testing, etc.)
- Can update their Covid Status when infected or recovered.
- Can make orders to the Shopkeepers whose list they can view.
- Can contact shopkeeper using the phone number incase of any doubts.
---

## HOW TO RUN THIS PROJECT
- Install Python(3.7.6) (Dont Forget to Tick Add to Path while installing Python)

- Download This Project Zip Folder and Extract it
- Move to project folder in Terminal. Then run following Commands :
```
pip install -r requirements.txt
py manage.py makemigrations
py manage.py migrate
py manage.py runserver
```
- Now enter following URL in Your Browser Installed On Your Pc
```
http://127.0.0.1:8000/
```

## CHANGES REQUIRED FOR CONTACT US PAGE
- In settings.py file, You have to give your email and password
```
EMAIL_HOST_USER = 'youremail@gmail.com'
EMAIL_HOST_PASSWORD = 'your email password'
EMAIL_RECEIVING_USER = 'youremail@gmail.com'
```
- Login to Gmail through host email id in your browser and open following link and turn it ON:
```
https://myaccount.google.com/lesssecureapps
```

## Important
- Anyone can register as the Admin now, which is obviously not desired for real-life deployment. So make sure to block that route after adding all the CRT Admins.

Incase of any queries, feel free to reach out at d.gunjan@iitg.ac.in or pranjal.singh@iitg.ac.in

