# myapp/management/commands/send_due_date_reminders.py

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from LibraryApp.models import BookRequest
from datetime import timedelta
from LibraryMgmtProject import settings
class Command(BaseCommand):
    help = 'Send reminder emails for due date'

    def handle(self, *args, **options):
        # Calculate the due date threshold (e.g., 1 day before due date)
        due_date_threshold = timezone.now() + timedelta(days=1)

        # Get book requests due before the threshold
        book_requests = BookRequest.objects.filter(
            status_to_approve='Approved',
            due_date__lte=due_date_threshold
        )

        # Send reminder emails
        for request in book_requests:
            subject = f'Reminder: Return "{request.book.btitle}" Tomorrow'
            message = f"Hi {request.requested_by_student.username},\n\nThis is a reminder that you need to return the book '{request.book.btitle}' tomorrow.\nPlease make sure to return it on time to avoid any fines.\n\nThank you!"
            from_email = settings.EMAIL_HOST_USER  
            recipient_list = [request.requested_by_student.email]

            send_mail(subject, message, from_email, recipient_list)

        self.stdout.write(self.style.SUCCESS('Reminder emails sent successfully'))
