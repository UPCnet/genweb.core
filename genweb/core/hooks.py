# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from Products.CMFPlone.utils import safe_unicode

from cgi import escape
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from five import grok
from plone import api
from plone.app.workflow.events import ILocalrolesModifiedEvent

import socket


@grok.subscribe(IPloneSiteRoot, ILocalrolesModifiedEvent)
def addedPermissionsPloneSiteRoot(content, event):
    portal = api.portal.get()
    # sender_email = portal.getProperty('email_from_address')
    # sender_name = portal.getProperty('email_from_name').encode('utf-8')
    email_charset = portal.getProperty('email_charset')
    # fromMsg = sender_name + ' ' + '<' + sender_email + '>'
    fromMsg = 'Cristina Dantart <cristina.dantart@upc.edu>'

    serverid = socket.gethostname()
    mountpoint = '/'.join(content.getPhysicalPath())
    plone = content.absolute_url()

    # TODO Enviar correo para abrir tiquet
    context = aq_inner(content)
    mailhost = getToolByName(context, 'MailHost')
    msg = MIMEMultipart()
    msg['From'] = fromMsg
    msg['To'] = 'mailtoticket.genesis@upc.edu'
    msg['Subject'] = escape(safe_unicode('Recatalogar el genweb ' + plone))
    msg['charset'] = email_charset

    message = "Màquina: " + serverid + "\nMontpoint: " + mountpoint + "\nURL: " + plone

    msg.attach(MIMEText(message, 'plain', email_charset))
    mailhost.send(msg)
