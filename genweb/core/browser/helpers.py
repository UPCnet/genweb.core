# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from App.config import getConfiguration
from Products.CMFPlone.interfaces import IPloneSiteRoot
from OFS.interfaces import IFolder
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from five import grok
from OFS.interfaces import IApplication
from zope.component import queryUtility
from plone.registry.interfaces import IRegistry
import json


DORSALS = {"1": "Víctor Valdés", "2": "Dani Alves", "3": "Piqué", "4": "Cesc", "5": "Puyol", "6": "Xavi", "7": "David Villa", "8": "A. Iniesta", "9": "Alexis", "10": "Messi", "11": "Thiago", "12": "Unknown", "13": "Pinto", "14": "Mascherano", "15": "Keita", "16": "Sergio", "17": "Pedro"}


def getDorsal():
    config = getConfiguration()
    configuration = config.product_config.get('genwebconfig', dict())
    zeo = configuration.get('zeo')
    return zeo


class getZEO(BrowserView):
    """ Funcio que agafa el numero de zeo al que esta assignat la instancia de genweb.
        Per aixo, el buildout s'ha d'afegir una linea a la zope-conf-additional:
        zope-conf-additional =
           <product-config genweb>
               zeo 9
           </product-config>
    """

    def dorsal(self):
        config = getConfiguration()
        configuration = config.product_config.get('genwebconfig', dict())
        zeo = configuration.get('zeo')
        return zeo

    def nomDorsal(self):
        return DORSALS[self.dorsal()]
