from django.shortcuts import render
from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from datetime import timedelta
from roles_creation.permissions import HasRolePermission
from .serializers import TicketHistorySerializer,ReportSerializer,AttachmentSerializer
from .models import History,Reports,Attachment
from timer.models import Ticket

class HistoryAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, ticket=None):
        self.permission_required = "view_history"
        if not HasRolePermission().has_permission(request, self.permission_required):
          return Response({'error': 'Permission denied.'}, status=403)
        
        
        try:
            ticket = request.query_params.get('ticket')
            print(ticket)
            history = History.objects.filter(ticket=ticket)
            serializer = TicketHistorySerializer(history, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
          return Response({"error": "Invalid request."}, status=status.HTTP_400_BAD_REQUEST)
    
 

    def post(self, request, *args, **kwargs):
            self.permission_required = "create_history"
            if not HasRolePermission().has_permission(request, self.permission_required):
                return Response({'error': 'Permission denied.'}, status=403)
            serializer = TicketHistorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(modified_by=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
          
class ReportAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        self.permission_required = "view_report"
        if not HasRolePermission().has_permission(request, self.permission_required):
          return Response({'error': 'Permission denied.'}, status=403)
        ticket = request.query_params.get('ticket')
        if not ticket:
            return Response({"error": "Ticket parameter is required"},status=status.HTTP_400_BAD_REQUEST)
        try:
            report = Reports.objects.filter(ticket=ticket)
            if not report.exists():
                return Response({"error": "No reports found for the given ticket"},status=status.HTTP_404_NOT_FOUND)
            serializer = ReportSerializer(report, many=True,context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"},status=status.HTTP_400_BAD_REQUEST)
 
    def post(self, request, *args, **kwargs):
            self.permission_required = "create_report"
            if not HasRolePermission().has_permission(request, self.permission_required):
                return Response({'error': 'Permission denied.'}, status=403)
            serializer = ReportSerializer(data=request.data,context={'request': request})
            if serializer.is_valid():
                serializer.save(modified_by=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class AttachmentsAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    # def get(self, request):
    #     # self.permission_required = "view_employee"  
    #     # HasRolePermission.has_permission(self,request,self.permission_required)
       
    #     if 1:
    #         ticket=request.query_params.get('ticket')
    #         print(ticket)
    #         report = Attachment.objects.filter(ticket=ticket)
    #         serializer = AttachmentSerializer(report, many=True)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     else:
    #       return Response({"error": "Invalid request."}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        ticket_id = request.query_params.get("ticket_id")
        user = request.user
 
        try:
            ticket = Ticket.objects.get(ticket_id=ticket_id)
        except Ticket.DoesNotExist:
            return Response({"error": "Ticket not found"}, status=404)
 
        if ticket.created_by_id == user.id or ticket.assignee_id == user.id:
            attachments = Attachment.objects.filter(ticket=ticket)
            serializer = AttachmentSerializer(attachments, many=True)
            return Response(serializer.data)
 
        return Response({"detail": "You do not have permission to view these attachments."}, status=403)
 
 
 

class TicketChatHistory(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, ticket_id):
        messages = History.objects.filter(ticket__ticket_id=ticket_id).order_by('created_at')
        data = [
            {
                'username': msg.created_by.username,
                'message': msg.title,
                'created_at': msg.created_at
            } for msg in messages
        ]
        return Response(data)
