from django.conf import settings

from settings.config import Config

#
# MailGun API
#
MAILGUN_DOMAIN = Config.string('ZIMAGI_MAILGUN_DOMAIN')
MAILGUN_API_KEY = Config.string('ZIMAGI_MAILGUN_API_KEY')
