"""
    Django settings for meizhi project.
    
    For more information on this file, see
    https://docs.djangoproject.com/en/1.7/topics/settings/
    
    For the full list of settings and their values, see
    https://docs.djangoproject.com/en/1.7/ref/settings/
    """

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.split(os.path.dirname(__file__))[0]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'yee8j&wck@)g27g#q(!zkdud8zrnvj128^=$(^bnht1nk^g!2-'

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
                  'django.contrib.admin',
                  'django.contrib.auth',
                  'django.contrib.contenttypes',
                  'django.contrib.sessions',
                  'django.contrib.messages',
                  'django.contrib.staticfiles',
                  'apps.question',
                  'apps.product',
                  'apps.products',
                  'apps.feed',
                  'apps.search',
                  'apps.topic',
                  'apps.ucenter',
                  'apps.activities',
                  'apps.cart',
                  'apps.order',
                  'apps.middleware',
				  'apps.game',
                  'compressor',
                  )

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)

MIDDLEWARE_CLASSES = (
                      'django.contrib.sessions.middleware.SessionMiddleware',
                      'django.middleware.common.CommonMiddleware',
#                      'django.middleware.csrf.CsrfViewMiddleware',
                      'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
                      'django.middleware.gzip.GZipMiddleware',
                      'django.contrib.messages.middleware.MessageMiddleware',
                      'django.middleware.clickjacking.XFrameOptionsMiddleware',
                      'apps.middleware.user_tracking_middleware.UserTrackingMiddleware',
                      )

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'm_fenpu',
    'USER': 'root',
    'PASSWORD': 'applen_(0)',
    'HOST': '182.92.67.121',
    'PORT': '3306',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATIC_PATH = os.path.join(BASE_DIR,'static')

STATICFILES_DIRS = (
    STATIC_PATH,
)

COMPRESS_ROOT = '/static/'
#COMPRESS_URL = 'include/' 
COMPRESS_ENABLED = True

#logging
LOGGING = {
  'version': 1,
  'disable_existing_loggers': False,
  'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/data/fenpu-mobile/django.log',
        },
  },
  'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
  },
}
