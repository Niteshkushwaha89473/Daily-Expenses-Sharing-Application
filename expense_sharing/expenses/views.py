from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.contrib.auth.models import User
from .models import Expense
from .serializers import ExpenseSerializer
import csv
from django.http import HttpResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model

User = get_user_model()

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        expense = self.get_object()
        jwt_authenticator = JWTAuthentication()
        try:
            validated_token = jwt_authenticator.get_validated_token(request.headers.get('Authorization').split()[1])
            user_from_token = jwt_authenticator.get_user(validated_token)
        except Exception as e:
            raise AuthenticationFailed('Invalid token')

        if expense.created_by != user_from_token:
            raise AuthenticationFailed('You do not have permission to view this expense')

        return super().retrieve(request, *args, **kwargs)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def user_expenses(self, request):
        user_expenses = Expense.objects.filter(created_by=request.user)
        serializer = self.get_serializer(user_expenses, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated, IsAdminUser])
    def overall_expenses(self, request):
        overall_expenses = Expense.objects.all()
        serializer = self.get_serializer(overall_expenses, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated, IsAdminUser])
    def download_balance_sheet(self, request):
        # Create the HttpResponse object with the appropriate CSV header.
        response =  HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="balance_sheet.csv"'},
            )
        writer = csv.writer(response)
        writer.writerow(['Title', 'Amount', 'Split Type', 'Created By', 'Created At', 'Split Info'])

        expenses = Expense.objects.all()
        for expense in expenses:
            split_info = "; ".join(
                [f"{split.user.username}: {split.amount} ({split.percentage}%)" for split in expense.splits.all()]
            )
            writer.writerow([
                expense.title, 
                expense.amount, 
                expense.get_split_type_display(), 
                expense.created_by.username, 
                expense.created_at,
                split_info
            ])

        return response

    # update ExpenseViewSet class to enforce condition like retrieve on the put and delete methods and can be modified by admin only
    def update(self, request, *args, **kwargs):
        expense = self.get_object()
        jwt_authenticator = JWTAuthentication()
        try:
            validated_token = jwt_authenticator.get_validated_token(request.headers.get('Authorization').split()[1])
            user_from_token = jwt_authenticator.get_user(validated_token)
        except Exception as e:
            raise AuthenticationFailed('Invalid token')

        if not user_from_token.is_staff:
            raise AuthenticationFailed('Only admin can update an expense')

        # Ensure nested fields are handled properly
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(expense, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Explicitly handle nested fields update
        self.perform_update(serializer)

        if getattr(expense, '_prefetched_objects_cache', None):
            # If 'prefetched_objects_cache' is not None, it means that the prefetch cache needs to be invalidated.
            expense._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        # Custom update method to handle nested fields
        validated_data = serializer.validated_data
        splits_data = validated_data.pop('splits', None)
        
        # Update the expense instance
        expense = serializer.save()
        
        # Handle nested splits if provided
        if splits_data:
            expense.splits.all().delete()
            for split_data in splits_data:
                expense.splits.create(**split_data)
    
    def destroy(self, request, *args, **kwargs):
        
        expense = self.get_object()
        jwt_authenticator = JWTAuthentication()
        try:
            validated_token = jwt_authenticator.get_validated_token(request.headers.get('Authorization').split()[1])
            user_from_token = jwt_authenticator.get_user(validated_token)
        except Exception as e:
            raise AuthenticationFailed('Invalid token')

        if not user_from_token.is_staff:
            raise AuthenticationFailed('Only admin can delete an expense')
        return super().destroy(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_403_FORBIDDEN)
    
