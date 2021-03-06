# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from plone.formwidget.recaptcha.widget import ReCaptchaFieldWidget
from plone.schema import email
from plone.app.users.schema import checkEmailAddress
from plone.z3cform.layout import wrap_form
from z3c.form import button
from z3c.form import field
from z3c.form import form
from zope import interface
from zope import schema
from zope.component import getMultiAdapter

from plone.api.portal import get_registry_record

import logging


logger = logging.getLogger(__name__)


class IReCaptchaForm(interface.Interface):
    name = schema.TextLine(
        title="Nom complet",
        description="Veuiller saisir votre nom complet.",
        required=True,
    )
    email = email.Email(
        title="Expéditeur",
        description="Veuiller saisir votre adresse email.",
        required=True,
        constraint=checkEmailAddress,
    )
    subject = schema.TextLine(title="Sujet", description="", required=True)
    message = schema.Text(title="Message", description="", required=False)
    captcha = schema.TextLine(title="ReCaptcha", description="", required=False)


class ReCaptcha(object):
    name = ""
    email = ""
    subject = ""
    message = ""
    captcha = ""

    def __init__(self, context):
        self.context = context


class BaseForm(form.Form):
    """example captcha form"""

    fields = field.Fields(IReCaptchaForm)
    fields["captcha"].widgetFactory = ReCaptchaFieldWidget

    @button.buttonAndHandler("Save")
    def handleApply(self, action):
        data, errors = self.extractData()
        captcha = getMultiAdapter(
            (aq_inner(self.context), self.request), name="recaptcha"
        )
        logger.info(data)

        logger.info(str(captcha.verify()))

        if captcha.verify():
            logger.info("ReCaptcha validation passed.")

            mailhost = self.context.MailHost
            # dest_email = self.context.getProperty(
            #     "email_from_address"
            # )
            dest_email = get_registry_record('plone.email_from_address')
            send_email = get_registry_record('plone.email_from_address')

            # from_name = get_registry_record('plone.email_from_name')

            try:
                mailhost.send(
                    f"Message de {data['name']} ({data['email']}) : {data['message']}",
                    dest_email,
                    send_email,
                    data["subject"],
                )
                logger.info("Message emailed.")
            except Exception:
                logger.error(
                    f"SMTP exception while trying to send an email to {dest_email}"
                )
        else:
            logger.info("The code you entered was wrong, please enter the new one.")
            return


ReCaptchaForm = wrap_form(BaseForm)
