config_name = 'master_locations'


def set_django_conf_name(name):
    global config_name
    config_name = name


def get_django_name():
    global config_name
    return config_name


def configure_django():
    import os
    import django
    set_django_conf_name('admin_dashboard.master_locations')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin_dashboard.admin_dashboard.settings")
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
    django.setup()


