import unittest

from zope.component import getMultiAdapter

from Products.CMFCore.utils import getToolByName

from Products.PloneTestCase.ptc import PloneTestCase

from upc.genwebupc.tests.layer import Layer


class TestFixUIDs(PloneTestCase):

    layer = Layer

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.catalog = getToolByName(self.portal, 'portal_catalog')
        # Create content
        self.folder.invokeFactory('Document', 'doc', title='Document')
        self.doc = self.folder['doc']
        self.folder.invokeFactory('News Item', 'newsitem', title='News Item')
        self.newsitem = self.folder['newsitem']
        self.folder.invokeFactory('Event', 'event', title='Event')
        self.event = self.folder['event']
        # Create some link targets
        self.folder.invokeFactory('Document', 'linktarget1', title='Link Target 1')
        self.linktarget1 = self.folder['linktarget1']
        self.linktarget1_path = '/' + self.linktarget1.absolute_url(relative=True)
        self.linktarget1_uid = self.catalog.searchResults(path=self.linktarget1_path)[0].UID
        self.folder.invokeFactory('Document', 'linktarget2', title='Link Target 2')
        self.linktarget2 = self.folder['linktarget2']
        self.linktarget2_path = '/' + self.linktarget2.absolute_url(relative=True)
        self.linktarget2_uid = self.catalog.searchResults(path=self.linktarget2_path)[0].UID
        self.folder.invokeFactory('Document', 'linktarget3', title='Link Target 3')
        self.linktarget3 = self.folder['linktarget3']
        self.linktarget3_path = '/' + self.linktarget3.absolute_url(relative=True)
        self.linktarget3_uid = self.catalog.searchResults(path=self.linktarget3_path)[0].UID

    def testFixDocumentUIDsView(self):
        self.failUnless(self.doc.restrictedTraverse('@@fix-uids'))

    def testFixNewsItemUIDsView(self):
        self.failUnless(self.newsitem.restrictedTraverse('@@fix-uids'))

    def testFixEventUIDsView(self):
        self.failUnless(self.event.restrictedTraverse('@@fix-uids'))
    
    def testFixUIDsView(self):
        self.failUnless(self.portal.restrictedTraverse('@@fix-uids'))

    def testFixLinkUIDs(self):
        self.doc.setText('<a href="%s">pressupostos</a>' % self.linktarget1_path)
        self.doc.reindexObject()
        view = getMultiAdapter((self.doc, self.portal.REQUEST), name="fix-uids")
        view = view.__of__(self.doc)
        view()
        self.assertEquals(self.doc.getRawText(), 
                          '<a href="resolveuid/%s">pressupostos</a>' % self.linktarget1_uid)

    def testFixImgUIDs(self):
        self.doc.setText('<img src="%s" alt="image" />' % self.linktarget1_path)
        self.doc.reindexObject()
        view = getMultiAdapter((self.doc, self.portal.REQUEST), name="fix-uids")
        view = view.__of__(self.doc)
        view()
        self.assertEquals(self.doc.getRawText(), 
                          '<img src="resolveuid/%s" alt="image" />' % self.linktarget1_uid)

    def testDoNotFixExternalLinks(self):
        self.doc.setText('<a href="http://www.upc.edu">UPC</a>')
        self.doc.reindexObject()
        view = getMultiAdapter((self.doc, self.portal.REQUEST), name="fix-uids")
        view = view.__of__(self.doc)
        view()
        self.assertEquals(self.doc.getRawText(), '<a href="http://www.upc.edu">UPC</a>')

    def testDoNotFixExternalImgLinks(self):
        self.doc.setText('<img src="http://www.upc.edu/img.png" alt="image" />')
        self.doc.reindexObject()
        view = getMultiAdapter((self.doc, self.portal.REQUEST), name="fix-uids")
        view = view.__of__(self.doc)
        view()
        self.assertEquals(self.doc.getRawText(), '<img src="http://www.upc.edu/img.png" alt="image" />')      

    def testDoNotFixPloneLinks(self):
        self.doc.setText('<a href="@@mail-controlpanel">Mail Control Panel</a>')
        self.doc.reindexObject()
        view = getMultiAdapter((self.doc, self.portal.REQUEST), name="fix-uids")
        view = view.__of__(self.doc)
        view()
        self.assertEquals(self.doc.getRawText(), '<a href="@@mail-controlpanel">Mail Control Panel</a>')

    def testCheckExternatlLinks(self):
        self.doc.setText('<a href="http://www.upc.edu/logoPrint.gif">UPC</a>')
        self.doc.reindexObject()
        view = getMultiAdapter((self.doc, self.portal.REQUEST), name="fix-uids")
        view = view.__of__(self.doc)
        view()
        self.assertEquals(self.doc.getRawText(), '<a href="http://www.upc.edu/logoPrint.gif">UPC</a>')        
    
    def testFixUIDs(self):
        self.doc.setText('<p>Aquest punt inclou la informacio economica de la UPC. Per un costat hi trobareu els <a href="%s">pressupostos</a> des de lany 2004 i les <a href="%s">memòries</a> auditades de la UPC.</p><p>Per altra part, si us identifiqueu a la intranet<strong>,</strong>&nbsp;oferim informació relacionada amb les convocatòries dajuts, tant del Ministerio de educación y ciencia, de la Generalitat de Catalunya com de la UPC.</p><p>Tambe hi trobareu el <a href="%s">Pla destabilitzacio plurianual [pdf]</a>.</p>' \
                         % (self.linktarget1_path, self.linktarget2_path, self.linktarget3_path))
        self.doc.reindexObject()
        view = getMultiAdapter((self.doc, self.portal.REQUEST), name="fix-uids")
        view = view.__of__(self.doc)
        view()
        text = self.doc.getRawText()
        self.failIf(self.linktarget1_path in text)
        self.failIf(self.linktarget2_path in text)
        self.failIf(self.linktarget3_path in text)
        self.failUnless(self.linktarget1_uid in text)
        self.failUnless(self.linktarget2_uid in text)
        self.failUnless(self.linktarget3_uid in text)

    def testFixAllUIDs(self):
        text = '<a href="%s">pressupostos</a>' % self.linktarget1_path
        self.doc.setText(text)
        self.newsitem.setText(text)
        self.event.setText(text)
        self.doc.reindexObject()
        self.newsitem.reindexObject()
        self.event.reindexObject()
        view = getMultiAdapter((self.portal, self.portal.REQUEST), name="fix-all-uids")
        view = view.__of__(self.portal)
        view()
        self.failIf(self.linktarget1_path in self.doc.getText())
        self.failIf(self.linktarget1_path in self.newsitem.getText())
        self.failIf(self.linktarget1_path in self.event.getText())
        self.failUnless(self.linktarget1_uid in self.doc.getText())
        self.failUnless(self.linktarget1_uid in self.newsitem.getText())
        self.failUnless(self.linktarget1_uid in self.event.getText())
        
def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)