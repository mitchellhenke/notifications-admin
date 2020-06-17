import re

from notifications_utils.field import Field
from notifications_utils.formatters import formatted_list
from notifications_utils.recipients import (
    InvalidEmailError,
    validate_email_address,
)
from notifications_utils.sanitise_text import SanitiseSMS
from wtforms import ValidationError

from app.main._commonly_used_passwords import commonly_used_passwords
from app.utils import Spreadsheet, is_gov_user


class CommonlyUsedPassword:
    def __init__(self, message=None):
        if not message:
            message = 'Password is in list of commonly used passwords.'
        self.message = message

    def __call__(self, form, field):
        if field.data in commonly_used_passwords:
            raise ValidationError(self.message)


class CsvFileValidator:

    def __init__(self, message='Not a csv file'):
        self.message = message

    def __call__(self, form, field):
        if not Spreadsheet.can_handle(field.data.filename):
            raise ValidationError("{} is not a spreadsheet that Notify can read".format(field.data.filename))


class ValidGovEmail:

    def __call__(self, form, field):

        if field.data == '':
            return

        from flask import url_for
        message = '''
            Enter a public sector email address or
            <a class="govuk-link govuk-link--no-visited-state" href="{}">find out who can use Notify</a>
        '''.format(url_for('main.who_can_use_notify'))
        if not is_gov_user(field.data.lower()):
            raise ValidationError(message)


class ValidEmail:

    message = 'Enter a valid email address'

    def __call__(self, form, field):

        if field.data == '':
            return

        try:
            validate_email_address(field.data)
        except InvalidEmailError:
            raise ValidationError(self.message)


class NoCommasInPlaceHolders:

    def __init__(self, message='You cannot put commas between double brackets'):
        self.message = message

    def __call__(self, form, field):
        if ',' in ''.join(Field(field.data).placeholders):
            raise ValidationError(self.message)


class NoEmbeddedImagesInSVG:

    def __init__(self, message='This SVG has an embedded raster image in it and will not render well'):
        self.message = message

    def __call__(self, form, field):
        is_image_embedded = '<image' in field.data.stream.read().decode("utf-8")
        field.data.stream.seek(0)
        if is_image_embedded:
            raise ValidationError(self.message)


class OnlySMSCharacters:
    def __call__(self, form, field):
        non_sms_characters = sorted(list(SanitiseSMS.get_non_compatible_characters(field.data)))
        if non_sms_characters:
            raise ValidationError(
                'You cannot use {} in text messages. {} will not show up properly on everyone’s phones.'.format(
                    formatted_list(non_sms_characters, conjunction='or', before_each='', after_each=''),
                    ('It' if len(non_sms_characters) == 1 else 'They')
                )
            )


class LettersNumbersFullStopsAndUnderscoresOnly:

    regex = re.compile(r'^[a-zA-Z0-9\s\._]+$')

    def __init__(self, message='Use letters and numbers only'):
        self.message = message

    def __call__(self, form, field):
        if field.data and not re.match(self.regex, field.data):
            raise ValidationError(self.message)


class DoesNotStartWithDoubleZero:

    def __init__(self, message="Cannot start with 00"):
        self.message = message

    def __call__(self, form, field):
        if field.data and field.data.startswith("00"):
            raise ValidationError(self.message)


class MustContainAlphanumericCharacters:

    regex = re.compile(r".*[a-zA-Z0-9].*[a-zA-Z0-9].*")

    def __init__(
        self,
        message="Must include at least two alphanumeric characters"
    ):
        self.message = message

    def __call__(self, form, field):
        if field.data and not re.match(self.regex, field.data):
            raise ValidationError(self.message)
