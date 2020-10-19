"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 3.1rc1.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

import environ
import sentry_sdk

from pathlib import Path
from sentry_sdk.integrations.django import DjangoIntegration

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

# django-environ
env = environ.Env(
    # # set casting, default value
    # DEBUG=(bool, False)
)

# Deploy NOTE defined first to decide when to read the .env file
DEPLOY = env("DEPLOY", str, None)

# reading .env file () when testing and in LOCAL env else read from env vars
if not DEPLOY or DEPLOY == "LOCAL":
    environ.Env.read_env(str(BASE_DIR / ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY", str)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG", bool, False)

ALLOWED_HOSTS = env(
    "ALLOWED_HOSTS", tuple, ("localhost", "127.0.0.1", ".shahwan.me", ".herokuapp.com")
)


# Application definition

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party
    "django_extensions",
    "rest_framework",
    "rest_framework.authtoken",
    "phonenumber_field",
    "multiselectfield",
    "crispy_forms",
    # Local
    "xshop.users.apps.UsersConfig",
    "xshop.pages.apps.PagesConfig",
    "xshop.core.apps.CoreConfig",
]


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ]
}

MIDDLEWARE = [
    # Simplified static file serving.
    # https://warehouse.python.org/project/whitenoise/
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("POSTGRES_HOST"),
        "PORT": env("POSTGRES_PORT"),
        "TEST": {"NAME": "xshop_test_db"},
        "CONN_MAX_AGE": 60 if DEPLOY != "LOCAL" else 0,
        "ATOMIC_REQUESTS": True,
    }
}


# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = (BASE_DIR / "static",)

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# PhoneNumber settings
PHONENUMBER_DB_FORMAT = "E164"
PHONENUMBER_DEFAULT_REGION = "EG"

# user model
AUTH_USER_MODEL = "users.User"

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# django-crispy-forms
CRISPY_TEMPLATE_PACK = "bootstrap4"

# Login Redirection
LOGIN_REDIRECT_URL = "pages:home"
LOGOUT_REDIRECT_URL = "pages:home"

# sentry
if DEPLOY and DEPLOY not in ("LOCAL", "TESTING"):
    sentry_sdk.init(
        dsn=env("SENTRY_DSN", str),
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True,
    )

# TODO update later
DASHBOARD_MODULES = []

# django-money
CURRENCIES = ("EGP",)
CURRENCY_CHOICES = [
    ("EGP", "EGP E£"),
]
DEFAULT_CURRENCY = "EGP"
CURRENCY_DECIMAL_PLACES = 2

# All URLs end with '/'
APPEND_SLASH = True

# django admin customization with jazzmin
JAZZMIN_SETTINGS = {
    # title of the window
    "site_title": "XShop",
    # Title on the brand, and the login screen (19 chars max)
    "site_header": "XShop",
    # square logo to use for your site, must be present in static files, used for favicon and brand on top left
    # "site_logo": "polls/img/logo.png",
    # Welcome text on the login screen
    "welcome_sign": "Welcome to XShop",
    # Copyright on the footer
    "copyright": "Egypt Shops LLC",
    # The model admin to search from the search bar, search bar omitted if excluded
    "search_model": "users.User",
    # Field name on user model that contains avatar image
    "user_avatar": None,
    ############
    # Top Menu #
    ############
    # Links to put along the top menu
    "topmenu_links": [
        # Url that gets reversed (Permissions can be added)
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        # external url that opens in a new window (Permissions can be added)
        # {
        #     "name": "Support",
        #     "url": "https://github.com/farridav/django-jazzmin/issues",
        #     "new_window": True,
        # },
        # model admin to link to (Permissions checked against model)
        # {"model": "users.User"},
        # App with dropdown menu to all its models pages (Permissions checked against models)
        # {"app": "core"},
    ],
    #############
    # User Menu #
    #############
    # Additional links to include in the user menu on the top right ('app' url type is not allowed)
    "usermenu_links": [
        # {
        #     "name": "Support",
        #     "url": "https://github.com/farridav/django-jazzmin/issues",
        #     "new_window": True,
        # },
        {"model": "users.User"},
    ],
    #############
    # Side Menu #
    #############
    # Whether to display the side menu
    "show_sidebar": True,
    # Whether to aut expand the menu
    "navigation_expanded": True,
    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": [],
    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],
    # List of apps to base side menu ordering off of (does not need to contain all apps)
    "order_with_respect_to": ["core", "users"],
    # Custom links to append to app groups, keyed on app name
    # "custom_links": {
    #     "polls": [
    #         {
    #             "name": "Make Messages",
    #             "url": "make_messages",
    #             "icon": "fas fa-comments",
    #             "permissions": ["polls.view_poll"],
    #         }
    #     ]
    # },
    # Custom icons for side menu apps/models See https://www.fontawesomecheatsheet.com/font-awesome-cheatsheet-5x/
    # for a list of icon classes
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": None,
    "custom_js": None,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": False,
    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "horizontal_tabs",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {
        "users.User": "collapsible",
        "auth.group": "vertical_tabs",
    },
    # Add a language dropdown into the admin
    "language_chooser": False,
}
