import logging

from django.core.management.base import BaseCommand
from xshop.core.utils import UserGroup
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

GROUPS = [
    UserGroup.CUSTOMER,
    UserGroup.CASHIER,
    UserGroup.DATA_ENTRY_CLERK,
    UserGroup.GENERAL_MANAGER,
    UserGroup.MANAGER,
]
MODELS = ["Invoice", "Order", "Shop", "Product"]
PERMISSIONS = ["add", "change" "delete" "view"]


class Command(BaseCommand):
    def handle(self, *args, **options):

        for group in GROUPS:
            new_group, created = Group.objects.get_or_create(name=group)
            for model in MODELS:
                for permission in PERMISSIONS:
                    name = "Can {} {}".format(permission, model)
                    self.stdout.write("Creating {}".format(name))

                    try:
                        model_add_perm = Permission.objects.get(name=name)
                    except Permission.DoesNotExist:
                        logging.warning(
                            "Permission not found with name '{}'.".format(name)
                        )
                        continue

                    new_group.permissions.add(model_add_perm)
