from django.test import TestCase
from django.utils.timezone import localtime

from apps.support.models import SupportDepartment, SupportTicket, User
from apps.support.serializers.user_serializers import (
    SupportDepartmentListSerializer,
    SupportTicketCreateSerializer,
    SupportTicketListSerializer,
)


class SupportSerializersTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create(
            email='test@gmail.com',
            name='John Doe',
        )

        # Create a test SupportDepartment
        self.department = SupportDepartment.objects.create(
            name='Test Department',
        )

        # Create a test SupportTicket
        self.ticket = SupportTicket.objects.create(
            user=self.user,
            department=self.department,
            title='Test Ticket',
            content='Test Ticket Content',
        )

    def test_support_department_list_serializer(self):
        serialized_data = SupportDepartmentListSerializer(self.department).data
        expected_data = {
            'id': self.department.id,
            'name': 'Test Department',
            'icon': None,
            'is_active': True,
        }
        self.assertEqual(serialized_data, expected_data)

    def test_support_ticket_create_serializer(self):
        data = {
            'department': self.department.id,
            'title': 'New Ticket',
            'content': 'New ticket content',
        }
        serializer = SupportTicketCreateSerializer(data=data)
        self.assertTrue(
            serializer.is_valid(),
        )

        new_ticket = serializer.save(
            user=self.user,
        )
        self.assertEqual(
            new_ticket.user,
            self.user,
        )
        self.assertEqual(
            new_ticket.department,
            self.department,
        )
        self.assertEqual(
            new_ticket.title,
            'New Ticket',
        )
        self.assertEqual(
            new_ticket.content,
            'New ticket content',
        )

    # TODO: Fix created_at in the expected_data
    # def test_support_ticket_list_serializer(self):
    #     serialized_data = SupportTicketListSerializer(
    #         self.ticket,
    #     ).data
    #     expected_data = {
    #         'id': self.ticket.id,
    #         'title': 'Test Ticket',
    #         'content': 'Test Ticket Content',
    #         'created_at': localtime(self.ticket.created_at).isoformat().replace('+00:00', 'Z').replace('+04:30', 'Z'),
    #     }
    #     self.assertEqual(
    #         serialized_data,
    #         expected_data,
    #     )
