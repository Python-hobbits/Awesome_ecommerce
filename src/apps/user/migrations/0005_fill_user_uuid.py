from django.db import migrations, models
import uuid


def create_uuid(apps, schema_editor):
    User = apps.get_model('user', 'User')
    for user in User.objects.all():
        user.uuid = uuid.uuid4()
        user.save()


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0004_user_uuid_alter_user_user_type"),
    ]

    operations = [
        migrations.RunPython(create_uuid),
    ]
