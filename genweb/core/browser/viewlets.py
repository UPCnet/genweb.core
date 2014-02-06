from five import grok
from urllib import quote
from ZTUtils import make_query

from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.uuid.interfaces import IUUID
from plone.app.i18n.locales.browser.selector import LanguageSelector
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName

from genweb.core import ITranslatable
from genweb.core.utils import genweb_config, havePermissionAtRoot
from genweb.core.interfaces import IGenwebLayer
from genweb.core import GenwebMessageFactory as _

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


class gwLanguageSelectorViewletManager(grok.ViewletManager):
    grok.context(Interface)
    grok.name('genweb.language_selector_manager')


class gwLanguageSelectorBase(LanguageSelector, grok.Viewlet):
    grok.baseclass()
    render = ViewPageTemplateFile('viewlets_templates/language_selector.pt')

    def get_selected_lang(self, languages):
        # Show all languages in language selector
        all_languages = super(gwLanguageSelectorBase, self).languages()
        
        if self.context.REQUEST.form.get('set_language'):
            idiomes_publicats = genweb_config().idiomes_publicats

        return [lang for lang in all_languages if lang['selected']][0]


    def lang_published(self):
        # show if the selected lang is published or not in language selector
        lang = dict(getToolByName(self, 'portal_languages').listAvailableLanguages())
        published_lang = genweb_config().idiomes_publicats
        params_lang = self.context.REQUEST.form.get('set_language')
        cookie_lang =  getToolByName(self, 'portal_languages').getPreferredLanguage()

        if params_lang:
            if params_lang not in lang:
                return _(u"not a valid language", default=u"${results} not a valid language", mapping={ u"results" : params_lang})
            if params_lang not in published_lang:
                return _(u"Not published")
        else:
            if cookie_lang not in published_lang:
                return _(u"Not published")


    def get_google_translated_langs(self):
        # return dict(ca=genweb_config().idiomes_google_translate_link_ca,
        #             en=genweb_config().idiomes_google_translate_link_en,
        #             es=genweb_config().idiomes_google_translate_link_es)
        return False

class gwLanguageSelectorViewlet(gwLanguageSelectorBase):
    grok.context(ITranslatable)
    grok.viewletmanager(gwLanguageSelectorViewletManager)
    #grok.layer(IGenwebLayer)

    def languages(self):

        languages_info = super(gwLanguageSelectorViewlet, self).languages()

        google_translated = self.get_google_translated_langs()
        idiomes_publicats = genweb_config().idiomes_publicats
        redirect_to_root = genweb_config().languages_link_to_root

        user_has_permission_at_root = havePermissionAtRoot()
        results = []

        uuid = IUUID(self.context)
        if uuid is None:
            uuid = 'nouuid'

        filtered_languages = [lang_info for lang_info in languages_info if user_has_permission_at_root or lang_info['code'] in idiomes_publicats]

        for lang_info in filtered_languages:
            # Avoid to modify the original language dict
            data = lang_info.copy()
            data['translated'] = True
            # if google_translated.get(data['code']):
            #     data['google_translated'] = True
            #     google_query_string = dict(sl=self.tool.getPreferredLanguage(),
            #                                tl=data['code'],
            #                                u=quote(self.context.absolute_url())
            #                                )

            #     data['url'] = 'http://translate.google.com/translate?hl={sl}&sl={sl}&tl={tl}&u={u}'.format(**google_query_string)
            # else:
            query_extras = {
                'set_language': data['code'],
            }
            if not redirect_to_root:
                post_path = getPostPath(self.context, self.request)
                if post_path:
                    query_extras['post_path'] = post_path

                data['url'] = addQuery(
                    self.request,
                    self.context.absolute_url().rstrip("/") +
                    "/@@goto/%s/%s" % (
                        uuid,
                        lang_info['code']
                    ),
                    **query_extras
                )
            else: # Redirect to root when make a language click
                data['url'] = self.portal_url() + '?set_language=' + data['code']

            results.append(data)

        return results


class gwLanguageSelectorForRoot(gwLanguageSelectorBase):
    # Show link to languages published in control panel
    grok.context(IPloneSiteRoot)
    grok.viewletmanager(gwLanguageSelectorViewletManager)
    #grok.layer(IGenwebLayer)

    def languages(self):
        languages_info = super(gwLanguageSelectorForRoot, self).languages()
        idiomes_publicats = genweb_config().idiomes_publicats
        redirect_to_root = genweb_config().languages_link_to_root

        user_has_permission_at_root = havePermissionAtRoot()
        results = []

        filtered_languages = [lang_info for lang_info in languages_info if user_has_permission_at_root or lang_info['code'] in idiomes_publicats]

        for lang_info in filtered_languages:
            # Avoid to modify the original language dict
            data = lang_info.copy()
            data['translated'] = True
            query_extras = {
                'set_language': data['code'],
            }
            if not redirect_to_root:
                post_path = getPostPath(self.context, self.request)
                if post_path:
                    query_extras['post_path'] = post_path
                data['url'] = addQuery(
                    self.request,
                    self.context.absolute_url(),
                    **query_extras
                )
            else: # Redirect to root when make a language click
                data['url'] = self.portal_url() + '?set_language=' + data['code']

            results.append(data)

        return results
