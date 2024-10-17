from myapp.utils.sentiment_analysis import predict_sentiment
from .models import Booking, Payment, User,  Admin,  Category
import json
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from uuid import uuid4
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.admin.models import LogEntry
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login as auth_login

from django.shortcuts import render, get_object_or_404, redirect
from .models import Category
from django.shortcuts import render, get_object_or_404, redirect
from .models import Category
from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie
from django.contrib import messages
from django.shortcuts import render
from .models import Movie
from django.core.paginator import Paginator

from django.shortcuts import render
from .models import Movie
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Subcategory



from django.shortcuts import render, redirect, get_object_or_404

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Category

def list_categories(request):
    categories = Category.objects.all()
    return render(request, 'list_categories.html', {'categories': categories})
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        
       
        Category.objects.create(name=name, description=description)
        
      
        return redirect('list_categories')
    
    return render(request, 'admin/add_category.html')

from django.shortcuts import render, redirect, get_object_or_404
from .models import Category

def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        name = request.POST.get('name').strip()  # Removing leading/trailing spaces
        description = request.POST.get('description').strip()

        if not name or not description:  # Check if either field is blank
            category.delete()  # Delete the category if fields are blank
            return redirect('list_categories')
        
        category.name = name
        category.description = description
        category.save()
        return redirect('list_categories')

    return render(request, 'admin/edit_category.html', {'category': category})


def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('list_categories')
    return render(request, 'admin/delete_category.html', {'category': category})




# Index View
def index(request):
    # Booking.objects.all().delete()
    # Feedback.objects.all().delete()
    return render(request, 'index.html')
## myapp/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .models import Profile,User  # Import only Profile, not User

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email'].strip().lower()
        phone = request.POST['phone']
        address = request.POST['address']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            return render(request, 'register.html', {'error': 'Passwords do not match'})

        hashed_password = make_password(password)

        try:
            # Create User instance with only username and email
            user = User(username=username, email=email, password=hashed_password)
            user.save()  # Save the User instance first
            
            # Create Profile instance with additional fields
            Profile.objects.create(user=user, phone=phone, address=address, role='user')
            return redirect('login')
        except Exception as e:
            return render(request, 'register.html', {'error': str(e)})

    return render(request, 'register.html')




# views.py
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User  # Ensure this is your custom user model

# Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Check if admin
        if username == 'tansya' and password == 'tansya@23':
            return redirect('admin_dashboard')

        # Authenticate user using Django's built-in authentication system
        user = authenticate(request, username=username, password=password)
        
        if user:
            auth_login(request, user)
            profile=Profile.objects.get(user=user)
            if profile.role == 'user':
                return redirect('user_dashboard')
            elif profile.role == 'theatre_owner':
                return redirect('theatre_owner_dashboard')

        messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')



from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Movie

# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import User

@login_required
def user_dashboard(request):
    user = request.user
    # Fetch movies and other data as needed
    movies = []  # Replace with actual queryset or list of movies
    return render(request, 'user_dashboard.html', {'user': user, 'movies': movies})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required





# Admin Dashboard
def admin_dashboard(request):
    log_entries = LogEntry.objects.all()
    return render(request, 'admin/admin_dashboard.html', {'log_entries': log_entries})

# Other Views


def contact(request):
    return render(request, 'contact.html')


# views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.core.files.storage import FileSystemStorage
from .models import Movie, Category

def list_movies(request):
    movies = Movie.objects.all()
    return render(request, 'list_movies.html', {'movies': movies})
#from datetime import timedelta
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.utils.dateparse import parse_date
from .models import Movie, Category
from django.core.exceptions import ValidationError

def add_movie(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        category_id = request.POST.get('category')
        release_date_str = request.POST.get('release_date')
        description = request.POST.get('description')
        poster_image = request.FILES.get('poster')
        director = request.POST.get('director')
        duration_str = request.POST.get('duration')
        price_str = request.POST.get('price')

        try:
            # Check if title already exists
            if Movie.objects.filter(title=title).exists():
                return render(request, 'admin/add_movie.html', {
                    'categories': Category.objects.all(),
                    'error_message': 'A movie with this title already exists.'
                })

            # Convert release_date from string to date
            release_date = parse_date(release_date_str)
            if not release_date:
                raise ValidationError("Invalid release date format")

            # Convert duration from string to timedelta
            hours, minutes = map(int, duration_str.split(':'))
            duration = timedelta(hours=hours, minutes=minutes)

            category = Category.objects.get(id=category_id)

            # Validate and convert the price
            if not price_str or float(price_str) <= 0:
                raise ValidationError("Price must be a positive number greater than zero")
            price = float(price_str)

            # Handle the file upload
            if not poster_image:
                raise ValidationError("No poster image uploaded")

            # Save the poster image
            poster_path = default_storage.save(poster_image.name, poster_image)

            # Create the movie object
            Movie.objects.create(
                title=title,
                category=category,
                release_date=release_date,
                description=description,
                poster=poster_path,
                director=director,
                duration=duration,
                price=price,
            )

            return redirect('list_movies')  # Redirect to the list of movies after adding

        except (ValidationError, Category.DoesNotExist) as e:
            # Handle validation errors or category not found
            return render(request, 'admin/add_movie.html', {
                'categories': Category.objects.all(),
                'error_message': str(e)
            })

    categories = Category.objects.all()
    return render(request, 'admin/add_movie.html', {'categories': categories})


from django.http import JsonResponse
from .models import Movie

def check_title_exists(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        exists = Movie.objects.filter(title=title).exists()
        return JsonResponse({'exists': exists})
    return JsonResponse({'exists': False})


from datetime import timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ValidationError
from django.contrib import messages
import re

def edit_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    categories = Category.objects.all()

    if request.method == 'POST':
        title = request.POST['title']
        category_id = request.POST['category']
        release_date = request.POST['release_date']
        description = request.POST['description']
        director = request.POST['director']
        price = request.POST['price']
        duration_str = request.POST['duration']

        # Title validation: only alphabets and spaces
        if not re.match(r'^[A-Za-z\s]+$', title):
            messages.error(request, "Title must contain only alphabets and spaces.")
            return render(request, 'admin/edit_movie.html', {'movie': movie, 'categories': categories})

        # Director validation: only alphabets and spaces
        if not re.match(r'^[A-Za-z\s]+$', director):
            messages.error(request, "Director must contain only alphabets and spaces.")
            return render(request, 'admin/edit_movie.html', {'movie': movie, 'categories': categories})

        # Price validation: must be a valid number greater than zero
        try:
            price = float(price)
            if price <= 0:
                raise ValueError
        except ValueError:
            messages.error(request, "Price must be a valid number greater than zero.")
            return render(request, 'admin/edit_movie.html', {'movie': movie, 'categories': categories})

        # Duration validation
        try:
            hours, minutes = map(int, duration_str.split(':'))
            duration = timedelta(hours=hours, minutes=minutes)
        except ValueError:
            messages.error(request, "Duration must be in the format HH:MM.")
            return render(request, 'admin/edit_movie.html', {'movie': movie, 'categories': categories})

        # Poster validation: must be a png or jpeg format
        if 'poster' in request.FILES:
            poster = request.FILES['poster']
            if not poster.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                messages.error(request, "Poster must be in PNG or JPEG format.")
                return render(request, 'admin/edit_movie.html', {'movie': movie, 'categories': categories})
            movie.poster = poster

        # Save the movie if all validations pass
        movie.title = title
        movie.category_id = category_id
        movie.release_date = release_date
        movie.description = description
        movie.director = director
        movie.duration = duration
        movie.price = price

        movie.save()
        messages.success(request, "Movie updated successfully.")
        return redirect('list_movies')

    return render(request, 'admin/edit_movie.html', {'movie': movie, 'categories': categories})



def delete_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        movie.delete()
        return redirect('list_movies')
    return render(request, 'admin/delete_movie.html', {'movie': movie})

# myapp/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Movie  # Import your Movie model
@login_required
def user_profile(request):
    user = request.user
    # Print or log user attributes to debug
    print(user.name)
    
    movies = Movie.objects.all()
    
    context = {
        'user': user,
        'movies': movies,
    }
    
    return render(request, 'user_profile.html', context)




@login_required
def user_profile(request):
    # Fetch the user profile data and pass it to the template
    user = request.user
    # Assuming you fetch movies elsewhere or use a different approach
    movies = [] # Replace with actual query to get movies
    return render(request, 'user_profile.html', {'user': user, 'movies': movies})

from django.shortcuts import render
from .models import Category  # Import your Category model

def list_categories_for_users(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'list_categories_for_users.html', context)


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import TheatreOwnerProfile  # Adjust according to your model

@login_required
def theatre_owner_profile(request):
    # Assuming `TheatreOwnerProfile` model is related to the `User` model
    try:
        profile = TheatreOwnerProfile.objects.get(user=request.user)
    except TheatreOwnerProfile.DoesNotExist:
        profile = None

    return render(request, 'theatre_owner/theatre_owner_profile.html', {'user': request.user, 'profile': profile})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User  # Adjust import based on your user model

@login_required
def update_theatre_owner_profile(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        # Update the user's profile information
        user = request.user
        user.username = name
        user.email = email
        user.phone = phone
        user.address = address
        user.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('theatre_owner_profile')
    
    return render(request, 'theatre_owner/update_theatre_owner_profile.html')




from django.shortcuts import render


def movie_category(request, category):
    # Filter movies by category
    movies = Movie.objects.filter(category__name=category)
    
    # Get all showtimes related to these movies
   
    
    # Pass movies and showtimes to template
    return render(request, 'movie_category.html', {
        'category': category,
        'movies': movies,
      
    })


# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Theatre  # Assuming you have a Theatre model

def add_theatre(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')
        rows = request.POST.get('rows')
        seats_per_row = request.POST.get('seats_per_row')
        parking_available = request.POST.get('parking_available') == 'on'
        food_and_beverage_options = request.POST.get('food_and_beverage_options')
        accessibility_options = request.POST.get('accessibility_options')

        # Check if the theatre already exists
        if Theatre.objects.filter(name=name).exists():
            messages.error(request, "Theatre already exists")
            return render(request, 'theatre_owner/add_theatre.html')

        # Create the new theatre
        Theatre.objects.create(
            name=name,
            location=location,
            rows=rows,
            seats_per_row=seats_per_row,
            parking_available=parking_available,
            food_and_beverage_options=food_and_beverage_options,
            accessibility_options=accessibility_options
        )
        messages.success(request, "Theatre added successfully")
        return redirect('theatre_owner_dashboard')  # Redirect to the dashboard or theatre list

    return render(request, 'theatre_owner/add_theatre.html')
# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Theatre

def edit_theatre(request, theatre_id):
    theatre = get_object_or_404(Theatre, id=theatre_id)

    if request.method == 'POST':
        # Update theatre fields from the form data
        theatre.name = request.POST.get('name')
        theatre.location = request.POST.get('location')
        theatre.rows = request.POST.get('rows')
        theatre.seats_per_row = int(request.POST.get('seats_per_row'))  # Ensure this is an integer
        theatre.parking_available = request.POST.get('parking_available', '')  # Checkbox handling
        theatre.food_and_beverage_options = request.POST.get('food_and_beverage_options', '')
        theatre.accessibility_options = request.POST.get('accessibility_options', '')

        # Save the updated theatre instance
        try:
            theatre.save()
            messages.success(request, "Theatre updated successfully!")
            return redirect('list_theatres')  # Redirect to a list of theatres or any other page
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return render(request, 'theatre_owner/edit_theatre.html', {'theatre': theatre})

    return render(request, 'theatre_owner/edit_theatre.html', {'theatre': theatre})

from django.shortcuts import redirect, get_object_or_404
from .models import Theatre

def delete_theatre(request, theatre_id):
    theatre = get_object_or_404(Theatre, id=theatre_id)
    theatre.delete()
    return redirect('list_theatres')  # Redirect to a list of theatres or any other page


def list_theatres(request):
    theatres = Theatre.objects.all()
    for theatre in theatres:
        theatre.rows_list = theatre.rows.split(',')  # Convert rows to a list
        theatre.total_seats = len(theatre.rows_list) * theatre.seats_per_row  # Calculate total seats
    return render(request, 'theatre_owner/list_theatres.html', {'theatres': theatres})
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.dateparse import parse_date
from django.utils.timezone import make_aware
from datetime import datetime, timedelta
from .models import Showtime, Movie, Theatre
from datetime import datetime 

def add_showtime(request):
    if request.method == 'POST':
        movie_id = request.POST.get('movie')
        theatre_id = request.POST.get('theatre')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        showtimes = request.POST.getlist('showtime')  # Get all showtime inputs

        # Validate inputs
        if not all([movie_id, theatre_id, start_date, end_date, showtimes]):
            messages.error(request, "All fields are required.")
            return render(request, 'theatre_owner/add_showtime.html', {
                'movies': Movie.objects.all(),
                'theatres': Theatre.objects.all(),
            })

        try:
            movie = Movie.objects.get(id=movie_id)
            theatre = Theatre.objects.get(id=theatre_id)
            start_date = parse_date(start_date)
            end_date = parse_date(end_date)

            if start_date >= end_date:
                raise ValueError("End date must be after the start date.")

            from datetime import datetime  # Ensure this import is present

            for showtime in showtimes:
                time = datetime.strptime(showtime, '%H:%M').time()
                current_date = start_date
                while current_date <= end_date:
                    showtime_datetime = make_aware(datetime.combine(current_date, time))
                    
                    # Check if the showtime already exists
                    if not Showtime.objects.filter(movie=movie, theatre=theatre, showtime=showtime_datetime).exists():
                        Showtime.objects.create(
                            movie=movie,
                            theatre=theatre,
                            showtime=showtime_datetime,
                            start_date=start_date,
                            end_date=end_date
                        )
                    current_date += timedelta(days=1)

            messages.success(request, "Showtimes added successfully!")
            return redirect('view_showtimes')

        except (Movie.DoesNotExist, Theatre.DoesNotExist):
            messages.error(request, "Invalid movie or theatre selection.")
        except ValueError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    # If GET request or if there's an error, render the form
    return render(request, 'theatre_owner/add_showtime.html', {
        'movies': Movie.objects.all(),
        'theatres': Theatre.objects.all(),
    })


from django.shortcuts import render, get_object_or_404, redirect
from django.utils.dateparse import parse_date
from django.utils.timezone import make_aware
import datetime
from .models import Showtime, Movie, Theatre
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import make_aware
from datetime import datetime
from .models import Showtime, Movie, Theatre
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import make_aware
from datetime import datetime
from .models import Showtime, Movie, Theatre
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import make_aware
from datetime import datetime
from .models import Showtime, Movie, Theatre

def edit_showtime(request, pk):
    showtime = get_object_or_404(Showtime, id=pk)

    if request.method == 'POST':
        movie_id = request.POST.get('movie')
        theatre_id = request.POST.get('theatre')
        showtime_str = request.POST.get('showtime')
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')

        error_message = None

        try:
            # Directly parse date and time from the input
            showtime_time = datetime.strptime(showtime_str, '%H:%M').time()
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

            # Ensure the end date is not before the start date
            if end_date < start_date:
                error_message = 'End date must be after the start date.'

            # Combine start date and showtime time
            showtime_datetime = make_aware(datetime.combine(start_date, showtime_time))
        except (ValueError, TypeError):
            error_message = 'Invalid date or time format. Please use correct formats.'

        if not error_message:
            try:
                movie = Movie.objects.get(id=movie_id)
                theatre = Theatre.objects.get(id=theatre_id)
            except Movie.DoesNotExist:
                error_message = 'Selected movie does not exist.'
            except Theatre.DoesNotExist:
                error_message = 'Selected theatre does not exist.'

        if not error_message:
            # Update the showtime entry
            showtime.movie = movie
            showtime.theatre = theatre
            showtime.showtime = showtime_datetime
            showtime.start_date = start_date
            showtime.end_date = end_date
            showtime.save()
            return redirect('theatre_owner_dashboard')

        # Render form with error message
        return render(request, 'theatre_owner/edit_showtime.html', {
            'showtime': showtime,
            'movies': Movie.objects.all(),
            'theatres': Theatre.objects.all(),
            'error_message': error_message
        })

    return render(request, 'theatre_owner/edit_showtime.html', {
        'showtime': showtime,
        'movies': Movie.objects.all(),
        'theatres': Theatre.objects.all()
    })
from django.shortcuts import redirect, get_object_or_404
from .models import Showtime

def delete_showtime(request, pk):
    showtime = get_object_or_404(Showtime, pk=pk)
    if request.method == 'POST':
        showtime.delete()
        messages.success(request, "Showtime deleted successfully.")
        return redirect('view_showtimes')
    return render(request, 'theatre_owner/delete_showtime.html', {'showtime': showtime})





from django.shortcuts import render, redirect, get_object_or_404
from .models import Showtime, Movie, Theatre
from django.utils.dateparse import parse_date
from django.utils.timezone import make_aware
import datetime

def showtime_list(request):
    showtimes = Showtime.objects.all().order_by('showtime')
    return render(request, 'theatre_owner/showtime_list.html', {'showtimes': showtimes})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Showtime, Movie, Theatre
from django.utils.dateparse import parse_date
from django.utils.timezone import make_aware
from datetime import datetime, timedelta  # Ensure correct import

def view_showtimes(request):
    showtimes = Showtime.objects.all().order_by('showtime')
    return render(request, 'theatre_owner/view_showtimes.html', {'showtimes': showtimes})





from django.shortcuts import render
def theatre_owner_dashboard(request):
    showtimes = Showtime.objects.all()  # Adjust as needed
    return render(request, 'theatre_owner/theatre_owner_dashboard.html', {'showtimes': showtimes})


def movie_showtimes(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    showtimes = Showtime.objects.filter(movie=movie)
    return render(request, 'movie_showtimes.html', {
        'movie': movie,
        'showtimes': showtimes
    })


# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Seating, Theatre

def add_seating(request, theatre_id):
    theatre = get_object_or_404(Theatre, id=theatre_id)
    
    if request.method == 'POST':
        row = request.POST.get('row')
        seat_number = request.POST.get('seat_number')
        
        # Ensure seat_number is correctly formatted (e.g., 1, 2, 3, ...)
        if not seat_number.isdigit():
            return HttpResponse("Seat number must be a valid integer.", status=400)

        Seating.objects.create(theatre=theatre, row=row, seat_number=seat_number)
        return redirect('theatre_owner_dashboard')  # Or another relevant URL
    
    rows = theatre.rows.split(',')
    existing_seats = Seating.objects.filter(theatre=theatre).order_by('row', 'seat_number')

    return render(request, 'theatre_owner/add_seating.html', {
        'theatre': theatre,
        'rows': rows,
        'existing_seats': existing_seats
    })

def edit_seating(request, seating_id):
    seating = get_object_or_404(Seating, id=seating_id)
    
    if request.method == 'POST':
        seating.row = request.POST.get('row')
        seating.seat_number = request.POST.get('seat_number')
        seating.save()
        return redirect('showtime_list')  # Or another relevant URL
    
    return render(request, 'theatre_owner/edit_seating.html', {'seating': seating})

def delete_seating(request, seating_id):
    seating = get_object_or_404(Seating, id=seating_id)
    seating.delete()
    return redirect('showtime_list')  # Or another relevant URL






def seating_view(request, theatre_id):
    # Fetch seating data from the database (pseudo-code)
    seating_arrangement = {
        'A': [{'number': 1, 'status': 'available'}, {'number': 2, 'status': 'taken'}, ...],
        'B': [{'number': 1, 'status': 'available'}, {'number': 2, 'status': 'available'}, ...],
        # Add more rows as needed
    }
    theatre = Theatre.objects.get(id=theatre_id)
    return render(request, 'seating_view.html', {
        'theatre': theatre,
        'seating_arrangement': seating_arrangement
    })




from django.shortcuts import render
from myapp.models import User  # Ensure this is your custom user model

def view_customers(request):
    customers = User.objects.all()  # Fetch all users
    return render(request, 'admin/view_customers.html', {'customers': customers})


# View to Activate a User
@login_required
def activate_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if not user.is_active:
        user.is_active = True
        user.save()
        messages.success(request, 'User activated successfully.')
    else:
        messages.info(request, 'User is already active.')

    return redirect('admin/view_customers')

# View to Deactivate a User
@login_required
def deactivate_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.is_active:
        user.is_active = False
        user.save()
        messages.success(request, 'User deactivated successfully.')
    else:
        messages.info(request, 'User is already deactivated.')

    return redirect('admin/view_customers')

# View to Remove a User
@login_required
def remove_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User removed successfully.')
        return redirect('admin/view_customers')

    return redirect('admin/view_customers')

from django.http import JsonResponse
from .models import Movie

def check_title_exists(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        exists = Movie.objects.filter(title=title).exists()
        return JsonResponse({'exists': exists})
    return JsonResponse({'exists': False}, status=400)

def logout_view(request):
    request.session.flush()
    return redirect("index")


import random
import string
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import UserProfile


@login_required
def update_profile(request):
    if request.method == 'POST':
        # Get or create the user profile
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)

        # Update profile fields
        name = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        # Add print statements for debugging
        print(f'Updating profile for user: {request.user}')
        print(f'Name: {name}, Email: {email}, Phone: {phone}, Address: {address}')
        
        if name:
            user_profile.name = name
        if email:
            request.user.email = email
        if phone:
            user_profile.phone = phone
        if address:
            user_profile.address = address
        
        # Save the updated profile and user
        try:
            user_profile.save()
            request.user.save()
            print('Profile updated successfully.')
        except Exception as e:
            print(f'Error updating profile: {e}')
        
        # Optionally send an email notification about the profile update
        send_mail(
            'Profile Updated',
            'Your profile has been successfully updated.',
            settings.DEFAULT_FROM_EMAIL,
            [request.user.email],
            fail_silently=False,
        )
        
        # Redirect to a success page or profile page after updating
        return redirect('user_dashboard')
    
    # Handle GET requests
    return render(request, 'update_profile.html')






from django.shortcuts import render
from .models import Theatre

def admin_theatre_list(request):
    # Fetch all theatres from the database
    theatres = Theatre.objects.all()

    # Process each theatre to include additional information
    for theatre in theatres:
        # Convert rows to a list for display purposes
        theatre.rows_list = theatre.rows.split(',')
        # Calculate the total number of seats
        theatre.total_seats = len(theatre.rows_list) * theatre.seats_per_row
    
    # Render the template with the theatres data
    return render(request, 'admin/admin_theatre_list.html', {'theatres': theatres})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Seating, Theatre, Showtime, Movie, Booking

from django.shortcuts import render, get_object_or_404, redirect
from .models import Theatre, Showtime, Movie, Booking, Seating
from django.utils import timezone

def view_seating(request, theatre_id):
    theatre = get_object_or_404(Theatre, id=theatre_id)
    
    # Fetch seating arrangement for the given theatre
    seats = Seating.objects.filter(theatre=theatre).order_by('row', 'seat_number')
    rows = theatre.rows.split(',')  # Assuming 'rows' is a comma-separated string

    seating_arrangement = {}
    for row in rows:
        seating_arrangement[row] = []

    for seat in seats:
        seating_arrangement[seat.row].append({
            'number': seat.seat_number,
            'status': 'available'  # Default status; update this based on bookings
        })

    if request.method == 'POST':
        showtime_id = request.POST.get('showtime_id')
        showtime = get_object_or_404(Showtime, id=showtime_id)
        movie = get_object_or_404(Movie, id=showtime.movie.id)
        
        # Get the current date and time for booking_date
        booking_date = timezone.now().date()
        
        # Safely handle selectedSeats
        selected_seats = request.POST.get('selectedSeats')
        if selected_seats is not None:
            selected_seats = selected_seats.split(',')
        else:
            selected_seats = []

        # Check for existing booking with the same user, movie, and booking_date
        existing_booking = Booking.objects.filter(
            user=request.user,
            movie=movie,
            booking_date=booking_date
        )
        
        if existing_booking:
            # Update the existing booking
            existing_booking.selected_seats = ','.join(selected_seats)
            existing_booking.status = 'Confirmed'  # Example default status
            existing_booking.showtime=showtime,
            existing_booking.theatre=theatre,
            existing_booking.save()
        else:
            # Create a new booking
            Booking.objects.create(
                user=request.user,
                movie=movie,
                showtime=showtime,
                theatre=theatre,
                selected_seats=','.join(selected_seats),
                status='Confirmed',  # Example default status
                booking_date=booking_date
            )
        
        return render(request, 'view_seating.html', {
        'theatre': theatre,
        'seating_arrangement': seating_arrangement
    })

    return render(request, 'view_seating.html', {
        'theatre': theatre,
        'seating_arrangement': seating_arrangement
    })


from django.shortcuts import render

def payment(request):
    # Implement your payment logic here
    return render(request, 'payment_page.html')




from django.shortcuts import render, redirect
from django.conf import settings
import razorpay
from .models import Booking
import requests
from requests.exceptions import ConnectionError as RequestsConnectionError
from django.http import HttpResponse

def confirm_booking(request):
    if request.method == 'POST':
        total_amount = int(request.POST.get('totalAmount'))  # Amount in INR
        selected_seats = request.POST.get('selectedSeats')
        movie_id = request.POST.get('movie_id')
        theatre_id = request.POST.get('theatre_id')
        showtime_id = request.POST.get('showtime_id')

        try:
            # Initialize Razorpay client
            client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

            # Create a Razorpay order
            order_data = {
                'amount': total_amount * 100,  # Amount in paise
                'currency': 'INR',
                'payment_capture': '1'
            }
            order = client.order.create(data=order_data)

            # Fetch the most recent booking for the user
            existing_bookings = Booking.objects.filter(user=request.user).order_by('-id')
            if existing_bookings.exists():
                existing_booking = existing_bookings.first()
                # Update existing booking
                existing_booking.selected_seats = selected_seats
                existing_booking.total_amount = total_amount
                existing_booking.save()
                booking_id = existing_booking.id
            else:
                # Create a new booking if not found
                new_booking = Booking.objects.create(
                    user=request.user,  # Assuming user is logged in
                    movie_id=movie_id,
                    theatre_id=theatre_id,
                    showtime_id=showtime_id,
                    selected_seats=selected_seats,
                    total_amount=total_amount
                )
                booking_id = new_booking.id

            # Prepare context for payment page
            context = {
                'totalAmount': total_amount,  # Amount in INR
                'api_key': settings.RAZORPAY_API_KEY,
                'order_id': order['id'],
                'selected_seats': selected_seats,
                'movie_id': movie_id,
                'theatre_id': theatre_id,
                'showtime_id': showtime_id,
                'booking_id': booking_id  # Pass booking_id to the template
            }
            return render(request, 'payment_page.html', context)
        
        except RequestsConnectionError as e:
            # Log the error or notify the user
            return HttpResponse(f"Error connecting to payment gateway: {e}", status=500)

    return redirect('/')








from django.shortcuts import render, get_object_or_404
from .models import Booking





from django.shortcuts import render, get_object_or_404
from .models import Booking
def booking_confirmation(request, booking_id):
    if request.method == 'POST':
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')

        try:
            # Fetch the booking instance
            booking = get_object_or_404(Booking, id=booking_id)

            # Check if a payment record already exists for this booking
            if Payment.objects.filter(booking=booking).exists():
                messages.warning(request, "This booking has already been paid for.")
                return redirect('booking_confirmation_view', booking_id=booking_id)

            # Create the Payment record
            payment = Payment.objects.create(
                user=request.user,
                booking=booking,
                amount=booking.total_amount,
                razorpay_order_id=razorpay_order_id,
                razorpay_payment_id=razorpay_payment_id,
                status='SUCCESS'  # Assuming the payment is successful
            )

            # Update the booking status
            booking.status = 'CONFIRMED'
            booking.save()

            messages.success(request, "Payment successful and booking confirmed!")
            return redirect('booking_confirmation_view', booking_id=booking_id)

        except Booking.DoesNotExist:
            messages.error(request, "Booking not found.")
            return redirect('/')

    return redirect('/')
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import Booking, Movie, Theatre, Showtime

def booking_confirmation_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    movie = get_object_or_404(Movie, id=booking.movie_id)
    theatre = get_object_or_404(Theatre, id=booking.theatre_id)
    showtime = get_object_or_404(Showtime, id=booking.showtime_id)
    
    # Adjust the field names based on your Showtime model
    showtime_date = showtime.date if hasattr(showtime, 'date') else 'Date not available'
    showtime_time = showtime.showtime if hasattr(showtime, 'showtime') else 'Time not available'
    
    subject = f"Booking Confirmation for {movie.title}"
    message = (
        f"Dear {request.user.username},\n\n"
        f"Your booking for the movie {movie.title} has been confirmed.\n\n"
        f"Details:\n"
        f"Movie: {movie.title}\n"
        f"Theatre: {theatre.name}\n"
        f"Showtime: {showtime_time} on {showtime_date}\n"
        f"Selected Seats: {booking.selected_seats}\n"
        f"Total Amount: ₹{booking.total_amount}\n"
        f"Status: {booking.status}\n"
        f"Payment: {booking.payment}\n\n"
        "Thank you for booking with us!\n"
        "Enjoy your movie!\n"
    )
    
    try:
      
        messages.success(request, 'Booking confirmation email sent successfully.')
    except Exception as e:
        messages.error(request, f"An error occurred while sending the email: {str(e)}")

    return render(request, 'booking_confirmation.html', {   
        'booking': booking,
        'movie': movie,
        'theatre': theatre,
        'showtime': showtime
    })
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import Booking, Movie, Theatre

def send_booking_confirmation_email(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    user_email = booking.user.email
    movie = booking.movie
    theatre = booking.theatre
    showtime = booking.showtime

    subject = f'Booking Confirmation - {movie.title}'
    message = f"""
    Dear {booking.user.name},

    Your booking for the movie "{movie.title}" has been successfully confirmed.

    Booking Details:
    Movie: {movie.title}
    Theatre: {theatre.name}
    Showtime: {showtime.strftime('%Y-%m-%d %H:%M')}
    Seats: {booking.seats}

    Thank you for choosing our service. We hope you enjoy the show!

    Regards,
    Your Cinema Team
    """

    from_email = 'ticketflix01@gmail.com'
    recipient_list = [user_email]

    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    except BadHeaderError:
        return HttpResponse("Invalid header found.")
    except Exception as e:
        return HttpResponse(f"An error occurred while sending the email: {str(e)}")

    return HttpResponse("Booking confirmation email has been sent successfully.")



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Booking

@login_required
def view_bookings(request):
    # Fetch bookings associated with the logged-in user
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'view_bookings.html', {'bookings': bookings})

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Booking

from django.shortcuts import render, get_object_or_404
from .models import Booking

def refund_processing(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'refund_processing.html', {'booking': booking})

@login_required
def cancel_booking(request, booking_id):
    # Fetch the specific booking and ensure it's associated with the logged-in user
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.status = 'Cancelled'
    booking.save()
    # Optionally, send a cancellation email
    # send_cancellation_email(request.user.email, booking)
    return redirect('view_bookings')



from django.shortcuts import render

def feedback_success(request):
    return render(request, 'feedback_success.html')

from django.shortcuts import render, redirect
from myapp.models import Feedback, Booking

def submit_feedback(request, booking_id):
    if request.method == "POST":
        feedback_text = request.POST.get('feedback')
        
        # Retrieve the booking instance using the booking_id
        booking = Booking.objects.get(id=booking_id)
        
        # Perform sentiment analysis
        sentiment = predict_sentiment(feedback_text)

        # Create a new Feedback object and save it to the database
        feedback = Feedback.objects.create(
            booking=booking,
            user=request.user,
            feedback_text=feedback_text,
            sentiment=sentiment
        )
        return render(request, 'feedback_thankyou.html', {'sentiment': sentiment})

def sentiment_analysis(request):
    feedbacks = Feedback.objects.all()
    analysis_results = []

    for feedback in feedbacks:
        # Ensure feedback has text
        if hasattr(feedback, 'feedback_text'):
            analysis = TextBlob(feedback.feedback_text)  # Use feedback.feedback_text
            sentiment = analysis.sentiment.polarity
            if sentiment > 0:
                sentiment_label = 'Positive'
            elif sentiment == 0:
                sentiment_label = 'Neutral'
            else:
                sentiment_label = 'Negative'
            analysis_results.append({
                'feedback': feedback.feedback_text,  # Use feedback.feedback_text
                'sentiment': sentiment_label
            })

    context = {
        'analysis_results': analysis_results
    }
    return render(request, 'admin/sentiment_analysis.html', context)
from django.shortcuts import render
from collections import Counter
from .models import Feedback  # Adjust the import based on your model location

def sentiment_analysis_view(request):
    # Fetch all feedback from the database
    feedbacks = Feedback.objects.all()

    # Count the occurrences of each sentiment
    sentiment_counts = Counter(feedback.sentiment for feedback in feedbacks)

    # Ensure all sentiment types are represented in the dictionary
    sentiments = ['Positive', 'Neutral', 'Negative']
    for sentiment in sentiments:
        if sentiment not in sentiment_counts:
            sentiment_counts[sentiment] = 0

    # Prepare the context
    context = {
        'analysis_results': feedbacks,
        'sentiment_counts': sentiment_counts
    }
    return render(request, 'admin/sentiment_analysis.html', context)
from django.shortcuts import render
from .models import Feedback
from textblob import TextBlob
from django.db.models import Count
from django.db.models.functions import TruncDay
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime

def sentiment_trend_view(request):
    # Analyze sentiment for all feedback
    feedbacks = Feedback.objects.all()
    for feedback in feedbacks:
        blob = TextBlob(feedback.feedback_text)
        sentiment = 'Positive' if blob.sentiment.polarity > 0.1 else 'Negative' if blob.sentiment.polarity < -0.1 else 'Neutral'
        feedback.sentiment = sentiment
        feedback.save()

    # Aggregate sentiment data by day
    daily_sentiment = feedbacks.annotate(date=TruncDay('created_at')).values('date', 'sentiment').annotate(count=Count('sentiment')).order_by('date')

    # Create a dictionary for storing counts per date
    sentiment_counts = {'Positive': {}, 'Neutral': {}, 'Negative': {}}
    dates = []

    # Initialize dictionaries for each date
    for entry in daily_sentiment:
        date_str = entry['date'].strftime('%Y-%m-%d')  # format date for consistency
        if date_str not in dates:
            dates.append(date_str)

        sentiment_type = entry['sentiment']
        sentiment_counts[sentiment_type][date_str] = entry['count']

    # Ensure all sentiment types have values for each date (fill missing with 0)
    positive_counts = [sentiment_counts['Positive'].get(date, 0) for date in dates]
    neutral_counts = [sentiment_counts['Neutral'].get(date, 0) for date in dates]
    negative_counts = [sentiment_counts['Negative'].get(date, 0) for date in dates]

    # Generate the plot
    plt.figure(figsize=(10, 6))
    plt.plot(dates, positive_counts, label='Positive', color='green')
    plt.plot(dates, neutral_counts, label='Neutral', color='grey')
    plt.plot(dates, negative_counts, label='Negative', color='red')
    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.title('Sentiment Trend Over Time')
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.grid(True)

    # Save plot to a PNG image
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    # Render the result
    context = {
        'plot_data': plot_data,
        'current_year': datetime.now().year,
    }

    return render(request, 'admin/sentiment_trend.html', context)


from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Booking

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = HttpResponse(content_type='application/pdf')
    pisa_status = pisa.CreatePDF(html, dest=result)
    if pisa_status.err:
        return HttpResponse('We had some errors with the PDF generation <pre>' + html + '</pre>')
    return result

def download_ticket_pdf(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    context = {
        'booking': booking,
        'movie': booking.movie,
        'theatre': booking.theatre,
        'showtime': booking.showtime,
        'selected_seats': booking.selected_seats,
        'total_amount': booking.total_amount,
        'status': booking.status,
        'payment': booking.payment,
    }
    return render_to_pdf('booking_ticket_pdf.html', context)



from django.shortcuts import render
from .models import Showtime, Theatre

def showtime_list(request):
    # Get all theatres for filtering
    theatres = Theatre.objects.all()

    # Get filter and sort parameters from the request
    selected_theatre = request.GET.get('theatre')
    sort_option = request.GET.get('sort', 'time')  # Default sort by time

    # Filter showtimes by selected theatre if provided
    showtimes = Showtime.objects.all()
    if selected_theatre:
        showtimes = showtimes.filter(theatre__id=selected_theatre)

    # Sort showtimes based on the selected option
    if sort_option == 'time':
        showtimes = showtimes.order_by('showtime')  # Earliest to latest
    elif sort_option == 'theatre':
        showtimes = showtimes.order_by('theatre__name')  # Sort by theatre name

    context = {
        'showtimes': showtimes,
        'theatres': theatres,
        'selected_theatre': selected_theatre,
        'sort_option': sort_option,
    }
    return render(request, 'showtime.html', context)

# views.py
from django.shortcuts import render, get_object_or_404
from .models import Theatre

def theatre_detail(request, theatre_id):
    theatre = get_object_or_404(Theatre, id=theatre_id)
    context = {
        'theatre': theatre,
    }
    return render(request, 'theatre_detail.html', context)


# views.py
from django.shortcuts import render
from .models import Theatre

def theatre(request):
    # Retrieve all theatres from the database
    theatres = Theatre.objects.all()
    
    # Pass the theatres to the template
    return render(request, 'theatre.html', {'theatres': theatres})


from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, Rating  # Ensure you import the Rating model
from django.contrib import messages

def rate_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == 'POST':
        score = request.POST.get('score')

        # Check if the user has already rated this movie
        existing_rating = Rating.objects.filter(user=request.user, movie=movie).first()
        if existing_rating:
            messages.warning(request, "You have already rated this movie. Your rating cannot be changed.")
        else:
            # Create a new rating
            Rating.objects.create(user=request.user, movie=movie, score=score)
            messages.success(request, "Thank you for your rating!")

        return redirect('movie_detail', movie_id=movie.id)  # Redirect to the movie detail page

    return redirect('movie_list')  # Redirect if not a POST request


# views.py
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    
    # Check if the user has rated this movie
    has_rated = Rating.objects.filter(user=request.user, movie=movie).exists()

    context = {
        'movie': movie,
        'user': {
            'has_rated': has_rated  # Pass the rating status to the template
        }
    }
    
    return render(request, 'movie_detail.html', context)


# views.py
import io
import qrcode
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.shortcuts import render
from .models import Ticket  # Assuming you have a Ticket model

def generate_ticket(request, ticket_id):
    # Fetch the ticket details from the database
    ticket = Ticket.objects.get(id=ticket_id)  # Replace with your ticket fetching logic

    # Create a QR code
    qr_data = f'Ticket ID: {ticket.id}, Movie: {ticket.movie.title}, User: {ticket.user.username}'
    qr = qrcode.make(qr_data)
    
    # Save the QR code to a BytesIO object
    qr_buffer = io.BytesIO()
    qr.save(qr_buffer, format='PNG')
    qr_buffer.seek(0)

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ticket_{ticket.id}.pdf"'

    # Create a PDF with ReportLab
    pdf_buffer = io.BytesIO()
    p = canvas.Canvas(pdf_buffer, pagesize=letter)
    width, height = letter

    # Add ticket details to the PDF
    p.drawString(100, height - 100, f'Ticket ID: {ticket.id}')
    p.drawString(100, height - 120, f'Movie: {ticket.movie.title}')
    p.drawString(100, height - 140, f'User: {ticket.user.username}')
    p.drawString(100, height - 160, f'Showtime: {ticket.showtime}')
    
    # Draw the QR code on the PDF
    p.drawImage(qr_buffer, 100, height - 250, width=100, height=100)  # Adjust size and position as needed

    p.showPage()
    p.save()

    # Get the PDF content
    pdf_buffer.seek(0)
    response.write(pdf_buffer.getvalue())
    return response

import io
import base64
import qrcode
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.shortcuts import render
from .models import Ticket  # Assuming you have a Ticket model

def generate_ticket_pdf(request, ticket_id):
    # Fetch the ticket details from the database
    ticket = Ticket.objects.get(id=ticket_id)  # Replace with your ticket fetching logic

    # Create a QR code
    qr_data = f'Ticket ID: {ticket.id}, Movie: {ticket.movie.title}, User: {ticket.user.username}'
    qr = qrcode.make(qr_data)

    # Save the QR code to a BytesIO object
    qr_buffer = io.BytesIO()
    qr.save(qr_buffer, format='PNG')
    qr_buffer.seek(0)

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ticket_{ticket.id}.pdf"'

    # Create a PDF with ReportLab
    pdf_buffer = io.BytesIO()
    p = canvas.Canvas(pdf_buffer, pagesize=letter)
    width, height = letter

    # Add ticket details to the PDF
    p.drawString(100, height - 100, f'Ticket ID: {ticket.id}')
    p.drawString(100, height - 120, f'Movie: {ticket.movie.title}')
    p.drawString(100, height - 140, f'User: {ticket.user.username}')
    p.drawString(100, height - 160, f'Showtime: {ticket.showtime}')

    # Draw the QR code on the PDF
    p.drawImage(qr_buffer, 100, height - 250, width=100, height=100)  # Adjust size and position as needed

    p.showPage()
    p.save()

    # Get the PDF content
    pdf_buffer.seek(0)
    response.write(pdf_buffer.getvalue())
    return response



# views.py
def validate_voucher(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        voucher_code = data.get('voucher_code')

        try:
            voucher = GiftVoucher.objects.get(code=voucher_code)

            if voucher.expiration_date < timezone.now().date():
                return JsonResponse({'success': False, 'message': 'Voucher has expired.'})

            # Log the voucher usage
            VoucherUsage.objects.create(voucher=voucher, user=request.user)

            return JsonResponse({'success': True, 'discount_value': voucher.discount_value})

        except GiftVoucher.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Invalid voucher code.'})

    return JsonResponse({'success': False, 'message': 'Invalid request.'})

# views.py
# views.py
from django.shortcuts import render, redirect
from .models import GiftVoucher
from django.contrib import messages
from django.utils import timezone

def create_voucher(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        discount_value = request.POST.get('discount_value')
        expiration_date = request.POST.get('expiration_date')

        # Convert expiration_date to a valid datetime object
        try:
            expiration_date = timezone.datetime.strptime(expiration_date, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Invalid date format.")
            return redirect('admin/create_voucher')  # Change this to your voucher form URL name

        # Save the voucher if the form is valid
        try:
            voucher = GiftVoucher.objects.create(
                code=code,
                discount_value=discount_value,
                expiration_date=expiration_date
            )
            messages.success(request, 'Voucher created successfully!')
        except Exception as e:
            messages.error(request, f"Error creating voucher: {e}")

        return redirect('voucher_success')  # Redirect to prevent resubmission

    return render(request, 'admin/create_voucher.html')
# views.py
from django.shortcuts import render

def voucher_success(request):
    return render(request, 'admin/voucher_success.html')



# views.py
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from .models import Booking

@login_required
def invite_friends(request, booking_id):
    if request.method == 'POST':
        friend_emails = request.POST.get('friend_emails')
        booking = get_object_or_404(Booking, id=booking_id)

        # Split the emails and clean them
        emails = [email.strip() for email in friend_emails.split(',') if email.strip()]

        # Prepare the email content
        subject = f"Join me for {booking.movie.title} at {booking.theatre.name}"
        message = (
            f"Hi there!\n\n"
            f"I just booked tickets for {booking.movie.title} at {booking.theatre.name}.\n"
            f"Showtime: {booking.showtime.showtime|date:'h:i A'} on {booking.showtime.date}\n"
            f"Selected Seats: {booking.selected_seats}\n\n"
            f"I would love for you to join me!\n\n"
            f"Best,\n"
            f"{request.user.username}"
        )

        # Send emails
        for email in emails:
            try:
                send_mail(subject, message, 'ticketflix01.com', [email])
            except Exception as e:
                messages.error(request, f"An error occurred while sending the invite to {email}: {str(e)}")
                continue

        messages.success(request, "Invitations sent successfully!")
        return redirect('booking_confirmation_view', booking_id=booking_id)

    return redirect('user_dashboard')  # Redirect if not a POST request


# views.py
# views.py
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages

def send_notification(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        message_type = request.POST.get('message_type')

        # Logic to determine recipients based on message_type
        if message_type == 'all':
            recipients = ['sonusebastian751@gmail.com', 'btansya@gmail.com']  # Add all user emails
        elif message_type == 'theatre_owner':
            recipients = ['theatre_owner@example.com']  # Add theatre owner emails
        elif message_type == 'admin':
            recipients = ['admin@example.com']  # Add admin emails

        # Send email
        send_mail(
            'System Notification',  # Subject
            message,  # Message
            settings.EMAIL_HOST_USER,  # From email
            recipients,  # To email list
            fail_silently=False,  # Raise an error if sending fails
        )

        messages.success(request, "Notification sent successfully!")
        return redirect('view_notifications')  # Redirect to the notifications page

    return render(request, 'admin/send_notification.html')



# views.py
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def view_notifications(request):
    user_type = 'all'  # Default to all users
    if request.user.is_staff:
        user_type = 'admin'
    elif hasattr(request.user, 'theatreowner'):
        user_type = 'theatre_owner'

    notifications = Notification.objects.filter(message_type__in=['all', user_type]).order_by('-created_at')

    return render(request, 'notifications/view_notifications.html', {'notifications': notifications})

# views.py


# views.py

# myapp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Booking, Movie  # Ensure Movie is imported
from django.contrib import messages
import calendar
   # myapp/views.py
def generate_report(request):
       # Get the selected month and year from the form
       month = request.GET.get('month', None)
       year = request.GET.get('year', None)

       # Fetch the relevant booking data based on the selected month and year
       filtered_bookings = []
       if month and year:
           month_number = str(list(calendar.month_name).index(month)).zfill(2)  # Convert month to '01', '02', etc.
           
           # Query the database for bookings in the selected month and year using 'booking_date'
           filtered_bookings = Booking.objects.filter(
               booking_date__year=year,
               booking_date__month=month_number
           ).select_related('user', 'movie')  # Use select_related to fetch related user and movie data

           # Filter out bookings with no user
           filtered_bookings = [booking for booking in filtered_bookings if booking.user is not None]

       # Check if the user wants to generate a PDF
       if request.GET.get('generate_pdf', None):
           return generate_pdf_report(filtered_bookings, month, year)

       # Prepare context for rendering the HTML template
       months = list(calendar.month_name)[1:]  # List of month names (January to December)
       context = {
           'months': months,
           'month': month,
           'year': year,
           'bookings': filtered_bookings,
       }
       return render(request, 'admin/generate_report.html', context)
# myapp/views.py
def generate_pdf_report(bookings, month, year):
    # Step 5: Create the HTTP response for the PDF file
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="report_{month}_{year}.pdf"'

    # Step 6: Create a PDF with ReportLab
    pdf = canvas.Canvas(response, pagesize=letter)
    pdf.setTitle(f"Monthly Booking Report - {month} {year}")

    # PDF Title
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, 750, f"Monthly Booking Report for {month} {year}")
    
    # PDF Table Headers
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, 720, "User")
    pdf.drawString(200, 720, "Movie")
    pdf.drawString(350, 720, "Date")
    pdf.drawString(450, 720, "Amount")

    # PDF Table Content
    y = 700  # Starting y position for the first row
    pdf.setFont("Helvetica", 10)
    
    if not bookings:
        pdf.drawString(50, y, "No bookings available for this period.")
    else:
        for booking in bookings:
            if booking.user:  # Check if user is not None
                pdf.drawString(50, y, str(booking.user.username))  # Display username
            else:
                pdf.drawString(50, y, "Unknown User")  # Handle case where user is None
            
            pdf.drawString(200, y, str(booking.movie.title))  # Display movie title
            
            # Add spacing for the date
            pdf.drawString(350, y, str(booking.booking_date))  # Display date
            
            # Add spacing for the amount
            total_amount = booking.total_amount if booking.total_amount is not None else 0  # Default to 0 if None
            pdf.drawString(450, y, f"${float(total_amount):.2f}")  # Display amount
            
            y -= 30  # Increase vertical spacing for the next row (from 20 to 30)
            if y < 100:  # Prevent content from going off the page
                pdf.showPage()
                y = 750  # Reset y position for new page

    # Finish up and save the PDF
    pdf.showPage()
    pdf.save()

    return response




from django.shortcuts import render, redirect
from django.conf import settings
import razorpay
from .models import Booking
import requests
from requests.exceptions import ConnectionError as RequestsConnectionError
from django.http import HttpResponse

def confirm_booking(request):
    if request.method == 'POST':
        total_amount = int(request.POST.get('totalAmount'))  # Amount in INR
        selected_seats = request.POST.get('selectedSeats')
        movie_id = request.POST.get('movie_id')
        theatre_id = request.POST.get('theatre_id')
        showtime_id = request.POST.get('showtime_id')

        try:
            # Initialize Razorpay client
            client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

            # Create a Razorpay order
            order_data = {
                'amount': total_amount * 100,  # Amount in paise
                'currency': 'INR',
                'payment_capture': '1'
            }
            order = client.order.create(data=order_data)

            # Fetch the most recent booking for the user
            existing_bookings = Booking.objects.filter(user=request.user).order_by('-id')
            if existing_bookings.exists():
                existing_booking = existing_bookings.first()
                # Update existing booking
                existing_booking.selected_seats = selected_seats
                existing_booking.total_amount = total_amount
                existing_booking.save()
                booking_id = existing_booking.id
            else:
                # Create a new booking if not found
                new_booking = Booking.objects.create(
                    user=request.user,  # Assuming user is logged in
                    movie_id=movie_id,
                    theatre_id=theatre_id,
                    showtime_id=showtime_id,
                    selected_seats=selected_seats,
                    total_amount=total_amount
                )
                booking_id = new_booking.id

            # Prepare context for payment page
            context = {
                'totalAmount': total_amount,  # Amount in INR
                'api_key': settings.RAZORPAY_API_KEY,
                'order_id': order['id'],
                'selected_seats': selected_seats,
                'movie_id': movie_id,
                'theatre_id': theatre_id,
                'showtime_id': showtime_id,
                'booking_id': booking_id  # Pass booking_id to the template
            }
            return render(request, 'payment_page.html', context)
        
        except RequestsConnectionError as e:
            # Log the error or notify the user
            return HttpResponse(f"Error connecting to payment gateway: {e}", status=500)

    return redirect('/')

 # Example for GET request
# views.py
from django.shortcuts import render
from .models import Movie
from django.utils import timezone

def upcoming_movies(request):
    # Get today's date
    today = timezone.now().date()
    # Fetch upcoming movies
    upcoming_movies = Movie.objects.filter(release_date__gt=today).order_by('release_date')

    context = {
        'upcoming_movies': upcoming_movies
    }
    return render(request, 'admin/upcoming_movies.html', context)
# myapp/views.py
from datetime import timedelta
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Movie, Category

def add_upcoming_movie(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        category_id = request.POST.get('category')
        release_date = request.POST.get('release_date')
        description = request.POST.get('description')
        poster_image = request.FILES.get('poster')
        director = request.POST.get('director')
        duration_str = request.POST.get('duration')  # This should be in HH:MM format
        price_str = request.POST.get('price')

        try:
            # Check if title already exists
            if Movie.objects.filter(title=title).exists():
                messages.error(request, "A movie with this title already exists.")
                return render(request, 'admin/add_upcoming_movie.html', {
                    'categories': Category.objects.all(),
                })

            # Validate and convert the price
            if not price_str or float(price_str) <= 0:
                raise ValueError("Price must be a positive number greater than zero")
            price = float(price_str)

            # Handle the file upload
            if not poster_image:
                raise ValueError("No poster image uploaded")

            # Convert duration from string to timedelta
            if duration_str:
                hours, minutes = map(int, duration_str.split(':'))
                duration = timedelta(hours=hours, minutes=minutes)
            else:
                raise ValueError("Duration must be provided in HH:MM format")

            # Create the movie object
            Movie.objects.create(
                title=title,
                category_id=category_id,
                release_date=release_date,
                description=description,
                poster=poster_image,
                director=director,
                duration=duration,  # Now this is a timedelta object
                price=price,
            )

            messages.success(request, "Upcoming movie added successfully!")  # Success message
            return redirect('upcoming_movies')  # Redirect to the upcoming movies page after adding

        except ValueError as e:
            messages.error(request, str(e))
            return render(request, 'admin/add_upcoming_movie.html', {
                'categories': Category.objects.all(),
            })

    categories = Category.objects.all()
    return render(request, 'admin/add_upcoming_movie.html', {'categories': categories})  # Render the form


# myapp/views.py
from django.shortcuts import render
from .models import Movie
import datetime

def list_upcoming_movies(request):
    # Get today's date
    today = datetime.date.today()
    # Filter movies that are scheduled to be released in the future
    upcoming_movies = Movie.objects.filter(release_date__gt=today).order_by('release_date')
    
    return render(request, 'admin/list_upcoming_movies.html', {'upcoming_movies': upcoming_movies})
from django.shortcuts import render
def chatbot_view(request):
    response = ""
    if request.method == 'POST':
        user_message = request.POST.get('message', '')

        # In a real implementation, you could process the message using NLP here
        
        # Basic response that acknowledges the question
        response = f"You asked: '{user_message}'. We're working on an answer, please contact support for complex inquiries."

    return render(request, 'chatbot.html', {'response': response})

# myapp/views.py
from django.shortcuts import render
from .models import VoucherUsage  # Ensure you import the VoucherUsage model

def voucher_usage_report(request):
    usages = VoucherUsage.objects.select_related('voucher', 'user').all()
    return render(request, 'admin/voucher_usage_report.html', {'usages': usages})



# views.py
from django.shortcuts import render
from .models import Movie
from django.utils import timezone

def user_upcoming_movies(request):
    # Get today's date
    today = timezone.now().date()
    # Fetch upcoming movies
    upcoming_movies = Movie.objects.filter(release_date__gt=today).order_by('release_date')

    context = {
        'upcoming_movies': upcoming_movies
    }
    return render(request, 'user_upcoming_movies.html', context)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Movie, Category
from datetime import timedelta

def edit_upcoming_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    categories = Category.objects.all()  # Fetch all categories

    if request.method == 'POST':
        # Update movie fields directly from the request
        movie.title = request.POST.get('title', movie.title)
        movie.category_id = request.POST.get('category', movie.category_id)  # Assuming category is a ForeignKey
        movie.release_date = request.POST.get('release_date', movie.release_date)
        movie.description = request.POST.get('description', movie.description)
        movie.director = request.POST.get('director', movie.director)

        # Handle duration conversion
        duration_str = request.POST.get('duration', movie.duration)
        if duration_str:
            try:
                hours, minutes = map(int, duration_str.split(':'))
                movie.duration = timedelta(hours=hours, minutes=minutes)
            except ValueError:
                messages.error(request, "Duration must be in HH:MM format.")
                return render(request, 'admin/edit_upcoming_movies.html', {'movie': movie, 'categories': categories})

        movie.price = request.POST.get('price', movie.price)

        # Handle file upload for the poster
        if request.FILES.get('poster'):
            movie.poster = request.FILES['poster']

        movie.save()  # Save the updated movie instance
        messages.success(request, "Movie updated successfully.")  # Success message
        return redirect('admin_upcoming_movies')  # Redirect to the upcoming movies list

    return render(request, 'admin/edit_upcoming_movies.html', {'movie': movie, 'categories': categories})



from django.shortcuts import render, redirect
from .models import Auditorium

def list_auditoriums(request):
    auditoriums = Auditorium.objects.all()  # Fetch all auditoriums
    return render(request, 'theatre_owner/list_auditoriums.html', {'auditoriums': auditoriums})

# myapp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Auditorium, Theatre  # Ensure Theatre is imported
from django.contrib import messages
# myapp/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Auditorium, Theatre  # Ensure Theatre is imported

def add_auditorium(request):
    if request.method == 'POST':
        theatre_id = request.POST.get('theatre')  # Get theatre ID from POST data
        name = request.POST.get('name')  # Get auditorium name from POST data
        capacity = request.POST.get('capacity')  # Get capacity from POST data
        
        # Validate that theatre_id is provided
        if not theatre_id:
            messages.error(request, "Theatre ID is required.")
            return render(request, 'theatre_owner/add_auditorium.html')

        # Create and save the new auditorium
        try:
            Auditorium.objects.create(theatre_id=theatre_id, name=name, capacity=capacity)
            messages.success(request, "Auditorium added successfully.")
            return redirect('list_auditoriums')  # Redirect to the list view
        except Exception as e:
            messages.error(request, f"Error adding auditorium: {str(e)}")
            return render(request, 'theatre_owner/add_auditorium.html')

    theatres = Theatre.objects.all()  # Fetch all theatres to display in the form
    return render(request, 'theatre_owner/add_auditorium.html', {'theatres': theatres})  # Render the add auditorium form
# myapp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Wishlist

def add_to_wishlist(request, movie_id):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, id=movie_id)
        Wishlist.objects.get_or_create(user=request.user, movie=movie)
        return redirect('user_dashboard')  # Redirect to the user dashboard or wherever appropriate
    return redirect('login')  # Redirect to login if not authenticated

def remove_from_wishlist(request, movie_id):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, id=movie_id)
        Wishlist.objects.filter(user=request.user, movie=movie).delete()
        return redirect('user_dashboard')  # Redirect to the user dashboard or wherever appropriate
    return redirect('login')  # Redirect to login if not authenticated

def user_dashboard(request):
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user)
        return render(request, 'user_dashboard.html', {'wishlist_items': wishlist_items})
    return redirect('login')  # Redirect to login if not authenticated

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Movie, Wishlist


def user_wishlist(request):
    """View to display the user's wishlist."""
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'user_wishlist.html', {'wishlist_items': wishlist_items})


# myapp/views.py
from django.shortcuts import render
from django.utils import timezone

def booking_report_form(request):
    """View to display the booking report form."""
    today = timezone.now()  # Get today's date
    return render(request, 'theatre_owner/booking_report_form.html', {
        'today': today,
    })