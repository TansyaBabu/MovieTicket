# myapp/management/commands/send_reminders.py
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from myapp.models import Booking

class Command(BaseCommand):
    help = 'Send email reminders for upcoming showtimes'

    def handle(self, *args, **kwargs):
        # Get current time and time 1 hour from now
        now = timezone.now()
        reminder_time = now + timedelta(hours=1)

        # Get bookings that are within the next hour
        bookings = Booking.objects.filter(showtime__showtime__range=(now, reminder_time))

        for booking in bookings:
            subject = 'Reminder: Your Upcoming Showtime'
            message = f"""
            Hi {booking.user.username},

            This is a reminder for your upcoming showtime:

            Movie: {booking.movie.title}
            Date: {booking.showtime.date}
            Time: {booking.showtime.showtime}
            Theatre: {booking.theatre.name}

            Enjoy the show!

            Best,
            Your Movie Booking Team
            """
            send_mail(subject, message, 'your_email@gmail.com', [booking.user.email])
            self.stdout.write(self.style.SUCCESS(f'Sent reminder to {booking.user.email}'))