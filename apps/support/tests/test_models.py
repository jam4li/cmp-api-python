from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.users.models import User
from apps.support.models import (
    SupportDepartment,
    SupportTicket,
    SupportTicketReply,
)


class SupportTestCase(TestCase):
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
            title='Test Ticket Title',
            content='Test Ticket Content',
        )

    def test_support_department_creation(self):
        self.assertEqual(
            self.department.name,
            'Test Department',
        )

    def test_support_ticket_creation(self):
        self.assertEqual(
            self.ticket.user,
            self.user,
        )
        self.assertEqual(
            self.ticket.department,
            self.department,
        )
        self.assertEqual(
            self.ticket.title,
            'Test Ticket Title',
        )
        self.assertEqual(
            self.ticket.content,
            'Test Ticket Content',
        )

    def test_support_ticket_reply_creation(self):
        # Create a test SupportTicketReply
        reply = SupportTicketReply.objects.create(
            ticket=self.ticket,
            content='Test Reply Content',
        )

        self.assertEqual(
            reply.ticket,
            self.ticket,
        )
        self.assertEqual(
            reply.content,
            'Test Reply Content',
        )

    # TODO: Add test_support_ticket_reply_with_attachment
