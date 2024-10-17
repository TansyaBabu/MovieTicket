from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import add_theatre, edit_theatre, delete_theatre
from .views import activate_user, deactivate_user,remove_user

from .views import add_movie, check_title_exists
from .views import update_theatre_owner_profile
# Correct import
from myapp.models import UserProfile
from .views import send_otp, verify_otp
from .views import confirm_booking,booking_confirmation
from .views import send_confirmation_email

from .views import admin_theatre_list


from .views import confirm_booking
from .views import create_order

from .views import view_bookings, cancel_booking

from .views import submit_feedback, feedback_success 
from .views import analyze_feedback,sentiment_analysis_view
from .views import sentiment_trend_view

from .views import download_ticket_pdf
from .views import theatre_detail, theatre
from .views import rate_movie,movie_detail
from .views import generate_ticket
from .views import generate_report
from .views import validate_voucher
from .views import create_voucher
from .views import weekly_booking_report
from .views import invite_friends
from .views import send_notification, view_notifications
from .views import add_auditorium
from .views import upcoming_movies
from .views import add_upcoming_movie 
from .views import voucher_usage_report
from .views import list_upcoming_movies
from .views import user_upcoming_movies
from .views import edit_upcoming_movie
from .views import user_dashboard, add_to_wishlist, remove_from_wishlist, user_wishlist
from .views import booking_report_form
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'), 

    path('contact/', views.contact, name='contact'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
  
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'), 
    path('user_profile/', views.user_profile, name='user_profile'), 
     path('update_profile/', views.update_profile, name='update_profile'), 
    path('view_customers/', views.view_customers, name='view_customers'),
    path('categories/', views.list_categories, name='list_categories'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<int:pk>/', views.edit_category, name='edit_category'),
   path('categories/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    path('add_movie/', views.add_movie, name='add_movie'),
    path('edit_movie/<int:movie_id>/', views.edit_movie, name='edit_movie'),
    path('delete_movie/<int:pk>/', views.delete_movie, name='delete_movie'),
    path('list_movies/', views.list_movies, name='list_movies'),
 
    path('movies/<str:category>/', views.movie_category, name='movie_category'),
  
   
    path('theatre_owner_dashboard/', views.theatre_owner_dashboard, name='theatre_owner_dashboard'),
 
    path('theatre_owner_profile/', views.theatre_owner_profile, name='theatre_owner_profile'),
    # URL pattern for updating profile
    path('update_theatre_owner_profile/', views.update_theatre_owner_profile, name='update_theatre_owner_profile'),





    path('add_theatre/', add_theatre, name='add_theatre'),
    path('edit_theatre/<int:theatre_id>/', edit_theatre, name='edit_theatre'),
    path('delete_theatre/<int:theatre_id>/', delete_theatre, name='delete_theatre'),
  path('theatres/', views.list_theatres, name='list_theatres'),

     path('showtimes/add/', views.add_showtime, name='add_showtime'),
 path('showtimes/edit/<int:pk>/', views.edit_showtime, name='edit_showtime'),

path('showtimes/delete/<int:pk>/', views.delete_showtime, name='delete_showtime'),
      path('showtime-list/', views.showtime_list, name='showtime_list'),
  path('movies/<int:movie_id>/showtimes/', views.movie_showtimes, name='movie_showtimes'),
  path('add_seating/<int:theatre_id>/', views.add_seating, name='add_seating'),
    path('edit_seating/<int:seating_id>/', views.edit_seating, name='edit_seating'),
    path('delete_seating/<int:seating_id>/', views.delete_seating, name='delete_seating'),
    path('view_seating/<int:theatre_id>/', views.view_seating, name='view_seating'),
      path('view_showtimes/', views.view_showtimes, name='view_showtimes'),


      path('payment/', views.payment, name='payment'),
       path('process_payment/', views.process_payment, name='process_payment'), 
    path('activate_user/<int:user_id>/', views.activate_user, name='activate_user'),
    path('deactivate_user/<int:user_id>/', views.deactivate_user, name='deactivate_user'),
      path('check_title_exists/', check_title_exists, name='check_title_exists'),

      path('logout/', views.logout_view, name='logout'),


   
     path('remove_user/<int:user_id>/', views.remove_user, name='remove_user'),
 
         path('confirm_booking/', confirm_booking, name='confirm_booking'),
    
    
  path('admin_theatre_list/', admin_theatre_list, name='admin_theatre_list'),


  path('payment/', views.payment, name='payment'),


    path('booking_confirmation/<int:booking_id>/', booking_confirmation, name='booking_confirmation'),



    path('booking_confirmation_view/<int:booking_id>/', views.booking_confirmation_view, name='booking_confirmation_view'),
    
      path('view_bookings/', view_bookings, name='view_bookings'),
    path('cancel_booking/<int:booking_id>/', cancel_booking, name='cancel_booking'),
    
       path('submit-feedback/<int:booking_id>/', views.submit_feedback, name='submit_feedback'),
      
   
          path('feedback_success/', views.feedback_success, name='feedback_success'),
           path('sentiment_analysis/', views.sentiment_analysis_view, name='sentiment_analysis'),
             path('sentiment-trend/', sentiment_trend_view, name='sentiment_trend'),
         
           path('download_ticket_pdf/<int:booking_id>/', download_ticket_pdf, name='download_ticket_pdf'),
           path('showtime/', views.showtime_list, name='showtime'),
           
            path('theatre/', theatre_list, name='theatre'),
    path('theatre/<int:theatre_id>/', theatre_detail, name='theatre_detail'),
    
     path('movie/<int:movie_id>/rate/', views.rate_movie, name='rate_movie'),
       path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),  
        path('ticket/<int:ticket_id>/', generate_ticket, name='generate_ticket'),
   path('refund-processing/<int:booking_id>/', views.refund_processing, name='refund_processing'),
  path('generate_report/', views.generate_report, name='generate_report'),
   path('validate-voucher/', views.validate_voucher, name='validate_voucher'),
     path('create_voucher/', views.create_voucher, name='create_voucher'),

      path('invite-friends/<int:booking_id>/', views.invite_friends, name='invite_friends'),
       path('send_notification/', views.send_notification, name='send_notification'),
    path('notifications/', views.view_notifications, name='view_notifications'),

    path('voucher_success/', views.voucher_success, name='voucher_success'),
     path('upcoming_movies/', views.upcoming_movies, name='upcoming_movies'),
      path('add_upcoming_movie/', views.add_upcoming_movie, name='add_upcoming_movie'),
       path('chatbot/', views.chatbot_view, name='chatbot'),
        path('voucher_usage/', views.voucher_usage_report, name='voucher_usage_report'),
         path('upcoming_movies/', views.list_upcoming_movies, name='list_upcoming_movies'),
         
  path('user_upcoming_movies/', views.user_upcoming_movies, name='user_upcoming_movies'),
  path('upcoming-movies/edit/<int:movie_id>/', views.edit_upcoming_movie, name='edit_upcoming_movie'),
   path('auditoriums/', views.list_auditoriums, name='list_auditoriums'),
    path('add_auditorium/', views.add_auditorium, name='add_auditorium'),
     path('wishlist/', views.user_wishlist, name='user_wishlist'),  # View wishlist
    path('wishlist/add/<int:movie_id>/', views.add_to_wishlist, name='add_to_wishlist'),  # Add movie to wishlist
    path('wishlist/remove/<int:movie_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
      # Example view# Remove movie from wishlist
    # Other URL patterns...
]

  


       

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
