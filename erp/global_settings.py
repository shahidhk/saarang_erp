# Django settings for saarang_erp project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# The model to use as a profile for users
AUTH_PROFILE_MODULE = 'userprofile.UserProfile'

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.4/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Kolkata'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True


# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'm&amp;@6f9kg-8&amp;upa$6_o140_#8(n5tkhl83w*hu@eqbes7qg2-d7'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'erp.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'erp.wsgi.application'


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'forum',
    'userprofile',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

DEPARTMENTS = (
     ('public', 'Public'),
        ('coregroup','Core Group'),
        ('qms', 'QMS'),
        ('webops', 'Web Operaions'),
        ('publicity', 'Publicity'),
        ('ticketsales', 'Ticketsales'),
        ('spons', 'Sponsorship'),
        ('fr', 'Facilities & Requirements'),
        ('design', 'Design'),
        ('hospi', 'Hospitality'),
        ('events', 'Events'),
        ('finance','Finance'), 
        ('security', 'Security'),
        ('proshows','Pro Shows'),
    )

EVENTS = (
        ('na','Not Applicable'),

        ('qms', 'QMS'),
        ('webops', 'Web Operaions'),
        ('publicity', 'Publicity'),
        ('ticketsales', 'Ticketsales'),
        ('spons', 'Sponsorship'),
        ('fr', 'Facilities & Requirements'),        
        ('design', 'Design'),
        ('hospi', 'Hospitality'),
        ('events', 'Events'),
        ('finance','Finance'), 
        ('security', 'Security'),
        ('proshows','Pro Shows'),

        ('adventurezone','Adventure Zone'),
        ('saarangdebate','Saarang Debate'),
        ('westernmusic','Western Music'),
        ('sudoku','Sudoku'),
        ('bigplan','Big Plan'),
        ('dramatics','Dramatics'),
        ('speakingevents','Speaking Events'),
        ('finearts','Fine Arts'),
        ('lightmusic','Light Music'),
        ('treasurehunt','Treasure Hunt'),
        ('choreo','Choreo'),
        ('crossie','Crossie'),
        ('scrabble','Scrabble'),
        ('wtgw','WTGW'),
        ('onlineanddailyquiz','Online + Daily Quiz'),
        ('buzzerquiz','Buzzer Quiz'),
        ('indiaquiz','India Quiz'),
        ('mainquiz','Main Quiz'),
        ('spentquiz','SpEnt Quiz'),
        ('travelandlivingquiz','Travel and Living Quiz'),
        ('creativewriting','Creative Writing'),
        ('streets','$treet$'),
        ('lecdems','LecDems'),
        ('workshops','Workshops'),
        ('spellingbee','Spelling Bee'),
        ('classicalarts','Classical Arts'),
        ('cluedo','Cluedo'),
        ('carnival','Carnival'),
        ('roadshows','Road Shows'),
        ('mediaevents','Media Events'),
        ('potpourrie','PotPourrie'),
    )

HOSTELS = (
        ('mandak','Mandakini'),
        ('jam','Jamuna'),
        ('ganga','Ganga'),
        ('alak','Alakananda'),
        ('godav','Godavari'),
        ('saras','Saraswati'),
        ('naramad','Narmada'),
        ('tapti','Tapti'),
        ('brahms','Brahmaputra'),
        ('cauvery','Cauvery'),
        ('krishna','Krishna'),
        ('mahanadhi','Mahanadhi'),
        ('pampa','Pampa'),
        ('sindhu','Sindhu'),
        ('tampi','Tamaraparani'),
        ('sharav','Sharavati'),
        ('sarayu','Sarayu'),
    )