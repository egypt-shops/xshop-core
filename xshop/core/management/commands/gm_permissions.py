from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

from xshop.core.utils import UserGroup


GROUP = Group.objects.get(name=UserGroup.GENERAL_MANAGER)
APPS = {
    "invoices": ["invoice"],
    "orders": ["order", "order item"],
    "products": ["product"],
    "users": ["general manager", "manager", "data entry clerk", "cashier"],
    "shops": ["shop"],
}
ACTIONS = ["add", "change" "delete" "view"]


class Command(BaseCommand):
    def handle(self, *args, **options):
        for app in APPS:
            if app != "shops":
                for model in APPS.get(app):
                    ct = ContentType.objects.get(app_label=app, model=model)
                    if app == "users" and model == "general manager":
                        code_name = f"{app}.view_{model}"
                        permission = Permission.objects.create(
                            codename=code_name, content_type=ct
                        )
                        GROUP.permissions.add(permission)
                        code_name = f"{app}.change_{model}"
                        permission = Permission.objects.create(
                            codename=code_name, content_type=ct
                        )
                        GROUP.permissions.add(permission)
                    else:
                        for action in ACTIONS:
                            code_name = f"{app}.{action}_{model}"
                            permission = Permission.objects.create(
                                codename=code_name, content_type=ct
                            )
                            GROUP.permissions.add(permission)
            else:
                ct = ContentType.objects.get(app_label="shops", model="shop")
                code_name = "shops.view_shop"
                permission = Permission.objects.create(
                    codename=code_name, content_type=ct
                )
                GROUP.permissions.add(permission)
                code_name = "shops.change_shop"
                permission = Permission.objects.create(
                    codename=code_name, content_type=ct
                )
                GROUP.permissions.add(permission)
