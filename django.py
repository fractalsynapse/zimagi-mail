from django.conf import settings

from settings.config import Config

#
# MailGun API
#
EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
ANYMAIL = {
    'MAILGUN_API_KEY': Config.string('ZIMAGI_MAILGUN_API_KEY'),
    'MAILGUN_SENDER_DOMAIN': Config.string('ZIMAGI_MAILGUN_DOMAIN', 'example.com'),
    'MAILGUN_API_URL': Config.string('ZIMAGI_MAILGUN_API_URL', 'https://api.mailgun.net/v3'),
}

#
# Email configurations
#
EMAIL_SITE_NAME = Config.string('ZIMAGI_EMAIL_SITE_NAME', 'Nexical Federal Contract Explorer')
ROOT_EMAIL_URL = Config.string('ZIMAGI_ROOT_EMAIL_URL', 'https://example.com')

DEFAULT_FROM_EMAIL = Config.string('ZIMAGI_DEFAULT_FROM_EMAIL', 'No Reply <noreply@example.com>')
EMAIL_SUBJECT_PREFIX = Config.string('ZIMAGI_EMAIL_SUBJECT_PREFIX', '')
