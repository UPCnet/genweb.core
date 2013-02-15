from five import grok
from ZTUtils import make_query
from Acquisition import aq_inner

from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.uuid.interfaces import IUUID
from plone.app.layout.viewlets.interfaces import IAboveContent
from plone.app.i18n.locales.browser.selector import LanguageSelector
from zope.interface import Interface

from genweb.core.interfaces import IGenwebLayer
from genweb.core.interfaces import IHomePage
from genweb.core.utils import portal_url

import pkg_resources

try:
    pkg_resources.get_distribution('Products.LinguaPlone')
except pkg_resources.DistributionNotFound:
    HAS_LINGUAPLONE = False
    from genweb.core.interfaces import ITranslatable
else:
    HAS_LINGUAPLONE = True
    from Products.LinguaPlone.interfaces import ITranslatable


def addQuery(request, url, exclude=tuple(), **extras):
    """Adds the incoming GET query to the end of the url
    so that is propagated through the redirect hoops
    """
    formvariables = {}
    for k, v in request.form.items():
        if k not in exclude:
            if isinstance(v, unicode):
                formvariables[k] = v.encode('utf-8')
            else:
                formvariables[k] = v
    formvariables.update(extras)
    try:
        if len(formvariables) > 0:
            url += '?' + make_query(formvariables)
    # Again, LinguaPlone did this try/except here so I'm keeping it.
    except UnicodeError:
        pass
    return url


def getPostPath(context, request):
    """Finds the path to be added at the end of a context.

    This is useful because you might have a view or even something more long
    (form and widget traversing) at the very end of the absolute_url
    of a translated item.
    When you get the translated item absolute_url,
    you want to also have the eventual views etc ported over:
    this function does that.
    """
    # This is copied over from LinguaPlone
    # because there's a lot of knowledge embed in it.

    # We need to find the actual translatable content object. As an
    # optimization we assume it is within the last three segments.
    path = context.getPhysicalPath()
    path_info = request.get('PATH_INFO', '')
    match = [p for p in path[-3:] if p]
    current_path = [pi for pi in path_info.split('/') if pi]
    append_path = []
    stop = False
    while current_path and not stop:
        check = current_path.pop()
        if check == 'VirtualHostRoot' or check.startswith('_vh_'):
            # Once we hit a VHM marker, we should stop
            break
        if check not in match:
            append_path.insert(0, check)
        else:
            stop = True
    if append_path:
        append_path.insert(0, '')
    return "/".join(append_path)


class notConfigured(grok.Viewlet):
    grok.baseclass()

    def existObjectsNeeded(self):
        """Funcio que mira si existeixen els objectes que son necessaris pel bon funcionament del espai
           TODO: Fer que comprovi mes objectes, per ara nomes comprova la pagina principal en catala
        """
        context = aq_inner(self.context)
        return getattr(context, 'benvingut', False)

    def getSetupLink(self):
        """Funcio que dona l'enllas al formulari de creacio dels elements per defecte
        """
        return portal_url() + "/setup-view"


class notConfiguredForHomes(notConfigured):
    grok.viewletmanager(IAboveContent)
    grok.context(IHomePage)
    grok.template('notconfigured')
    grok.layer(IGenwebLayer)


class notConfiguredForRoots(notConfigured):
    grok.viewletmanager(IAboveContent)
    grok.context(IPloneSiteRoot)
    grok.template('notconfigured')
    grok.layer(IGenwebLayer)


class gwLanguageSelectorViewletManager(grok.ViewletManager):
    grok.context(Interface)
    grok.name('genweb.language_selector_manager')


class gwLanguageSelectorBase(LanguageSelector, grok.Viewlet):
    grok.baseclass()

    render = ViewPageTemplateFile('viewlets_templates/language_selector.pt')

    def get_selected_lang(self, languages):
        return [lang for lang in languages if lang['selected']][0]


class gwLanguageSelectorViewlet(gwLanguageSelectorBase):
    grok.context(ITranslatable)
    grok.viewletmanager(gwLanguageSelectorViewletManager)
    grok.layer(IGenwebLayer)

    def languages(self):
        languages_info = super(gwLanguageSelectorViewlet, self).languages()
        results = []

        uuid = IUUID(self.context)
        if uuid is None:
            uuid = 'nouuid'
        for lang_info in languages_info:
            # Avoid to modify the original language dict
            data = lang_info.copy()
            data['translated'] = True
            query_extras = {
                'set_language': data['code'],
            }
            post_path = getPostPath(self.context, self.request)
            if post_path:
                query_extras['post_path'] = post_path
            data['url'] = addQuery(
                self.request,
                self.context.absolute_url().rstrip("/") + \
                    "/@@goto/%s/%s" % (
                        uuid,
                        lang_info['code']
                    ),
                **query_extras
            )
            results.append(data)

        return results


class gwLanguageSelectorForRoot(gwLanguageSelectorBase):
    grok.context(IPloneSiteRoot)
    grok.viewletmanager(gwLanguageSelectorViewletManager)
    grok.layer(IGenwebLayer)

    def languages(self):
        languages_info = super(gwLanguageSelectorForRoot, self).languages()
        results = []

        for lang_info in languages_info:
            # Avoid to modify the original language dict
            data = lang_info.copy()
            data['translated'] = True
            query_extras = {
                'set_language': data['code'],
            }
            post_path = getPostPath(self.context, self.request)
            if post_path:
                query_extras['post_path'] = post_path
            data['url'] = addQuery(
                self.request,
                self.context.absolute_url(),
                **query_extras
            )
            results.append(data)

        return results
