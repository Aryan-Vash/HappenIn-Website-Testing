from django.shortcuts import render

from rest_framework.views import *

from .models import *

from rest_framework.response import *

from rest_framework import *

from .serializers import *

from django.db.models import Avg, F, Q

from django.utils import timezone 

from django.utils.timezone import now

from django.shortcuts import get_object_or_404

from datetime import datetime,date

from rest_framework.generics import ListAPIView, RetrieveAPIView

from django.http import JsonResponse

from django.db import transaction














#1
class SignupView(APIView):
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "uid": user.id,
                "username": user.username
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


#2
class LoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            try:
                user = User.objects.get(username=username)
                if user.password == password:
                    return Response({
                        "uid": user.id,
                        "username": user.username
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Invalid password"}, status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


    
#3
class AdminLoginView(APIView):
    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['emailID']
            password = serializer.validated_data['password']

            try:
                admin = Admin.objects.get(emailID=email)
                if admin.password == password:
                    return Response({
                        "id": admin.id,
                        "emailID": admin.emailID,
                        "role": admin.role
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Invalid password."}, status=status.HTTP_401_UNAUTHORIZED)

            except Admin.DoesNotExist:
                return Response({"error": "Admin not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


    
#4
class OrganizerLoginView(APIView):
    def post(self, request):
        serializer = OrganizerLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


    
#5
class OrganizerSignupView(APIView):
    def post(self, request):
        serializer = OrganizerSignupSerializer(data=request.data)
        if serializer.is_valid():
            organizer = serializer.save()
            return Response({
                "id": organizer.id,
                "username": organizer.username
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



#6
class EventDetailView(APIView):
    def get(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = EventDetailSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)
    




#7
class FilteredEventView(APIView):
    def get(self, request):
        current_datetime = now().astimezone()
        current_date = current_datetime.date()
        current_time = current_datetime.time()

        # Mapping of shortform to matching category strings
        category_map = {
            'ea': ['Concert', 'Dance', 'Art'],
            'bt': ['Business', 'Tech'],
            'fl': ['Food', 'Expo'],
            'si': ['Charity'],
            'sf': ['Sports', 'Gaming']
        }

        # Get and normalize the filter param to lowercase
        filter_key = request.query_params.get('filter', '').lower()
        categories = category_map.get(filter_key, None)

        # Base query: upcoming events that are not full
        query = Event.objects.filter(
            Q(startDate__gt=current_date) |
            Q(startDate=current_date, startTime__gt=current_time)
        ).exclude(
            ticketsSold=F('maxAttendees')
        )

        # If a valid filter is provided, filter by category
        if categories:
            query = query.filter(category__in=categories)

        serializer = EventSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    





#8
class EventsByOrganizerView(APIView):
    def get(self, request, organizer_id):
        current_datetime = now().astimezone()
        current_date = current_datetime.date()
        current_time = current_datetime.time()

        # Base query
        events = Event.objects.filter(organizer__id=organizer_id)

        # Optional filter: 0 = upcoming, 1 = past
        filter_value = request.query_params.get('filter', None)

        if filter_value == '0':
            # Upcoming: date is in future or today with time > now
            events = events.filter(
                Q(startDate__gt=current_date) |
                Q(startDate=current_date, startTime__gt=current_time)
            )
        elif filter_value == '1':
            # Past: date is in past or today with time < now
            events = events.filter(
                Q(startDate__lt=current_date) |
                Q(startDate=current_date, startTime__lt=current_time)
            )

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)






#9
class OrganizersByAdminView(APIView):
    def get(self, request, staff_id):
        organizers = Organizer.objects.filter(staff__id=staff_id)
        
        if not organizers.exists():
            return Response({"message": "No organizers found for this admin."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = OrganizerListSerializer(organizers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)






#10
class OrganizerAverageRatingView(APIView):
    def get(self, request, organizer_id):
        organizer = Organizer.objects.filter(id=organizer_id).first()

        if not organizer:
            return Response({"error": "Organizer not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get all event IDs organized by this organizer
        events = Event.objects.filter(organizer_id=organizer_id).values_list('id', flat=True)

        # Calculate average rating from Feedback linked to these events
        avg_rating = Feedback.objects.filter(event_id__in=events).aggregate(avg=Avg('Rating'))['avg']

        serializer = OrganizerAvgRatingSerializer({
            'organizerID': organizer.id,
            'firstName': organizer.firstName,
            'lastName': organizer.lastName,
            'avgRating': round(avg_rating, 2) if avg_rating is not None else 0.0
        })

        return Response(serializer.data, status=status.HTTP_200_OK)
    




#11
class ComplaintCountView(APIView):
    def get(self, request, organizer_id):
        event_id = request.query_params.get('event_id', None)

        if event_id:
            complaints = Complaint.objects.filter(event__id=event_id, event__organizer__id=organizer_id)
            count = complaints.count()
            data = {
                'organizer_id': organizer_id,
                'event_id': int(event_id),
                'complaints': count
            }
        else:
            complaints = Complaint.objects.filter(event__organizer__id=organizer_id)
            count = complaints.count()
            data = {
                'organizer_id': organizer_id,
                'complaints': count
            }

        serializer = ComplaintCountSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


#11
class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    lookup_field = 'id'



#12
class AdminDetailView(RetrieveAPIView):
    queryset = Admin.objects.all()
    serializer_class = AdminDetailSerializer
    lookup_field = 'id'




#13
class OrganizerDetailView(RetrieveAPIView):
    queryset = Organizer.objects.all()
    serializer_class = OrganizerDetailSerializer
    lookup_field = 'id'



#14
class UnverifiedOrganizerListView(ListAPIView):
    queryset = Organizer.objects.filter(verificationStatus=False)
    serializer_class = UnverifiedOrganizerSerializer

   



#15
class OrganizerEventFeedbackView(APIView):
    def get(self, request, organizer_id):
        event_id = request.query_params.get('event_id')

        if event_id:
            # Feedback for specific event
            event = get_object_or_404(Event, id=event_id, organizer__id=organizer_id)
            feedbacks = Feedback.objects.filter(event=event)
        else:
            # Feedback for all events by organizer
            events = Event.objects.filter(organizer__id=organizer_id)
            feedbacks = Feedback.objects.filter(event__in=events)
        
        serializer = FeedbackSerializer(feedbacks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    



#16
class UserRegistrationTransactionView(APIView):
    def get(self, request, user_id):
        registrations = Registration.objects.filter(user__id=user_id)
        serializer = UserRegistrationSerializer(registrations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




#17
class UserEventListView(APIView):
    def get(self, request, user_id):
        filter_type = request.query_params.get('filter')  # "1" or "2"
        now = datetime.now().date()

        event_ids = Registration.objects.filter(user__id=user_id, event__isnull=False).values_list('event__id', flat=True)
        events = Event.objects.filter(id__in=event_ids)

        if filter_type == '1':
            events = events.filter(startDate__gte=now)
        elif filter_type == '2':
            events = events.filter(endDate__lt=now)

        serializer = EventBasicSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


#18
class ComplaintDetailView(APIView):
    def get(self, request, complaint_id):
        try:
            complaint = Complaint.objects.get(id=complaint_id)
            serializer = ComplaintDetailSerializer(complaint)
            return Response(serializer.data)
        except Complaint.DoesNotExist:
            return Response({'error': 'Complaint not found'}, status=status.HTTP_404_NOT_FOUND)
        


        
#19
class FeedbackDetailView(APIView):
    def get(self, request, feedback_id):
        try:
            feedback = Feedback.objects.get(id=feedback_id)
            serializer = FeedbackDetailSerializer(feedback)
            return Response(serializer.data)
        except Feedback.DoesNotExist:
            return Response({'error': 'Feedback not found'}, status=status.HTTP_404_NOT_FOUND)
        


        
#20
class TransactionDetailView(APIView):
    def get(self, request, transaction_id):
        try:
            transaction = Transaction.objects.get(id=transaction_id)
            serializer = TransactionDetailSerializer(transaction)
            return Response(serializer.data)
        except Transaction.DoesNotExist:
            return Response({'error': 'Transaction not found'}, status=status.HTTP_404_NOT_FOUND)
        

        

# 21
class RegistrationDetailView(APIView):
    def get(self, request, registration_id):
        try:
            registration = Registration.objects.get(id=registration_id)
            serializer = RegistrationDetailSerializer(registration)
            return Response(serializer.data)
        except Registration.DoesNotExist:
            return Response({'error': 'Registration not found'}, status=status.HTTP_404_NOT_FOUND)
        




#22
class CreateEventView(APIView):
    def post(self, request, organizer_id):
        try:
            organizer = Organizer.objects.get(pk=organizer_id)
        except Organizer.DoesNotExist:
            return Response({"error": "Organizer not found."}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['organizer'] = organizer.id  # attach organizer to event

        serializer = EventSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


    

# 23
class VerifyOrganizerView(APIView):
    def post(self, request, staff_id, organizer_id):
        try:
            staff = Admin.objects.get(pk=staff_id)
        except Admin.DoesNotExist:
            return Response({"error": "Invalid staff ID."}, status=status.HTTP_404_NOT_FOUND)

        try:
            organizer = Organizer.objects.get(pk=organizer_id)
        except Organizer.DoesNotExist:
            return Response({"error": "Invalid organizer ID."}, status=status.HTTP_404_NOT_FOUND)

        if organizer.verificationStatus:
            return Response({"message": "Organizer is already verified."}, status=status.HTTP_200_OK)

        # Update organizer fields
        organizer.verificationStatus = True
        organizer.dateOfVerification = date.today()
        organizer.staff = staff
        organizer.save()

        serializer = OrganizerVerificationSerializer(organizer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    



# 24
class SubmitFeedbackView(APIView):
    def post(self, request, user_id, event_id):
        # Attach user_id and event_id from URL into the request data
        request.data['user'] = user_id
        request.data['event'] = event_id

        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Feedback submitted successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# 25
class ComplaintCreateView(APIView):
    def post(self, request):
        serializer = ComplaintSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Complaint submitted successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



# 27
class CreateTransactionRegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationTransactionSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            user = data['user']
            event = data['event']
            total_price = data['total_price']
            num_tickets = data['number_of_tickets']

            # ✅ Check if event is upcoming
            if event.status.lower() != 'upcoming':
                return Response(
                    {"error": "This event is not open for registration."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # ✅ Check if enough tickets are available
            if event.maxAttendees is not None and event.ticketsSold + num_tickets > event.maxAttendees:
                return Response(
                    {"error": "Not enough tickets available for this event."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # ✅ Check wallet balance if applicable
            if data['payment_method'] == 'Wallet' and user.walletCash < total_price:
                return Response(
                    {"error": "Insufficient wallet balance."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                with transaction.atomic():
                    # Deduct wallet cash if applicable
                    if data['payment_method'] == 'Wallet':
                        user.walletCash -= total_price
                        user.save()

                    # Create Transaction
                    txn = Transaction.objects.create(
                        event=event,
                        user=user,
                        method_of_payment=data['payment_method'],
                        amount=total_price,
                        status='Processed'
                    )

                    # Create Registration
                    reg = Registration.objects.create(
                        user=user,
                        event=event,
                        transaction=txn
                    )

                    # Update event ticket count only after successful registration
                    event.ticketsSold += num_tickets
                    event.save()

            except Exception as e:
                return Response(
                    {"error": f"An error occurred during registration: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            return Response({'registration_id': reg.id}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



# 28
class EventRevenueAPIView(APIView):
    def get(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

        # Compute revenue
        ticket_price = event.ticketPrice
        tickets_sold = event.ticketsSold
        total_revenue = ticket_price * tickets_sold

        data = {
            "event_id": event.id,
            "event_name": event.eventName,
            "ticket_price": ticket_price,
            "tickets_sold": tickets_sold,
            "total_revenue": total_revenue
        }

        serializer = EventRevenueSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


#29
class UserTransactionHistoryView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        transactions = Transaction.objects.filter(user=user).order_by('-date_of_payment')
        total_transactions = transactions.count()
        serializer = TransactionSerializer(transactions, many=True)

        return Response({
            "user": user.username,
            "total_transactions": total_transactions,
            "transactions": serializer.data
        })
    



#30
class UserComplaintHistoryView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        complaints = Complaint.objects.filter(user=user).order_by('-Created_At')
        total_complaints = complaints.count()
        serializer = ComplaintSerializer(complaints, many=True)

        return Response({
            "user": user.username,
            "total_complaints": total_complaints,
            "complaints": serializer.data
        })


#31
class EventRevenueAPIView(APIView):
    def get(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

        # Compute revenue
        ticket_price = event.ticketPrice
        tickets_sold = event.ticketsSold
        total_revenue = ticket_price * tickets_sold

        data = {
            "event_id": event.id,
            "event_name": event.eventName,
            "ticket_price": ticket_price,
            "tickets_sold": tickets_sold,
            "total_revenue": total_revenue
        }

        serializer = EventRevenueSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

#32
class UpdateUserView(APIView):
    def put(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "Invalid user ID. No matching user found."},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#33
class UpdateOrganizerView(APIView):
    def put(self, request, organizer_id):
        try:
            organizer = Organizer.objects.get(id=organizer_id)
        except Organizer.DoesNotExist:
            return Response({"error": "Invalid organizer ID. No matching organizer found."},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = OrganizerUpdateSerializer(organizer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Organizer updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#34
class UpdateEventView(APIView):
    def put(self, request, event_id):
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return Response({"error": "Invalid event ID."}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()

        # Prevent changes to immutable fields
        immutable_fields = ['created_at']
        for field in immutable_fields:
            if field in data:
                data.pop(field)

        # Validate startDate and startTime are in the future
        start_date = data.get('startDate')
        start_time = data.get('startTime')

        if start_date and start_time:
            try:
                combined_datetime = datetime.combine(
                    datetime.strptime(start_date, "%Y-%m-%d").date(),
                    datetime.strptime(start_time, "%H:%M:%S").time()
                )
                combined_datetime = timezone.make_aware(combined_datetime)
                if combined_datetime < timezone.now():
                    return Response({"error": "Event cannot start in the past."}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error": "Invalid date/time format."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate fields like maxAttendees, ticketsSold, category, etc.
        if 'maxAttendees' in data:
            try:
                if int(data['maxAttendees']) <= 0:
                    return Response({"error": "maxAttendees must be greater than 0."}, status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response({"error": "maxAttendees must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

        if 'ticketsSold' in data:
            try:
                if int(data['ticketsSold']) < 0:
                    return Response({"error": "ticketsSold cannot be negative."}, status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response({"error": "ticketsSold must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

        if 'category' in data:
            if not isinstance(data['category'], str) or not data['category'].strip():
                return Response({"error": "Invalid category."}, status=status.HTTP_400_BAD_REQUEST)

        if 'organizer' in data and int(data['organizer']) != event.organizer_id:
            return Response({"error": "Organizer ID cannot be changed."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = EventSerializer(event, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)