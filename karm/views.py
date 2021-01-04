from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Patient, Contact, Doctor, Appointment
import datetime, pickle
from django.utils import timezone
# from django.core.mail import send_mail

# Create your views here.
def home(request):
    return render(request, 'home.html')

def handleSignup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        userType = request.POST['type']

        if len(username) > 20 or len(username) < 3:
            messages.error(request, "Username length must be in between 3 to 20 characters.")
            return render(request, 'error.html')

        if pass1 != pass2:
            messages.error(request, "Error!! Password and Confirmed Password didn't matched.")
            return render(request, 'error.html')  

        if not username.isalnum():
            messages.error(request, "Username should contain alphabates and numbers only")
            return render(request, 'error.html')     

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()

        if(userType=='doctor'):
            doctor = Doctor(username=username, first_name=fname, last_name=lname, email=email, user_type=userType)
            doctor.save()
        
        if(userType=='user'):
            patient = Patient(username=username, first_name=fname, last_name=lname, email=email, user_type=userType)
            patient.save()

        user = authenticate(username = username, password=pass1)
        if user is not None:
            login(request, user)

        messages.success(request, "Successfully Signed Up")
        return redirect('home')
    else:
        return render(request, 'error.html')

def handleLogin(request):
    if request.method == 'POST':
        username = request.POST['loginusername']
        password = request.POST['loginpass']

        user = authenticate(username = username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('home')
        else:
            messages.error(request, "Error!! Invalid Credentials.")
            return render(request, 'error.html')
    return render(request, 'error.html')


def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully Logged out")
    return redirect('home')

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        if len(name) < 2:
            messages.error(request, "Invalid Name. Name length must be greater than 1 !!")
            return redirect('home')

        if len(message) < 20:
            messages.error(request, "Invalid Message. Please fill the valid details and try again to contact us!!")
            return redirect('home')

        contact = Contact(name=name, email=email, message=message)
        contact.save()

        # send_mail(name, message, email, ['mishraritik86@gmail.com'])

        messages.success(request, "Thanks For Contacting Us. We will reply you soon.")
        return redirect('home')
    else:
        return render(request, 'error.html')
        
def appointment(request):
    if request.user.is_authenticated:
        patient = Patient.objects.filter(username=request.user.username)
        doctor = Doctor.objects.filter(username=request.user.username)   
        total = list(patient)+list(doctor)
        if len(total) >= 1:
            if(total[0].user_type=='doctor'):
                user_type = 'doctor'
                visible = total[0].visible
                appointment = Appointment.objects.filter(doc_name=request.user.first_name).filter(doc_email=request.user.email)
                # appointment = Appointment.objects.none()
            else:
                user_type = 'user'
                visible="None"
                appointment = Appointment.objects.filter(username=request.user)
        else:
            user_type = 'admin'
            visible="None"
            appointment = Appointment.objects.none()
    else:
        user_type = 'None'
        visible="None"
        appointment = Appointment.objects.none()
    doc_list = Doctor.objects.filter(visible='True')
    # if doc_list.count != 0:
    #     doc_name = [doc_list[i].first_name for i in range(len(doc_list))]
    #     doc_special = [doc_list[i].specialization for i in range(len(doc_list))]
    #     mylist = zip(doc_name, doc_special)
    # else:
    #     mylist = 'PK\x05\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    min_date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    max_date = (datetime.datetime.now() + datetime.timedelta(days=20)).strftime("%Y-%m-%dT%H:%M:%S")
    if request.user.is_superuser:
        pending_doc = Doctor.objects.filter(visible='False')
        if pending_doc.count == 0:
            pending_doc = Doctor.objects.none()
    else:
        pending_doc = Doctor.objects.none()

    appintment_list = []
    history = []
    for apt in appointment:
        if(apt.timing >= timezone.now()):
            appintment_list.append(apt)
        else:
            history.append(apt)

    appointments = {'appointments': appintment_list, 'user_type': user_type, 'pending_doc': pending_doc, 'doc_list':doc_list, 'min_date':min_date, 'max_date':max_date, 'visible':visible, 'history':history}
    return render(request, 'appointment.html', appointments)

# def bookAppoint(request, pk):
#     if request.method=='POST':
#         pat_name = request.POST['pat_name']
#         pat_email = request.POST['pat_email']
#         doc_name = request.POST['doc_name']
#         disease = request.POST['disease']
#         timing = request.POST['timing']
#         username = request.user
#         status = 'pending'
#         doc_email = Doctor.objects.get(first_name=doc_name).email
#         meeting_link = f"https://meet.jit.si/markdoc-{pat_name}-{doc_name}"
#         try:
#             appointment =  Appointment(username=username, pat_name=pat_name, pat_email=pat_email, doc_name=doc_name, doc_email=doc_email, disease=disease, timing=timing, status=status, meeting_link=meeting_link)
#             appointment.save()
#             messages.success(request, f"Hurray !! Your meeting is scheduled for {disease} on {timing} with {doc_name}")
#             return redirect('appointment')
#         except:
#             messages.error(request, "Sorry !! Our server is down due to some problem. Please try again after some time.")
#             return redirect('appointment')
#     else:
#         return render(request, 'error.html')
#     return render(request, 'error.html')

def bookAppoint(request, pk):
    if request.method=='POST':
        doctor = Doctor.objects.get(pk=pk)
        doc_name = doctor.first_name
        doc_email = doctor.email
        disease = doctor.specialization
        pat_name = request.POST['pat_name']
        pat_email = request.POST['pat_email']
        timing = request.POST['timing']
        status = 'pending'
        username = request.user
        meeting_link = f"https://meet.jit.si/markdoc-{pat_name}-{doc_name}"
        print(pat_email, pat_name, doc_name, doc_email, disease, timing, username, status, meeting_link)
        try:
            appointment =  Appointment(username=username, pat_name=pat_name, pat_email=pat_email, doc_name=doc_name, doc_email=doc_email, disease=disease, timing=timing, status=status, meeting_link=meeting_link)
            appointment.save()
            messages.success(request, f"Hurray !! Your meeting is scheduled for {disease} on {timing} with {doc_name}")
            return redirect('appointment')
        except:
            messages.error(request, "Sorry !! Our server is down due to some problem. Please try again after some time.")
            return redirect('appointment')
    else:
        return render(request, 'error.html')
    return render(request, 'error.html')

def confirm_doc(request, pk):
    if request.method=='POST':
        doctor = Doctor.objects.get(pk=pk)
        doctor.visible = 'True'
        doctor.save()
        messages.success(request, "Doctor is Visible now..")
        return redirect('appointment')
    return render(request, 'error.html')

def confirm_apt(request, pk):
    if request.method=='POST':
        apt = Appointment.objects.get(pk=pk)
        apt.status = 'confirmed'
        apt.save()
        messages.success(request, "Appointment is Scheduled...")
        return redirect('appointment')
    return render(request, 'error.html')

def cancel_apt(request, pk):
    if request.method=='POST':
        apt = Appointment.objects.get(pk=pk)
        status = request.POST['status']
        apt.status = status
        apt.save()
        messages.success(request, "Your Appointment is Cancelled Successfully...")
        return redirect('appointment')
    return render(request, 'error.html')

def test_center(request):
    return render(request, 'center.html')

def checkup(request):
    if request.method=='POST':
        box = {'stomach_pain':0, 'vomitting':0, 'weight_loss':0, 'cough':0, 'breathlessness':0, 'chest_pain':0, 'urination':0, 'fatigue':0, 'vision':0, 'back_pain':0, 'headache':0, 'acidity':0}
        name = request.POST['name']
        age = int(request.POST['age'])
        # stomach_pain = int(request.POST['stomach_pain'])
        # vomitting = int(request.POST['vomitting'])
        # weight_loss = int(request.POST['weight_loss'])
        # cough = int(request.POST['cough'])
        # breathlessness = int(request.POST['breathlessness'])
        # chest_pain = int(request.POST['chest_pain'])
        # urination = int(request.POST['urination'])
        # fatigue = int(request.POST['fatigue'])
        # vision = int(request.POST['vision'])
        # back_pain = int(request.POST['back_pain'])
        # headache = float(request.POST['headache'])
        # acidity = int(request.POST['acidity'])
        # gender = int(request.POST['gender'])
        # ca = int(request.POST['ca'])
        # thal = int(request.POST['thal'])
        # pregnancies = int(request.POST['pregnancies'])
        # insulin = int(request.POST['insulin'])
        # diab = float(request.POST['diab'])

        checkb = request.POST.getlist('checks[]')
        if not len(checkb)==0:
            for i in checkb:
                box[i]=1

        file = open('static/mark350.pickle', 'rb')
        clf = pickle.load(file)
        file.close()
        feature = [ box['stomach_pain'], box['vomitting'], box['weight_loss'], box['cough'], box['breathlessness'], box['chest_pain'], box['urination'], box['fatigue'], box['vision'], box['back_pain'], box['headache'], box['acidity']]
        info = clf.predict([feature])

        # file = open('static/heart.pickle', 'rb')
        # clf2 = pickle.load(file)
        # file.close()
        # feature2 = [age, gender, cp, bp, chol, fbs, restecg, beat, exang, oldpeak, slope, ca, thal]
        # info2 = clf2.predict_proba([feature2])[0][1]

        if info==0:
            disease = 'diabetes'
        else:
            disease = 'heart'

        doc_list = Doctor.objects.filter(visible='True').filter(specialization=disease)
        all_doc = Doctor.objects.filter(visible='True')

        doc = {'disease':disease, 'doc_list':doc_list, 'all_doc':all_doc}
        return render(request, 'doctors.html', doc)
    return render(request, 'error.html')