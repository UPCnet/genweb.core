# -*- coding: utf-8 -*-
from Products.CMFCore.interfaces import ISiteRoot


IMMEDIATELY_ADDABLE_TYPES = ("Document", "Event", "File", "Folder", "Image",
                             "Link", "News Item", "Collection", "Collage",
                             "Window", "packet")
CONSTRAINED_TYPES = ('Document', 'Event', 'File', 'Folder', 'Image', 'Link',
                     'News Item', 'Collection', 'Collage', 'Survey',
                     'PlonePopoll', 'Ploneboard', 'simpleTask', 'Meeting',
                     'Window', 'FormFolder', 'packet')


def folderAdded(folder, event):
    # In case we are creating a new first level folder, apply constrains
    if ISiteRoot.providedBy(folder.aq_parent):
        folder.setConstrainTypesMode(1)
        folder.setLocallyAllowedTypes(CONSTRAINED_TYPES)
        folder.setImmediatelyAddableTypes(IMMEDIATELY_ADDABLE_TYPES)
