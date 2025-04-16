from django.shortcuts import render

from rest_framework import serializers

from .models import *

from decimal import Decimal

from datetime import datetime

from django.utils import timezone 









#1,User Signup Serializer
class UserSignupSerializer(serializers.ModelSerializer):
    confirmPassword = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'confirmPassword', 'firstName', 'lastName', 'emailID', 'contactNo']

    def validate(self, data):
        if data['password'] != data['confirmPassword']:
            raise serializers.ValidationError("Passwords do not match.")
        if not data.get('emailID') and not data.get('contactNo'):
            raise serializers.ValidationError("Either emailID or contactNo is required.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirmPassword')
        return User.objects.create(**validated_data)
    



#2,User Login Serializer
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()





#3,Admin Login Serializer
class AdminLoginSerializer(serializers.Serializer):
    emailID = serializers.EmailField()
    password = serializers.CharField(write_only=True)





#4,Organizer Login Serializer
class OrganizerLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        try:
            organizer = Organizer.objects.get(username=username)
        except Organizer.DoesNotExist:
            raise serializers.ValidationError("Invalid username or password.")

        if organizer.password != password:
            raise serializers.ValidationError("Invalid username or password.")

        return {
            "id": organizer.id,
            "username": organizer.username
        }





#5,Organizer Signup Serializer
class OrganizerSignupSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = Organizer
        fields = ['username', 'password', 'confirm_password', 'firstName', 'lastName', 'emailID', 'contactNo']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        
        if not data.get('emailID') and not data.get('contactNo'):
            raise serializers.ValidationError("Either emailID or contactNo must be provided.")

        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')  # remove before saving
        return Organizer.objects.create(**validated_data)
    



#6,Event Detail Serializer
class EventDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


#7,Event Serializer
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'



#8,Organizer List Serializer
class OrganizerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizer
        fields = ['id', 'username', 'firstName', 'lastName', 'emailID', 'contactNo', 'organization', 'verificationStatus']




#9,Organizer Average Rating Serializer
class OrganizerAvgRatingSerializer(serializers.Serializer):
    organizerID = serializers.IntegerField()
    firstName = serializers.CharField()
    lastName = serializers.CharField(allow_null=True)
    avgRating = serializers.FloatField()




#10,Complaint Count Serializer
class ComplaintCountSerializer(serializers.Serializer):
    organizer_id = serializers.IntegerField()
    event_id = serializers.IntegerField(required=False)
    complaints = serializers.IntegerField()



#11
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['id']  # Don't show user ID



#12
class AdminDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        exclude = ['id']  # Don't show admin ID




#13
class OrganizerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizer
        exclude = ['id']  # Don't show organizer ID




#14
class UnverifiedOrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizer
        fields = '__all__'




#15
class FeedbackSerializer(serializers.ModelSerializer):
    eventName = serializers.CharField(source='event.eventName', read_only=True)
    
    class Meta:
        model = Feedback
        fields = ['eventName', 'Rating', 'Comments', 'Created_At']




#16
class TransactionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        exclude = ['id']  # or use fields if you want specific ones





#17
class EventBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id',
            'eventName',
            'category',
            'startDate',
            'startTime',
            'endDate',
            'endTime'
        ]

class UserRegistrationSerializer(serializers.ModelSerializer):
    event = EventBasicSerializer()
    transaction = TransactionDetailSerializer()

    class Meta:
        model = Registration
        fields = ['event', 'transaction']

class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'firstName', 'lastName']




#18
class ComplaintDetailSerializer(serializers.ModelSerializer):
    user = UserBasicSerializer(read_only=True)
    event = EventBasicSerializer(read_only=True)

    class Meta:
        model = Complaint
        fields = '__all__'



#19
class FeedbackDetailSerializer(serializers.ModelSerializer):
    user = UserBasicSerializer(read_only=True)
    event = EventBasicSerializer(read_only=True)

    class Meta:
        model = Feedback
        fields = '__all__'



#20
class TransactionDetailSerializer(serializers.ModelSerializer):
    user = UserBasicSerializer(read_only=True)
    event = EventBasicSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'




#21
class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'firstName']

class EventSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'eventName', 'category', 'startDate', 'endDate']

class TransactionSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'method_of_payment', 'date_of_payment', 'status']

class RegistrationDetailSerializer(serializers.ModelSerializer):
    user = UserSummarySerializer(read_only=True)
    event = EventSummarySerializer(read_only=True)
    transaction = TransactionSummarySerializer(read_only=True)

    class Meta:
        model = Registration
        fields = ['id', 'user', 'event', 'transaction']


#22
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        exclude = ['created_at', 'ticketsSold', 'status']  # status can be handled automatically

    def validate(self, data):
        # Grab current datetime
        current_datetime = datetime.now()

        start_date = data.get('startDate')
        start_time = data.get('startTime')
        end_date = data.get('endDate')
        end_time = data.get('endTime')

        # Constraint 1: Start date and time must be in the future
        start_datetime = datetime.combine(start_date, start_time)
        if start_datetime <= current_datetime:
            raise serializers.ValidationError("Start time must be in the future.")

        # Constraint 2: End time must be after start time
        end_datetime = datetime.combine(end_date, end_time)
        if end_datetime <= start_datetime:
            raise serializers.ValidationError("End time must be after start time.")

        # Constraint 3: Ticket price should be >= 0
        if data.get('ticketPrice') is not None and data['ticketPrice'] < 0:
            raise serializers.ValidationError("Ticket price cannot be negative.")

        return data

    def create(self, validated_data):
        validated_data['status'] = 'Upcoming'
        return super().create(validated_data)

#23
class OrganizerVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizer
        fields = ['id', 'username', 'emailID', 'verificationStatus', 'dateOfVerification', 'staff']
        read_only_fields = ['id', 'username', 'emailID', 'dateOfVerification', 'staff']


        

#24
class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['event', 'user', 'Rating', 'Comments']

    def validate(self, data):
        # Validate event exists
        event = data.get('event')
        user = data.get('user')

        if not Event.objects.filter(id=event.id).exists():
            raise serializers.ValidationError("Invalid event ID.")

        if not User.objects.filter(id=user.id).exists():
            raise serializers.ValidationError("Invalid user ID.")

        # Ensure user hasn't already given feedback for this event
        if Feedback.objects.filter(user=user, event=event).exists():
            raise serializers.ValidationError("Feedback already submitted for this event by this user.")

        return data

#25
class ComplaintSerializer(serializers.ModelSerializer):
    event_id = serializers.IntegerField(write_only=True)
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Complaint
        fields = ['event_id', 'user_id', 'Description', 'Category']

    def validate(self, data):
        event_id = data.get('event_id')
        user_id = data.get('user_id')

        if not Event.objects.filter(id=event_id).exists():
            raise serializers.ValidationError("Invalid event_id.")

        if not User.objects.filter(id=user_id).exists():
            raise serializers.ValidationError("Invalid user_id.")

        # Check for unique constraint
        if Complaint.objects.filter(user_id=user_id, event_id=event_id, Category=data['Category']).exists():
            raise serializers.ValidationError("Complaint for this event, user, and category already exists.")

        return data

    def create(self, validated_data):
        return Complaint.objects.create(
            event_id=validated_data['event_id'],
            user_id=validated_data['user_id'],
            Description=validated_data['Description'],
            Category=validated_data['Category']
        )


#27
class RegistrationTransactionSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    event_id = serializers.IntegerField()
    payment_method = serializers.ChoiceField(choices=[m for m in Transaction.PAYMENT_METHODS])
    number_of_tickets = serializers.IntegerField(min_value=1)

    def validate(self, data):
        try:
            user = User.objects.get(id=data['user_id'])
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid user ID.")

        try:
            event = Event.objects.get(id=data['event_id'])
        except Event.DoesNotExist:
            raise serializers.ValidationError("Invalid event ID.")

        total_price = Decimal(event.ticketPrice) * data['number_of_tickets']

        if data['payment_method'] == 'Wallet' and user.walletCash < total_price:
            raise serializers.ValidationError("Insufficient wallet balance.")

        if event.ticketsSold + data['number_of_tickets'] > event.maxAttendees:
            raise serializers.ValidationError("Not enough tickets available.")

        data['user'] = user
        data['event'] = event
        data['total_price'] = total_price
        return data


#28 
class EventRevenueSerializer(serializers.Serializer):
    event_id = serializers.IntegerField()
    event_name = serializers.CharField()
    ticket_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    tickets_sold = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=15, decimal_places=2)



#29
class TransactionSerializer(serializers.ModelSerializer):
    eventName = serializers.CharField(source='event.eventName', read_only=True)
    
    class Meta:
        model = Transaction
        fields = ['id', 'eventName', 'method_of_payment', 'amount', 'date_of_payment', 'status']



#30
class ComplaintSerializer(serializers.ModelSerializer):
    eventName = serializers.CharField(source='event.eventName', read_only=True)
    staffName = serializers.CharField(source='staff.username', read_only=True)

    class Meta:
        model = Complaint
        fields = ['id', 'eventName', 'Category', 'Description', 'Status', 'staffName', 'Created_At']


#31
class OrganizerRevenueStatsSerializer(serializers.Serializer):
    organizer_id = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_attendees = serializers.IntegerField()




#32
class UserUpdateSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            'password', 'confirm_password', 'lastName', 'emailID',
            'contactNo', 'dob'
        ]

    def validate(self, data):
        # If password is being updated, confirm_password must be provided
        if 'password' in data:
            if 'confirm_password' not in data:
                raise serializers.ValidationError({"confirm_password": "This field is required when changing password."})
            if data['password'] != data['confirm_password']:
                raise serializers.ValidationError({"password": "Password and confirm password do not match."})
        return data

    def update(self, instance, validated_data):
        # Remove confirm_password as it's not a model field
        validated_data.pop('confirm_password', None)

        # Only update fields allowed
        for field in ['password', 'lastName', 'emailID', 'contactNo', 'dob']:
            if field in validated_data:
                setattr(instance, field, validated_data[field])

        instance.full_clean()
        instance.save()
        return instance
    


    
#33
class OrganizerUpdateSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Organizer
        fields = [
            'emailID', 'contactNo', 'password', 'confirm_password', 'organization'
        ]

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password:
            if not confirm_password:
                raise serializers.ValidationError("Please provide confirm_password when updating password.")
            if password != confirm_password:
                raise serializers.ValidationError("Password and confirm_password do not match.")
        
        return data

    def update(self, instance, validated_data):
        if 'emailID' in validated_data:
            instance.emailID = validated_data['emailID']
        if 'contactNo' in validated_data:
            instance.contactNo = validated_data['contactNo']
        if 'password' in validated_data:
            instance.password = validated_data['password']
        if 'organization' in validated_data:
            instance.organization = validated_data['organization']

        instance.save()
        return instance




#34
class EventUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        exclude = ['created_at']  # Prevent updates to this field

    def validate(self, data):
        # Validate organizer existence
        if 'organizer' in data and data['organizer'] is not None:
            if not Organizer.objects.filter(id=data['organizer'].id).exists():
                raise serializers.ValidationError({'organizer': 'Invalid organizer ID.'})

        # Use fallback to instance values if not present in partial update
        start_date = data.get('startDate', getattr(self.instance, 'startDate', None))
        end_date = data.get('endDate', getattr(self.instance, 'endDate', None))
        start_time = data.get('startTime', getattr(self.instance, 'startTime', None))
        end_time = data.get('endTime', getattr(self.instance, 'endTime', None))

        if start_date and end_date:
            if end_date < start_date:
                raise serializers.ValidationError("End date cannot be before start date.")
            elif end_date == start_date and end_time and start_time and end_time <= start_time:
                raise serializers.ValidationError("End time must be after start time when dates are the same.")

        # Validate ticketsSold <= maxAttendees
        max_attendees = data.get('maxAttendees', getattr(self.instance, 'maxAttendees', None))
        tickets_sold = data.get('ticketsSold', getattr(self.instance, 'ticketsSold', None))
        if max_attendees is not None and tickets_sold is not None:
            if tickets_sold > max_attendees:
                raise serializers.ValidationError("Tickets sold cannot exceed max attendees.")

        return data


#35
class EventRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.emailID', read_only=True)
    contact = serializers.CharField(source='user.contactNo', read_only=True)

    class Meta:
        model = Registration
        fields = ['id', 'username', 'email', 'contact']

#36
class AverageTicketsSoldSerializer(serializers.Serializer):
    organizer_id = serializers.IntegerField()
    average_percentage_sold = serializers.FloatField()


#38
class ComplaintSerializer(serializers.ModelSerializer):
    event_name = serializers.CharField(source='event.eventName', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    organizer_name = serializers.CharField(source='event.organizer.username', read_only=True)

    class Meta:
        model = Complaint
        fields = ['id', 'event_name', 'user_name', 'organizer_name', 'Category', 'Status', 'Description', 'Created_At']



#39
class TopUserSerializer(serializers.ModelSerializer):
    events_registered = serializers.IntegerField()

    class Meta:
        model = User
        fields = ['id', 'username', 'emailID', 'contactNo', 'events_registered']

#40
class EventAttendeeWithTicketsSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    username = serializers.CharField()
    firstName = serializers.CharField()
    lastName = serializers.CharField()
    num_tickets = serializers.IntegerField()

#41
class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

#42
class EventPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


#43
class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = '__all__'

    def validate_pincode(self, value):
        if not value.isdigit() or not (5 <= len(value) <= 10):
            raise serializers.ValidationError("Pincode must be 5 to 10 digits.")
        return value

#44
class EventDetailCSerializer(serializers.ModelSerializer):
    venue_location = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['eventName', 'startDate', 'ticketPrice', 'status', 'venue_location']

    def get_venue_location(self, obj):
        if obj.venue:
            return f"{obj.venue.name}, {obj.venue.street}, {obj.venue.city}, {obj.venue.state}, {obj.venue.pincode}"
        return "No venue assigned"

#45
class UserNameSerializer(serializers.Serializer):
    username = serializers.CharField()
    firstName = serializers.CharField()
    lastName = serializers.CharField(allow_null=True, allow_blank=True)


#46
class ComplaintStatusUpdateSerializer(serializers.Serializer):
    status_id = serializers.IntegerField(min_value=1, max_value=4)


#47
class AdminOrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizer
        fields = ['id', 'username']  # adjust fields as per Organizer model

class AdminVenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ['id', 'name']  # adjust fields as needed

class AllEventsForAdminSerializer(serializers.ModelSerializer):
    organizer = AdminOrganizerSerializer()
    venue = AdminVenueSerializer()

    class Meta:
        model = Event
        fields = '__all__'


#48
class AllTheOrganisersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizer
        fields = '__all__'


#49
class WalletTopUpSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0.")
        return value
