from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string
from django.utils.encoding import force_str


class Mailer(object):

    def __init__(self, command, template_prefix, headers = None):
        self.command = command
        self.template_prefix = template_prefix
        self.headers = headers

        self.mailer = None
        self.email = None
        self.subject = ''
        self.text_message = ''
        self.html_message = ''


    def render(self, email, **context):
        self._render_mail(
            email,
            {
                "site_url": settings.ROOT_EMAIL_URL,
                "site_name": settings.EMAIL_SITE_NAME,
                "email": email,
                **context,
            }
        )


    def display(self):
        self.command.notice('Message')
        self.command.info('-' * self.command.display_width)
        self.command.info('-' * self.command.display_width)
        self.command.data('Email', self.email)
        self.command.data('Subject', self.subject)
        self.command.info('')

        if self.text_message:
            self.command.notice('Text message')
            self.command.info('-' * self.command.display_width)
            self.command.info(self.text_message)
            self.command.info('')

        if self.html_message:
            self.command.notice('HTML message')
            self.command.info('-' * self.command.display_width)
            self.command.info(self.html_message)
            self.command.info('')


    def send(self):
        self.mailer.send()


    def _format_email_subject(self, subject):
        prefix = settings.EMAIL_SUBJECT_PREFIX
        if prefix is None:
            prefix = "[{}] ".format(settings.EMAIL_SITE_NAME)
        return prefix + force_str(subject)


    def _render_mail(self, email, context):
        self.email = email

        subject = render_to_string("{}_subject.txt".format(self.template_prefix), context)
        subject = " ".join(subject.splitlines()).strip()
        self.subject = self._format_email_subject(subject)

        bodies = {}
        html_ext = 'html'
        for ext in [ html_ext, 'txt' ]:
            try:
                template_name = "{}_message.{}".format(self.template_prefix, ext)
                bodies[ext] = render_to_string(template_name, context).strip()
            except TemplateDoesNotExist:
                if ext == 'txt' and not bodies:
                    raise

        if 'txt' in bodies:
            self.text_message = bodies['txt']
            self.mailer = EmailMultiAlternatives(
                self.subject,
                self.text_message,
                settings.DEFAULT_FROM_EMAIL,
                [ self.email ],
                headers = self.headers
            )
            if html_ext in bodies:
                self.html_message = bodies[html_ext]
                self.mailer.attach_alternative(self.html_message, 'text/html')
        else:
            self.html_message = bodies[html_ext]
            self.mailer = EmailMessage(
                self.subject,
                self.html_message,
                settings.DEFAULT_FROM_EMAIL,
                [ self.email ],
                headers = self.headers
            )
            self.mailer.content_subtype = 'html'
