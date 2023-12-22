from django.conf import settings

import requests


class Mailgun(object):

    def __init__(self, command):
        self.command = command

        self.auth = ('api', settings.MAILGUN_API_KEY)
        self.base_url = 'https://api.mailgun.net/v3/{}'.format(settings.MAILGUN_DOMAIN)


    def _post(self, path, data, files = None):
        return requests.post(
            "{}/{}".format(self.base_url, path),
            auth = self.auth,
            data = data,
            files = files
        )

    def _get(self, path, params = None):
        return requests.get(
            "{}/{}".format(self.base_url, path),
            auth = self.auth,
            params = params
        )


    def send(self, from_email, to_email, subject,
        text = None,
        html = None,
        cc_emails = None,
        bcc_emails = None,
        reply_to_email = None,
        headers = None,
        inlines = None,
        attachments = None,
        campaign_id = None,
        tags = None
    ):
        files = []
        data = {
            'from': from_email,
            'to': to_email,
            'cc': cc_emails or [],
            'bcc': bcc_emails or [],
            'subject': subject or '',
            'text': text or '',
            'html': html or ''
        }
        if headers:
            for key, value in headers.items():
                data["h:{}".format(key)] = value

        if reply_to_email:
            data['h:Reply-To'] = reply_to_email

        if campaign_id:
            data['o:campaign'] = campaign_id
        if tags:
            data['o:tag'] = tags

        if inlines:
            for filename in inlines:
                files.append(('inline', open(filename)))

        if attachments:
            for filename, content_type, content in attachments:
                files.append(('attachment', (filename, content, content_type)))

        response = self._post('messages', data, files = files)
        return True if response.status_code == 200 else False
