from django.core.management.base import BaseCommand
from xshop.core.utils import UserGroup
from django.contrib.auth.models import Group

GROUPS = [
    UserGroup.CUSTOMER,
    UserGroup.CASHIER,
    UserGroup.DATA_ENTRY_CLERK,
    UserGroup.GENERAL_MANAGER,
    UserGroup.MANAGER,
]


class Command(BaseCommand):
    def handle(self, *args, **options):
        for group in GROUPS:
            Group.objects.get_or_create(name=group)
