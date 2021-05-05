from django.core.management import call_command
from django.test import TestCase
from django.contrib.auth.models import Group
from xshop.core.utils import UserGroup


class CreateGroupsTests(TestCase):
    def test_retrieve_existing_groups(self):
        self.assertEqual(Group.objects.all().count(), 0)
        call_command("create_groups")
        self.assertEqual(Group.objects.all().count(), 5)
        self.assertTrue(Group.objects.get(name=UserGroup.CUSTOMER))
        self.assertTrue(Group.objects.get(name=UserGroup.GENERAL_MANAGER))
        self.assertTrue(Group.objects.get(name=UserGroup.CASHIER))
        self.assertTrue(Group.objects.get(name=UserGroup.MANAGER))
        self.assertTrue(Group.objects.get(name=UserGroup.DATA_ENTRY_CLERK))
