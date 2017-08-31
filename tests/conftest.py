import os
import sys

import django
import pytest
from django.conf import settings


@pytest.fixture()
def vocabulary_factory():
    from thesaurus.models import Vocabulary

    def make_vocabulary(**args):
        return Vocabulary.objects.create(**args)

    return make_vocabulary


def pytest_configure():
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # NOQA

    sys.path.append(os.path.abspath(os.path.join(BASE_DIR, '..')))

    INSTALLED_APPS = [  # NOQA
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'thesaurus',
    ]

    MIDDLEWARE_CLASSES = [  # NOQA
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    settings.configure(
        SECRET_KEY="test-key",
        DEBUG=False,
        TEMPLATE_DEBUG=False,
        ALLOWED_HOSTS=[],
        INSTALLED_APPS=INSTALLED_APPS,
        MIDDLEWARE_CLASSES=MIDDLEWARE_CLASSES,
        ROOT_URLCONF='tests.urls',
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(BASE_DIR, 'test_db.sqlite3'),
            }
        },
        LANGUAGE_CODE='en-us',
        TIME_ZONE='UTC',
        USE_I18N=True,
        USE_L10N=True,
        USE_TZ=True,
        STATIC_URL='/static/',
    )

    django.setup()
