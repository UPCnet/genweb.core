Changelog
=========

4.4.4 (unreleased)
------------------

- Nothing changed yet.


4.4.3 (2014-09-16)
------------------

* Update dorsals for this season [Victor Fernandez de Alba]

4.4.2 (2014-09-09)
------------------

* Fix rare error compiling template. [Victor Fernandez de Alba]

4.4.1 (2014-09-05)
------------------

* Force p.a.robotframework into setup [Victor Fernandez de Alba]
* Order of field [Victor Fernandez de Alba]
* Extender into behavior, related tests [Victor Fernandez de Alba]
* Add open link in new folder behavior. [Victor Fernandez de Alba]

4.4.0 (2014-08-08)
------------------

* Update to pam 2.0 [Victor Fernandez de Alba]
* Try fix Travis 5 [Victor Fernandez de Alba]
* Try fix Travis 4 [Victor Fernandez de Alba]
* Try fix Travis 3 [Victor Fernandez de Alba]
* Try fix Travis 2 [Victor Fernandez de Alba]
* Try fix Travis [Victor Fernandez de Alba]
* Try to fix Travis [Victor Fernandez de Alba]
* Fix tests [Victor Fernandez de Alba]
* Install PAC and PAE by default on every Genweb site. Deprecate old language selector. [Victor Fernandez de Alba]
* [*** NON AT Genweb UPC ***] Updated to meet the new requirements agreed SC. From here, the Genweb core works with Dexterity CT by default. [Victor Fernandez de Alba]

4.3.29 (2014-07-24)
-------------------

* Merge [Victor Fernandez de Alba]
4.3.28 (2014-07-24)
-------------------

* List last login users [Victor Fernandez de Alba]

4.3.27 (2014-07-22)
-------------------

* Add missing dist files [Victor Fernandez de Alba]

4.3.26 (2014-07-21)
-------------------

* Sanitize the static resources for the whole Genweb project [Victor Fernandez de Alba]

4.3.25 (2014-07-15)
-------------------

* Add i18n strings for filtered_search_view and put more preference on permissions declarations [Victor Fernandez de Alba]
* New widget for searching in MAX user base directly. [Victor Fernandez de Alba]

4.3.24 (2014-07-08)
-------------------

* Change ldap externs url [Carles Bruguera]

4.3.23 (2014-07-07)
-------------------

* Fix deletion of Plone site from Zope root with a Protected content. [Victor Fernandez de Alba]
* Delete missing ipdb [Victor Fernandez de Alba]

4.3.22 (2014-06-12)
-------------------

* New profile for genweb.core with alternatheme [Victor Fernandez de Alba]
* Added alternatheme profile [Victor Fernandez de Alba]
* Added PAM global check [Victor Fernandez de Alba]

4.3.21 (2014-05-28)
-------------------

* User bulk creator for debug [Victor Fernandez de Alba]

4.3.20 (2014-05-27)
-------------------

* Merge branch 'develop' of github.com:UPCnet/genweb.core into develop [Victor Fernandez de Alba]
* Change permission schema with utils. [Victor Fernandez de Alba]
* traducciones [corina.riba]
* Traducción formulario contacto [corina.riba]

4.3.19 (2014-05-26)
-------------------

 * Add published languages feature to PAM LS [Victor Fernandez de Alba]

4.3.18 (2014-05-26)
-------------------

* Make home and subhome pages helpers. HAS_DXCT global helper too. [Victor Fernandez de Alba]
* Add new language selector viewlet and viewlet manager for PAM version, and make them conditionals [Victor Fernandez de Alba]

4.3.17 (2014-05-07)
-------------------

* Lowercase all user creations [Victor Fernandez de Alba]
* Update travis build and bootstrap [Victor Fernandez de Alba]
* New helper to detect development mode [Victor Fernandez de Alba]

4.3.16 (2014-04-08)
-------------------

* Add file widget translate [Victor Fernandez de Alba]

4.3.15 (2014-04-02)
-------------------

* added vocabulary to exclusion [Roberto Diaz]
* Add getVocabulary view if plone.app.widgets is not installed [Roberto Diaz]
* Fix permissions for keywords [Victor Fernandez de Alba]

4.3.14 (2014-03-31)
-------------------

* New tags widget for DX. [Victor Fernandez de Alba]
* Add new zope permission for webmasters [Victor Fernandez de Alba]

4.3.13 (2014-03-24)
-------------------

* AutoTokenizer [Victor Fernandez de Alba]

4.3.12 (2014-03-05)
-------------------

* Make p.a.c include conditional [Victor Fernandez de Alba]

4.3.11 (2014-03-04)
-------------------

* Update TinyMCE config [Victor Fernandez de Alba]
* Enable IImportant for DX types. [Victor Fernandez de Alba]
* Make tests work again even if there is no upc.genwebtheme for migration tests available. [Victor Fernandez de Alba]
* Make robot auto test run again [Victor Fernandez de Alba]

4.3.10 (2014-02-24)
-------------------

* Fix gitignore [Victor Fernandez de Alba]
* Un-dependency on p.a.contenttypes. [Victor Fernandez de Alba]
* Move some helpful methods into the g.core [Victor Fernandez de Alba]
* Merge branch 'develop' of github.com:UPCnet/genweb.core into rob [Victor Fernandez de Alba]
* Updated util method to use getSite and make it work for robot framework tests [Victor Fernandez de Alba]
* added share and top of page i18n [Roberto Diaz]
* Merge branch 'develop' of github.com:UPCnet/genweb.core into develop [Victor Fernandez de Alba]
* Change from includeDependencies to explicitly declare them for make robot tests pass [Victor Fernandez de Alba]
* add descr in ipdb line. useful in greps ;) [Roberto Diaz]
* solved bug trying to delete a previously created Plone Site [Roberto Diaz]
* added params i18n in language bar [Roberto Diaz]
* Solved: header language selector [Roberto Diaz]
* WIP header language selector [Victor Fernandez de Alba]
* Traducció nova vista [Corina Riba]
* corrected bug: error coding langs show/hidden in dropdown by cookie [Roberto Diaz]
* remove comments [Roberto Diaz]
* Modified template - Not Translated yet [Roberto Diaz]
* remove traces of GoogleTranslate [Roberto Diaz]
* if lang is not passed by url, but is innexistent and in a cookie [Roberto Diaz]
* solved error in lang selector if someone calls an inexistent or hidden lang [Roberto Diaz]
* Fix ldap setup views [Victor Fernandez de Alba]
* Final touches [Victor Fernandez de Alba]
* Merge branch 'develop' of github.com:UPCnet/genweb.core into develop [Victor Fernandez de Alba]
* Add setup helpers [Victor Fernandez de Alba]
* Disable from ControlPanel GoogleTranslate option [Roberto Diaz]
* added button translation [Roberto Diaz]
* update dorsals ;) [Roberto Diaz]
* added language option "link to root" in control panel [Roberto Diaz]

4.3.9 (2014-01-20)
------------------

* Merge branch 'develop' of github.com:UPCnet/genweb.core into develop [Corina Riba]
* Nuevo indice paralas imagenes de las noticias [Corina Riba]
* Add plone.api as dependency [Victor Fernandez de Alba]
* Bug LDAPUserFolder when searching on non standard attributes [Victor Fernandez de Alba]
* Index name field [Victor Fernandez de Alba]
* Indexar imagen news [Corina Riba]
* Merge branch 'develop' of github.com:UPCnet/genweb.core into develop [Corina Riba]
* Merge branch 'develop' of github.com:UPCnet/genweb.core into develop [Roberto Diaz]
* protected content message [Roberto Diaz]
* Improve conversor [Victor Fernandez de Alba]
* Put same policy of field search order. [Victor Fernandez de Alba]
* Patched mutable_properties for make it unicode normalization aware [Victor Fernandez de Alba]
* Merge branch 'develop' of github.com:UPCnet/genweb.core into develop [Corina Riba]
* New user select widget based on Select2.js [Victor Fernandez de Alba]
* Merge branch 'develop' of github.com:UPCnet/genweb.core into develop [Corina Riba]
* Traduccions [Corina Riba]
* New subscriber for prevent deletion of protected content [Victor Fernandez de Alba]
* New subscriber for prevent deletion of protected content [Victor Fernandez de Alba]
* Merge branch 'develop' of github.com:UPCnet/genweb.core into develop [Roberto Diaz]
* Show link to languages published in control panel [Roberto Diaz]
* Update dependencies on jarn.jsi18n [Victor Fernandez de Alba]
* Merge branch 'develop' of github.com:UPCnet/genweb.core into develop [Corina Riba]
* Cambio gestion "dades" cuando hay error [Corina Riba]
* i18n contacte [Roberto Diaz]
* Changed label for desactivate UPCmaps in contact form [Roberto Diaz]
* Add mailhost config [Victor Fernandez de Alba]

4.3.8 (2013-11-04)
------------------

* Add new translations [Victor Fernandez de Alba]

4.3.7 (2013-10-29)
------------------

 * Missing translations

4.3.6 (2013-10-29)
------------------

* Prevent role WebMaster to see the Root Folder link [Victor Fernandez de Alba]
* Literales "informacio contacte" y solucionar error directori si la UE no existe [Corina Riba]
* Get rid of getEdifici [Victor Fernandez de Alba]
* Eliminar traducciones duplicadas [Corina Riba]
* Merge de la 4.2 a develop de los últimos cambios [Corina Riba]
* getEdificiPeu [Corina Riba]
* Directori filtrado, cambio pie, pagina personalizada. Traducciones [Corina Riba]
* Cambio pie. Traducciones [Corina Riba]

4.3.5 (2013-10-01)
------------------

 * Traduccions [Corina Riba]
 * Update ignores [Carles Bruguera]
 * typo [Carles Bruguera]

4.3.4 (2013-09-19)
------------------

 * Fix for dexterity items in templates folders [Carles Bruguera]


4.3.3 (2013-08-02)
------------------

 * Traducciones [Corina Riba]
 * New helper view for balancer monitoring, order [Victor Fernandez de Alba]

4.3.2 (2013-07-25)
------------------

 * Remove shouter on TinyMCE template plugin [Victor Fernandez de Alba]
 * traducciones [Corina Riba]

4.3.1 (2013-07-11)
------------------

 * Traducciones [Corina Riba]
 * New i18n strings [Victor Fernandez de Alba]

4.3 (2013-06-10)
----------------

- First 4.3 (Plone 4.3 based) branch stable version

4.3b2 (unreleased)
------------------
- Un-grok the genweb.utils convenience view to BrowserView configured by ZCML,
  added the *allowed_interfaces* needed to access unrestricted to all the
  utilities methods.

4.3b1 (unreleased)
----------------
- New versioning number for the 2013 version of Genweb UPC: "rovelló de pi".
- New implementation from scratch, base of all the 2013 developments.
- Traspassada tota la funcionalitat del paquet upc.genwebupc
- Traspassats configuració genérica del profile del paquet upc.genwebupctheme

4.1.4 (2012-03-01)
------------------
- Permissos del root

4.1.3 (2011-12-19)
------------------
- Stripped tags al setuphandlers

4.1.2 (2011-12-12)
------------------
- Traduccions

4.1.1 (2011-11-30)
------------------
- Actualitzar nasty tags al setuphandlers

4.1 (2011-11-25)
----------------
- Actualització a Plone 4.

4.0b2 (dev)
-------------------
Nova versió del paquet, amb els viewlets updatats.
- Deprecat el viewlet de toolbar, updatant el de per defecte de Plone 4.
- Afegida l'acció d'usuari 'carpeta arrel'.
- Updatat el viewlet d'idiomes, utilitzant la estructura del original.
- Inclusió de la vista de utilitats genweb.utils per *.
- Desconfiguració dels viewlets per a configuració posterior.
- Update dels arxius .po i canvi al domini 'genweb'

4.0b1 (2010-11-10)
-------------------
- Ajustat les dependencies
- Eliminat el CKEditor
- Versió aplicada en Web UPCnet.

3.3dev (unreleased)
-------------------
- Initial release
