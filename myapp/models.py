from django.contrib.auth.models import AbstractUser
from django.db import models

from myapp.utils.sentiment_analysis import predict_sentiment
# myapp/models.py





class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.category.name} - {self.name}"





class Admin(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    role = models.CharField(max_length=50, default='admin')
    reset_password_token = models.CharField(max_length=100, blank=True, null=True)
    token_expiry = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.username
    

class Movie(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    release_date = models.DateField()
    description = models.TextField()
    poster = models.ImageField(upload_to='posters/',blank=True,null=True)
    director = models.CharField(max_length=100)
    duration = models.DurationField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    
    def average_rating(self):
        ratings = self.rating_set.all()  # Get all ratings for this movie
        if ratings.exists():
            return ratings.aggregate(models.Avg('score'))['score__avg']
        return None  # 

    def __str__(self):
        return self.title
class MovieImage(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='posters/')










class Theatre(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    rows = models.TextField()  # Stores rows as a comma-separated string like "A,B,C,D"
    seats_per_row = models.IntegerField()
    parking_available = models.TextField(blank=True, null=True) 
    food_and_beverage_options = models.TextField(blank=True, null=True)  # Description of options
    accessibility_options = models.TextField(blank=True, null=True)  # Accessibility information

    def __str__(self):
        return self.name


from django.db import models
from .models import Movie, Theatre

class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE)
    showtime = models.TimeField()
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    def __str__(self):
        return f"{self.movie.title} at {self.theatre.name} from {self.start_date} to {self.end_date} at {self.showtime}"


# models.py

class Seating(models.Model):
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE)
    row = models.CharField(max_length=1)  # Single character for row (e.g., 'A', 'B')
    seat_number = models.IntegerField()  # Seat number in the row
    is_booked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('theatre', 'row', 'seat_number')

    def __str__(self):
        return f"Row {self.row}, Seat {self.seat_number}"

    
from django.db import models
from django.conf import settings

class TheatreOwnerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username









from django.db import models
from django.conf import settings

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)






# models.py
from django.db import models
from django.contrib.auth.models import User
class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True,blank=True)  
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE,null=True,blank=True)  
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE,null=True,blank=True) 
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE,null=True,blank=True) 
    selected_seats = models.TextField(null=True,blank=True) 
    booking_date = models.DateTimeField(auto_now_add=True) 
    total_amount = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)  
    status = models.CharField(max_length=20, choices=[('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')], default='Confirmed')  
    payment=models.CharField(max_length=20,default="Success")
    refund_status = models.BooleanField(default=False) 
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)# New field for refund status


from django.db import models

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed')
    ], default='PENDING')
    payment_date = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Payment {self.id} - {self.user.username} - {self.amount}'


   




# In settings.py, you need to tell Django to use this custom model as the user model:
# class User(AbstractUser):
#     phone = models.CharField(max_length=15, blank=True, null=True)
#     address = models.TextField(blank=True, null=True)
#     role = models.CharField(max_length=15, choices=[('user', 'User'), ('theatre_owner', 'Theatre Owner')])
#     reset_password_token = models.CharField(max_length=100, blank=True, null=True)

#     def __str__(self):
#         return self.username


from django.conf import settings

class Feedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    booking = models.ForeignKey('Booking', on_delete=models.CASCADE)
    feedback_text = models.TextField()
    sentiment = models.CharField(max_length=20, blank=True, null=True)  # Ensure this field exists
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Feedback from {self.user} - {self.created_at}'


class Sentiment(models.Model):
    feedback = models.ForeignKey(Feedback, related_name='sentiments', on_delete=models.CASCADE)
    aspect = models.CharField(max_length=255)  # E.g., "service", "ambiance"
    sentiment = models.CharField(max_length=20)  # E.g., "positive", "negative"
    confidence = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Optional confidence score

    def __str__(self):
        return f'{self.aspect}: {self.sentiment}'

# models.py
from django.db import models
from django.conf import settings

class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    score = models.IntegerField()  # Assuming a rating scale of 1-5

    class Meta:
        unique_together = ('user', 'movie')  # Ensure a user can only rate a movie once

    def __str__(self):
        return f"{self.user.username} rated {self.movie.title} - {self.score}"
    
    
class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    showtime = models.DateTimeField()
    
    
class GiftVoucher(models.Model):
    code = models.CharField(max_length=50, unique=True)  # Unique voucher code
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)  # Discount amount
    expiration_date = models.DateField()  # Expiration date of the voucher
    is_active = models.BooleanField(default=True)  # Whether the voucher is active
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Optional: link to a user

    def __str__(self):
        return self.code
    
    # models.py
from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    MESSAGE_TYPE_CHOICES = [
        ('all', 'All Users'),
        ('theatre_owner', 'Theatre Owners'),
        ('admin', 'Admins'),
    ]

    message = models.TextField()
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.message_type}: {self.message[:20]}..."
    
    # models.py
from django.db import models



class Auditorium(models.Model):
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE, related_name='auditoriums')
    name = models.CharField(max_length=50)  # e.g., "Auditorium 1", "Auditorium 2"
    capacity = models.IntegerField()  # Number of seats in the auditorium

    def __str__(self):
        return f"{self.name} - {self.theatre.name}"
    
    
    # myapp/models.py


from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

# models.py

# VoucherUsage Model
class VoucherUsage(models.Model):
    voucher = models.ForeignKey(GiftVoucher, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    used_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} used {self.voucher.code} on {self.used_at}"
    
# myapp/models.py
from django.db import models
from django.conf import settings  # Import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use AUTH_USER_MODEL
    phone = models.CharField(max_length=15, blank=True, null=True)  # Allow phone to be optional
    address = models.TextField(blank=True, null=True)  # Allow address to be optional
    role = models.CharField(max_length=50, blank=True, null=True)  # Allow role to be optional

    def __str__(self):
        return f"{self.user.username}'s Profile"  # String representation for the Profile

# myapp/models.py
   # myapp/models.py



class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'movie')  # Ensure a user can only have one entry per movie

    def __str__(self):
        return f"{self.user.username}'s Wishlist - {self.movie.title}"
