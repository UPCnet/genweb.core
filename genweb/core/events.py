# -*- coding: utf-8 -*-
from Products.CMFCore.interfaces import ISiteRoot
from upc.genwebupctheme.browser import utils
from upc.genwebupctheme.browser.interfaces import IgenWebControlPanelSchemaGeneral as gw_schema

def folderAdded(folder,event):
    if ISiteRoot.providedBy(folder.aq_parent):
        folder.context = folder.aq_parent
        gw_util = utils.getGWConfig(folder)
        folder.setConstrainTypesMode(1)
        folder.setLocallyAllowedTypes(tuple([i.value for i in gw_schema._v_attrs['constrains'].value_type.vocabulary.__iter__()]))
        folder.setImmediatelyAddableTypes(tuple(gw_util.constrains))
