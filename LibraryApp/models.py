from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.
class User(AbstractUser):
	rt = [
		(0,'Guest'),
		(1,'Student'),
		(2,'Teacher'),
	]
	eid = models.CharField(max_length=20)
	role_type = models.IntegerField(default=0)

class StdProfile(models.Model):
	sg = [
		("h","Select Your Gender"),
		('M',"Male"),
		("F","Female")
	]
	b = [
		('G','----- Select Branch -----'),
		('CSE','Computer Science and Engineering'),
		('ECE','Electrical and Communication Engineering'),
		('EEE','Electrical and Electronics Engineering'),
		('CIVIL','Civil Engineering'),
		('MECH','Mechanical Engineering')
	]
	y = [
		('0','----- Select Year -----'),
		('1','1st Year'),
		('2','2nd Year'),
		('3','3rd Year'),
		('4','4th Year'),
	]
	sage = models.IntegerField()
	sgen = models.CharField(max_length=5,default='h',choices=sg)
	sbranch = models.CharField(max_length=6,default='G',choices=b)
	syear = models.CharField(max_length=3,default="0",choices=y)
	sstatus = models.BooleanField(default=0)
	std = models.OneToOneField(User,on_delete=models.CASCADE)

class TeacherProfile(models.Model):
	g = [
		("k","Select Your Gender"),
		('M',"Male"),
		("F","Female")
		]
	b = [
		('G','----- Select Branch -----'),
		('CSE','Computer Science and Engineering'),
		('ECE','Electrical and Communication Engineering'),
		('EEE','Electrical and Electronics Engineering'),
		('CIVIL','Civil Engineering'),
		('MECH','Mechanical Engineering')
	]
	tage = models.IntegerField()
	tgen = models.CharField(max_length=5,default='k',choices=g)
	tbranch = models.CharField(max_length=50,default='G',choices=b)
	texpr = models.IntegerField()
	tdesg = models.CharField(max_length=50)
	tstatus = models.BooleanField(default=0)
	tch = models.OneToOneField(User,on_delete=models.CASCADE)

    

class BookAdd(models.Model):
    b = [
		('G','----- Select Branch -----'),
		('CSE','Computer Science and Engineering'),
		('ECE','Electrical and Communication Engineering'),
		('EEE','Electrical and Electronics Engineering'),
		('CIVIL','Civil Engineering'),
		('MECH','Mechanical Engineering')
	]
    btitle = models.CharField(max_length=50)
    bauthor = models.CharField(max_length=50)
    bedition = models.CharField(max_length=20)
    bdes = models.TextField()
    bdept = models.CharField(max_length=50,choices=b,default='G')
    bstatus = models.BooleanField(default=False)
    num_copies = models.PositiveIntegerField(default=1)
    add_by = models.ForeignKey(User,on_delete=models.CASCADE)
    
class BookRequest(models.Model):
    book = models.ForeignKey(BookAdd, on_delete=models.CASCADE)
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    approved_by_teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,related_name='approved_by')
    requested_by_student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='book_requests_made',null=True)
    request_date = models.DateTimeField(auto_now_add=True)  
    approved_date = models.DateTimeField(null=True, blank=True)
    return_date = models.DateTimeField(null=True, blank=True)
    status_to_approve = models.CharField(max_length=20, choices=(
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected')
    ), default='Pending') 
    return_status = models.CharField(max_length=20, choices=(
        ('Pending', 'Pending'),
        ('Returned', 'Returned')
    ), default='Pending')	
    fine_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    due_date = models.DateTimeField(null=True, blank=True)

class Payment(models.Model):
	paid_by = models.ForeignKey(User,on_delete=models.CASCADE)
	paid_date = models.DateTimeField(auto_now_add=True)
	paid_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
	payment_status = models.BooleanField(default=False)
    
	

	

	
