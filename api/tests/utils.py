from django.contrib.auth.models import Group, Permission


def create_merchant():
    g = Group.objects.create(name='Merchant')
    g.permissions.add(Permission.objects.get(codename='add_medicine'))
    g.save()
