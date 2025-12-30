from django.db import  migrations

class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.RunSQL(
            sql="""
                CREATE SCHEMA IF NOT EXISTS "django";
                CREATE SCHEMA IF NOT EXISTS "user";
                CREATE SCHEMA IF NOT EXISTS "market";
                CREATE SCHEMA IF NOT EXISTS "real_market";
                
                ALTER TABLE auth_group SET SCHEMA "django";
                ALTER TABLE auth_group_permissions SET SCHEMA "django";
                ALTER TABLE auth_permission SET SCHEMA "django";
                ALTER TABLE auth_user SET SCHEMA "django";
                ALTER TABLE auth_user_groups SET SCHEMA "django";
                ALTER TABLE auth_user_user_permissions SET SCHEMA "django";
                ALTER TABLE django_admin_log SET SCHEMA "django";
                ALTER TABLE django_content_type SET SCHEMA "django";
                ALTER TABLE django_migrations SET SCHEMA "django";
            """,
            reverse_sql="""
                DROP SCHEMA IF EXISTS "django";
                DROP SCHEMA IF EXISTS "user";
                DROP SCHEMA IF EXISTS "market";
                DROP SCHEMA IF EXISTS "real_market";
            """
        )
    ]