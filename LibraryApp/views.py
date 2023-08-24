from django.shortcuts import render,redirect,get_object_or_404
from . models import *
from . forms import *
from django.contrib import messages
from django.core.mail import send_mail
from LibraryMgmtProject import settings
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from django.db.models import F
from datetime import datetime, timedelta

# Create your views here.

def home(request):
    return render(request,'html/home.html')

def about(request):
    return render(request,'html/about.html')

def contact(request):
    if  request.user.is_authenticated:
        if request.method == "POST":
            #name = request.POST['name']
            #email = request.POST['email']
            message = request.POST['message']
            subject = f"New Contact Form Submission from {request.user.username},On library.."
            message_body = f"Name: {request.user.username}\npin:{request.user.eid}\nEmail: {request.user.email}\nMessage: {message}"
            from_email = request.user.email  # Use the user's email as the sender
            recipient_list = settings.EMAIL_HOST_USER 

            try:
                send_mail(subject, message_body, from_email, [recipient_list])
                messages.success(request, 'Your message has been sent. We will get back to you soon.')
            except Exception as e:
                messages.error(request, 'An error occurred while sending your message. Please try again later.')
            student_subject = "Thank You for Contacting Us"
            student_message = f"Dear {request.user.username},\n\nThank you for contacting us. We have received your message and will get back to you soon.\n\nBest regards,\nThe Library Team"
            try:
                send_mail(student_subject,student_message,recipient_list,[from_email])
                
            except Exception as e:
                messages.error(request, 'An error occurred while sending your message. Please try again later.')
                
    else:
        if request.method == "POST":
            name = request.POST['name']
            email = request.POST['email']
            message = request.POST['message']
            subject = f'New Contact Form Submission from "{name}" unknown user,On library..'
            message_body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
            from_email = email  # Use the user's email as the sender
            recipient_list = settings.EMAIL_HOST_USER 

            try:
                send_mail(subject, message_body, from_email, [recipient_list])
                messages.success(request, 'Your message has been sent. We will get back to you soon.')
            except Exception as e:
                messages.error(request, 'An error occurred while sending your message. Please try again later.')            

    return render(request,'html/contact.html')

def register(request):    
    if request.method == 'POST':
        reg = UsForm(request.POST)
        print(reg)
        if reg.is_valid():
            h = reg.save(commit=False)
            sub = "Welcome To The Library Management System"
            des = f"Hi {h.username} , thankyou for regestering,your mail {h.email},please login to update your profile"
            y = settings.EMAIL_HOST_USER
            res = send_mail(sub,des,y,[h.email])
            #if res == 1:
               # print('mail sent')
           # else:
                #print('mail not sent')
            h.save()    
            return redirect('/lgin')
    reg = UsForm()
    return render(request,'html/register.html',{'rg':reg})

def stdprof(request):  
    return render(request,'html/stdprof.html')

#student request book logic
def showbook(request):
    c = BookAdd.objects.filter(bdept = 'CSE')
    e = BookAdd.objects.filter(bdept = 'ECE')
    ee = BookAdd.objects.filter(bdept = 'EEE')
    m = BookAdd.objects.filter(bdept = 'MECH')
    cv = BookAdd.objects.filter(bdept = 'CIVIL')
    return render(request,'html/reqbook.html',{'cse' : c,'ece' : e,'eee' : ee,'mech' : m,'civil' : cv})

def bookview(request,v):
    m = BookAdd.objects.get(id = v)
    isexist = BookRequest.objects.filter(book=m, requested_by=request.user).exists()
    requested_books_count = BookRequest.objects.filter(requested_by=request.user).count()
    if request.method == "POST" :
        if isexist:
            messages.warning(request, 'Duplicate book request not allowed.')
            return redirect('/sdashboard')
        elif m.num_copies <=0 :
            messages.warning(request,'Out of Stock...')
            return redirect('/sdashboard')
        elif requested_books_count >= 6:
            messages.warning(request,'You have reached the maximum book requests')
            return redirect('/sdashboard')
        else:
            reqbk = BookRequest(book=m,requested_by=request.user,requested_by_student=request.user)
            reqbk.save()
            messages.success(request,'BookAdded Success fully')
            return redirect('/sdashboard')     
    return render(request,'html/bookview.html',{'bookview' : m})

#book record storage logic dispaly
#fines logic
def total_fine(book_fine):
    t = 0
    for i in book_fine:
        t += i.fine_amount
    return t

def sdashboard(request):
    d = BookRequest.objects.filter(requested_by = request.user)
    aprove = BookRequest.objects.filter(requested_by = request.user,status_to_approve = 'Approved')
    book_fine = BookRequest.objects.filter(
        requested_by_student=request.user,
        status_to_approve='Approved',
        return_status='Returned'
    )
    approved_books = BookRequest.objects.filter(
        requested_by_student=request.user,
        status_to_approve='Approved'
    )
    all_books_returned = all(book.return_status == 'Returned' for book in approved_books)

    total = total_fine(book_fine) 
    return render(request,'html/sdashboard.html',{'book_requests' : d,'book_approved' : aprove,'total_fine' : total,'pay' : all_books_returned})

def cancel_req(request,bk):
    book_fine = BookRequest.objects.filter(
        requested_by_student=request.user,
        status_to_approve='Approved',
        return_status='Returned'
    )
    money = total_fine(book_fine)
    if request.method == "POST":
        book_request = BookRequest.objects.get(id = bk)
       
        if book_request.status_to_approve != 'Approved':
            book_request.delete()
            messages.success(request, 'Book request cancelled successfully.')
        elif money == 0 and book_request.return_status == 'Returned':
            book_request.delete()
            messages.success(request,'Book Submited..')
        else:
            messages.warning(request,'Not Possible Action')    
        
    return redirect('/sdashboard')


#student profile update
def update(request): 
    o = StdProfile.objects.all()
    dt = []
    for i in o:
        dt.append(i.std_id)
    if request.user.id not in dt:
        if request.method == "POST":
            up = StdForm(request.POST)
            if up.is_valid():
                h = up.save(commit=False)
                h.sstatus = 1
                h.std_id = request.user.id
                h.save()
            return redirect('/stdprof')
        up = StdForm()
        return render(request,'html/update.html',{'std' : up})    
    else:
        x = StdProfile.objects.get(std_id = request.user.id)
        if request.method == "POST":
            up = StdForm(request.POST,instance=x)
            if up.is_valid():
                up.save()
                return redirect('/stdprof')
        up = StdForm(instance=x)
        return render(request,'html/update.html',{'std' : up})        
    
def techprof(request):
    return render(request,'html/teachprof.html')

#teacher profile update
def updatet(request):
    tea = TeacherProfile.objects.all()
    mx = []
    for i in tea:
        mx.append(i.tch_id)
    if request.user.id not in mx:
        if request.method == "POST":
            h = TeacherForm(request.POST)
            if h.is_valid():
                rex = h.save(commit=False)
                rex.tstatus = 1
                rex.tch_id = request.user.id
                rex.save()
                return redirect('/teachprof')    
        tech = TeacherForm()
        return render(request,'html/updatet.html',{'tea' : tech})
    else: 
        tcx = TeacherProfile.objects.get(tch_id = request.user.id)
        if request.method == "POST":
            tat = TeacherForm(request.POST,instance=tcx)
            if tat.is_valid():
                tat.save()
                return redirect('/teachprof')
        tech = TeacherForm(instance=tcx)
        return render(request,'html/updatet.html',{'tea' : tech}) 
def addbook(request):
    #b = BookAdd.objects.all()
    b = BookAdd.objects.filter(add_by=request.user)
    if request.method == "POST":
        bk = AddBookForm(request.POST)
        if bk.is_valid():
            h = bk.save(commit=False)
            h.add_by_id = request.user.id
            h.bstatus = True
            h.save()
            return redirect('/addbook')
    bk = AddBookForm()
    return render(request,'html/addbook.html',{'book' : bk,'sdid' : b})   
  
def editbook(request,p):
    g = BookAdd.objects.get(id = p)
    if request.method == "POST":
        bu = AddBookForm(request.POST,instance=g)
        if bu.is_valid():
            bu.save()
            return redirect('/addbook')
    bu = AddBookForm(instance=g)    
    return render(request,'html/editbook.html',{'edit' : bu})
def delbook(request,d):
    g = BookAdd.objects.get(id = d)
    if request.method == "POST":
        g.delete()
        return redirect('/addbook')
    return render(request,'html/delbook.html',{'delbk' : g})


def tdashboard(request):
    p = BookRequest.objects.filter(status_to_approve = 'Pending')
    ap = BookRequest.objects.filter(Q(status_to_approve='Approved') & Q(return_status='Pending'))
    r = BookRequest.objects.filter(return_status = 'Returned')
    
    return render(request,'html/tdashboard.html',{'pending':p,'approve':ap,'return_status' : r})



def approve_book_request(request, request_id):
    book_request = BookRequest.objects.get(id = request_id)
    if book_request.book.num_copies > 0:
        book_request.status_to_approve = 'Approved'
        book_request.approved_date = timezone.now()
        due_date = book_request.approved_date + timedelta(days=1)#14 days from date of approval
        book_request.due_date = due_date
        book_request.approved_by_teacher = request.user
            # Decrement the available copies of the book by 1
        book = book_request.book
        BookAdd.objects.filter(id=book.id).update(num_copies=F('num_copies') - 1)
        book_request.save()
        subject = 'Book Request Approved'
        message = f"\nname : {book_request.requested_by_student}\npin : {book_request.requested_by_student.eid}"
        message += f"\nYour book request for '{book_request.book.btitle}' has been approved.\n"
        message += f"\nApproved Date: {book_request.approved_date}\n"
        message += f"\nDue Date: {due_date}\n"
        message += f"\nPlease make sure to return the book ,with in the due date ,otherwise you will be imposed of fine "
        message += f"\nDon't Reply...."
        recipient = book_request.requested_by.email

        send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient])
        messages.success(request,'Approved Successfully')
    else:
        messages.warning(request,'Out Of Stock...') 

      
    return redirect('/tdashboard')

def reject_book_request(request, request_id):
    book_request = BookRequest.objects.get(id = request_id)
    book_request.status_to_approve = 'Rejected'
    book_request.save()   
    subject = 'Book Request Rejected'
    message = f"\nname : {book_request.requested_by_student}\npin : {book_request.requested_by_student.eid}"
    message += f"\nYour book request for '{book_request.book.btitle}' has been rejected.\npls contact to your respected Teacher"
    message += f"\nDon't Reply...."
    recipient = book_request.requested_by.email
    send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient])
    messages.warning(request,'Rejected Successfully')   
    return redirect('/tdashboard')
   


def return_book(request, request_id):
    book_request = get_object_or_404(BookRequest, id=request_id)
    if request.method == 'POST':
        if book_request.return_status == 'Returned':
            messages.warning(request, 'Book has already been returned.')
        elif book_request.status_to_approve == 'Approved':
            book_request.return_status = 'Returned'
           # Increment the available copies of the book by 1
            book = book_request.book
            BookAdd.objects.filter(id=book.id).update(num_copies=F('num_copies') + 1)
            #static_return_date_str = '2023-08-29 23:59:00'
            #static_return_date = datetime.strptime(static_return_date_str, '%Y-%m-%d %H:%M:%S')
            #static_return_date_aware = timezone.make_aware(static_return_date, timezone.get_current_timezone())
            #book_request.return_date = static_return_date_aware
            book_request.return_date = timezone.now()
            book_request.save()
        # Calculate fine amount based on due date and actual return date
            due_date = book_request.due_date
            actual_return_date = book_request.return_date
            fine_amount = 0  
            #print(actual_return_date,due_date)
            if actual_return_date > due_date:

                # Calculate the number of days late
                days_late = (actual_return_date - due_date).days
                # Calculate the fine amount based on the fine per day rate
                fine_amount = days_late * 20  

            
            book_request.fine_amount = fine_amount
            book_request.save()


            subject = 'Book Returned..'
            message = f"\nname : {book_request.requested_by_student}\npin : {book_request.requested_by_student.eid}"
            message += f"\nYour book  '{book_request.book.btitle}' has been returned on {book_request.return_date}.\n"
            message += f"\nDon't Reply...."
            recipient = book_request.requested_by.email
            send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient])
            messages.success(request, 'Book returned successfully.')
            
                
        else:
            messages.info(request,'Book must to Approved.')    
    
    return redirect('/sdashboard')

def payfine(request):
    book_fine = BookRequest.objects.filter(
        requested_by_student=request.user,
        status_to_approve='Approved',
        return_status='Returned'
    )
    total = total_fine(book_fine) 
    approved_books = BookRequest.objects.filter(
        requested_by_student=request.user,
        status_to_approve='Approved'
    )
    all_books_returned = all(book.return_status == 'Returned' for book in approved_books)
    if request.method == "POST":
        if all_books_returned:
            #fee    = request.POST['amt']
            mobile_no = request.POST['mobile']
            card_no   = request.POST['debit']
            payment = Payment.objects.create(
                paid_by=request.user,
                paid_amount=total,
                paid_date = timezone.now(),
                payment_status=True,
            )
            for i in book_fine:
                i.fine_amount = 0
                i.save()
            subject = 'Payment Successful'
            message = f'Your payment of Rs.{total}/- has been successfully processed.'
            message += f'\n debeted from {card_no}xxxx'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [request.user.email]
            send_mail(subject, message, from_email, recipient_list) 
            messages.success(request,'payment sucessfull')
            return redirect('/payfine')
        else:
            messages.warning(request,'payment failed / you must return all the aproved books')
            return redirect('/payfine')
        
    payobj = Payment.objects.filter(paid_by = request.user)

    return render(request,'html/payfine.html',{'fine' : total,'payhistory' : payobj})
