from django.urls import path
from .views import *







urlpatterns = [

    #1
    path('signup/', SignupView.as_view(), name='signup'),

    #2
    path('login/', LoginView.as_view(), name='login'),

    #3
    path('admin/login/', AdminLoginView.as_view(), name='admin-login'),

    #4
    path('organizer/login/', OrganizerLoginView.as_view(), name='organizer-login'),

    #5
    path('organizer/signup/', OrganizerSignupView.as_view(), name='organizer-signup'),

    #6
    path('event/<int:event_id>/', EventDetailView.as_view(), name='event-detail'),

    #7
    path('events/filtered/', FilteredEventView.as_view(), name='filtered-events'),

    #8
    path('events/organizer/<int:organizer_id>/', EventsByOrganizerView.as_view(), name='events-by-organizer'),

    #9
    path('organizers/admin/<int:staff_id>/', OrganizersByAdminView.as_view(), name='organizers-by-admin'),

    #10
    path('organizer/<int:organizer_id>/average-rating/', OrganizerAverageRatingView.as_view(), name='organizer-average-rating'), 

    #11
    path('organizer/<int:organizer_id>/complaints/', ComplaintCountView.as_view(), name='organizer-complaints'),  

    #12 
    path('user/<int:id>/', UserDetailView.as_view(), name='user-detail'),

    #13
    path('admin/<int:id>/', AdminDetailView.as_view(), name='admin-detail'),

    #14
    path('organizer/<int:id>/', OrganizerDetailView.as_view(), name='organizer-detail'),

    #15
    path('admin/unverified-organizers/', UnverifiedOrganizerListView.as_view(), name='unverified-organizers'),

    #16 
    path('organizer/<int:organizer_id>/feedbacks/', OrganizerEventFeedbackView.as_view(), name='organizer-feedbacks'),

    #17 
    path('user/<int:user_id>/registrations/', UserRegistrationTransactionView.as_view(), name='user-registrations'),

    #18
    path('user/<int:user_id>/events/', UserEventListView.as_view(), name='user-events'),

    #19
    path('complaint/<int:complaint_id>/', ComplaintDetailView.as_view(), name='complaint-detail'),

    #20
    path('feedback/<int:feedback_id>/', FeedbackDetailView.as_view(), name='feedback-detail'),  

    #21 
    path('transaction/<int:transaction_id>/', TransactionDetailView.as_view(), name='transaction-detail'),

    #22
    path('api/registration/<int:registration_id>/', RegistrationDetailView.as_view(), name='registration-detail'),

    #23
    path('create-event/<int:organizer_id>/', CreateEventView.as_view(), name='create-event'),
     
    #24
    path('verify-organizer/<int:staff_id>/<int:organizer_id>/', VerifyOrganizerView.as_view(), name='verify-organizer'), 

    #25 
    path('feedback/<int:user_id>/<int:event_id>/', SubmitFeedbackView.as_view(), name='submit-feedback'), 

    #26
    path('complaints/create/', ComplaintCreateView.as_view(), name='create-complaint'), 

    #27
    path('register-event/', CreateTransactionRegistrationView.as_view(), name='register-event'), 
    
    #28
    path('event/<int:event_id>/revenue/', EventRevenueAPIView.as_view(), name='event-revenue'), 

    #29
    path('user/<int:user_id>/transactions/', UserTransactionHistoryView.as_view(), name='user-transactions'),

    #30
    path('user/<int:user_id>/complaints/', UserComplaintHistoryView.as_view(), name='user-complaints'),

    #31
    path('event/<int:event_id>/revenue/', EventRevenueAPIView.as_view(), name='event-revenue'), 

    #32
    path('users/<int:user_id>/update/', UpdateUserView.as_view(), name='update-user'), 

    #33 
    path('organizer/update/<int:organizer_id>/', UpdateOrganizerView.as_view(), name='update-organizer'), 

    #34
    path('events/<int:event_id>/update/', UpdateEventView.as_view(), name='update-event'), 

     #35
    path('event/<int:event_id>/registrations/', EventRegistrationView.as_view(), name='event-registrations'), 

    #36
    path('organizer/<int:organiser_id>/event-stats/', OrganizerEventStatsView.as_view(), name='organizer-event-stats'),

    #37
    path('event/<int:event_id>/rating/', EventRatingView.as_view(), name='event-average-rating'),

    #38
    path('admin/<int:admin_id>/organizer-complaints/', ComplaintsUnderAdminView.as_view(), name='admin-organizer-complaints'),







    
]
