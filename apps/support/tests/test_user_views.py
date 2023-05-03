from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token

from apps.users.models import User
from apps.support.models import SupportDepartment, SupportTicket
from apps.support.serializers.user_serializers import (
    SupportDepartmentListSerializer,
    SupportTicketListSerializer,
)


class SupportAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email='test@gmail.com',
            name='John Doe',
        )
        self.support_department = SupportDepartment.objects.create(
            name="Test Department",
            is_active=True,
        )
        self.support_ticket = SupportTicket.objects.create(
            user=self.user,
            department=self.support_department,
            title="Test Ticket",
            content="Test Ticket Content",
        )

        self.token = Token.objects.create(
            user=self.user,
        )
        self.api_authentication_header = f'Token {self.token.key}'

        self.support_department_list_url = reverse(
            'support_user:department-list',
        )

        self.support_ticket_create_url = reverse(
            'support_user:ticket-create',
        )

        self.support_ticket_list_url = reverse(
            'support_user:ticket-list',
        )

    def test_support_department_list_api_view(self):
        response = self.client.get(
            self.support_department_list_url,
            HTTP_AUTHORIZATION=self.api_authentication_header,
        )
        support_department_list = SupportDepartment.objects.all()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data['success'],
            True,
        )
        self.assertEqual(
            response.data['data'],
            SupportDepartmentListSerializer(
                support_department_list,
                many=True,
            ).data
        )

    def test_support_ticket_create_api_view(self):
        data = {
            'department': self.support_department.id,
            'title': 'New Test Ticket',
            'content': 'New Test Ticket Content',
        }
        response = self.client.post(
            self.support_ticket_create_url,
            data,
            HTTP_AUTHORIZATION=self.api_authentication_header,
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(
            response.data['success'],
            True,
        )
        self.assertEqual(
            response.data['message'],
            "Support ticket created successfully.",
        )
        self.assertIsNotNone(
            response.data['ticket_id'],
        )

    def test_support_ticket_list_api_view(self):
        response = self.client.get(
            self.support_ticket_list_url,
            HTTP_AUTHORIZATION=self.api_authentication_header,
        )
        support_ticket_list = SupportTicket.objects.filter(user=self.user)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data['success'],
            True,
        )
        self.assertEqual(
            response.data['data'],
            SupportTicketListSerializer(
                support_ticket_list,
                many=True,
            ).data
        )
