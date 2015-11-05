Changelog
=========

4.7.15 (2015-11-05)
-------------------

* Merge branch 'develop' of github.com:UPCnet/genweb.core into develop [Victor Fernandez de Alba]
* Fix getToolByName self object [Victor Fernandez de Alba]
* Translate navigation events portlet [hanirok]
* New pluggable changeMemberPortrait [Victor Fernandez de Alba]
* Translate new events portlet [hanirok]
* Tests for new portlet [Victor Fernandez de Alba]
* Add helper for detect write on reads [Victor Fernandez de Alba]
* Fix HISTORY [Victor Fernandez de Alba]

4.7.14 (2015-10-21)
-------------------

* Hide in the function the import of the new CSRF helper [Victor Fernandez de Alba]
* New registry setting for apply default languages [Victor Fernandez de Alba]
* Add cache helper [Victor Fernandez de Alba]

4.7.13 (2015-10-01)
-------------------

* add helper to remove duplicate genweb settings [Paco Gregori]
* Bullet proof provideAdapter by refactor it to grok like [Victor Fernandez de Alba]
* Bullet proof testing boilerplate [Victor Fernandez de Alba]

4.7.12 (2015-09-29)
-------------------

* afegeix propietats fila i cel·la a taula [Alberto Duran]
* Solucionat no hi ha dades al contacte [Alberto Duran]
* Merge branch 'develop' of github.com:UPCnet/genweb.core into develop [Victor Fernandez de Alba]
* Fix subjects select2 vocabulary helper view for include as id the title as well. [Victor Fernandez de Alba]
* Message contact message sent [hanirok]
* revert title patch [helena orihuela]

4.7.11 (2015-09-18)
-------------------

* Method to remove a user entry from soup [Carles Bruguera]
* title fixed [helena orihuela]

4.7.10 (2015-09-15)
-------------------

* Rebuild .mo


4.7.9 (2015-09-15)
------------------

* Rebuild always catalog with unicode strings [Carles Bruguera]

4.7.8 (2015-09-14)
------------------

* when add user to catalog, change username to lower [Paco Gregori]
* Merge branch 'develop' of github.com:UPCnet/genweb.core into develop [hanirok]
* Translate contact recipient [hanirok]

4.7.7 (2015-09-10)
------------------

* Traduccions [Pilar Marinas]

4.7.6 (2015-09-09)
------------------

* Merge branch 'develop' of github.com:UPCnet/genweb.core into develop [Victor Fernandez de Alba]
* New patch for normalize LDAP usernames to lowercase. This completes the normalization of the full system. [Victor Fernandez de Alba]

4.7.5 (2015-09-08)
------------------

* Fix tests [Victor Fernandez de Alba]
* Merge branch 'develop' of github.com:UPCnet/genweb.core into develop [Victor Fernandez de Alba]
* Re-refactor for not have to include template in CSS and JS resource viewlets [Victor Fernandez de Alba]
* Traducciones repeticion eventos [Pilar Marinas]
* Fix typo with resources viewlet [Victor Fernandez de Alba]
* New resource viewlet base class [Victor Fernandez de Alba]

4.7.4 (2015-09-04)
------------------

* Unify add_user_to_catalog to utils module. [Carles Bruguera]
* Comments in descending order by date [helena orihuela]
* Add tests for viewlets [Victor Fernandez de Alba]
* Adapt to new package genweb.cdn [Victor Fernandez de Alba]
* Traduccions [Pilar Marinas]

4.7.3 (2015-07-30)
------------------

* Merge branch 'develop' of github.com:UPCnet/genweb.core into develop [Victor Fernandez de Alba]

4.7.2 (2015-07-30)
------------------

* Fix cache [Victor Fernandez de Alba]
* Fix templates [Victor Fernandez de Alba]

4.7.1 (2015-07-29)
------------------

* Added helper to update the tiny templates [Victor Fernandez de Alba]

4.7 (2015-07-28)
----------------

* Merge branch 'develop' of github.com:UPCnet/genweb.core into develop [hanirok]
* Translate pasat [hanirok]
* Improve boilerplate for genweb.core [Victor Fernandez de Alba]
* Cambio literales Pestanyes [hanirok]
* Translation warning message and add new template [hanirok]

4.9 (2015-07-24)
----------------

* Traducccions [Pilar Marinas]
* New template Pestanyes [hanirok]
* Canvi plantilla Pestanyes [hanirok]

4.8 (2015-07-14)
----------------

* Traduccions [Pilar Marinas]
* Tranlations Allow discussion [Pilar Marinas]
* New helper views for touch instances [Victor Fernandez de Alba]
* fixed bug to add user+extended with API [Paco Gregori]
* Update i18n [Victor Fernandez de Alba]

4.7 (2015-06-25)
----------------

* Re-released under the new "minor" version.


4.6.4 (2015-06-25)
------------------

* genweb.js in place and css and js viewlets. Transferred components to genweb.js [Victor Fernandez de Alba]
* Add the new environment var for setting the purge cache server and new doral assignation [Victor Fernandez de Alba]
* Add support for custom icon list on TinyMCE. [Victor Fernandez de Alba]
* Translations Contents index view [hanirok]

4.6.3 (2015-06-17)
------------------

* Translate portlets [hanirok]
* Translate leadimage [Pilar Marinas]
* Tranlate objectius [hanirok]
* Add icon_blank in genwebtheme_custom [Pilar Marinas]
* Guard for attribute [Victor Fernandez de Alba]

4.6.2 (2015-06-10)
------------------

* Move out ldap group search code [Carles Bruguera]
* Add user to catalog [Pilar Marinas]
* Improve the method of acquiring the current (if enabled) user properties extender, and make the default property backend (IPropertiesPlugin) the more preferent one. [Victor Fernandez de Alba]

4.6.1 (2015-05-27)
------------------

* Disable right column in DX add forms [Victor Fernandez de Alba]
* Edit form right-portlet-less [Victor Fernandez de Alba]

4.6 (2015-05-18)
----------------

* Translation view name [hanirok]
* RAtionalize IGWUUID [Victor Fernandez de Alba]
* PEP8 [Victor Fernandez de Alba]
* Adding p.a.lockingbehavior [Victor Fernandez de Alba]
* Un-grok IGWUUID [Victor Fernandez de Alba]
* Ungrok IGWUUID adapter [Victor Fernandez de Alba]
* New contents view translation [hanirok]
* Fix missing space on searchable_text index [Victor Fernandez de Alba]
* Better displaying properties on this helper view [Victor Fernandez de Alba]
* Updated [Victor Fernandez de Alba]
* Fix previous commint [Victor Fernandez de Alba]
* New catalog user viewer [Victor Fernandez de Alba]
* New generic view for directory views [Victor Fernandez de Alba]
* Updated for complete profile generic enough for not to override it [Victor Fernandez de Alba]
* Add new test for IFavorite [Victor Fernandez de Alba]
* Modify script name as it's so similar to 'instance' [Victor Fernandez de Alba]
* Install/uninstall pre-commit-hooks for code analysis. [Victor Fernandez de Alba]
* Implement notlegit mark for users created via a non subscriber means, e.g a test or ACL [Victor Fernandez de Alba]
* Complete changes in searching users when the user properties are extended [Victor Fernandez de Alba]
* Improve search function by allowing to search through all the fields by introducing the new joined searchable_text. [Victor Fernandez de Alba]
* Fix favorites remove in case the user we are removing is not really favorited [Victor Fernandez de Alba]
* New functional CSS grunt-powered viewlet [Victor Fernandez de Alba]
* New json_request decorator [Victor Fernandez de Alba]
* Documentation on indexes and its use [Victor Fernandez de Alba]
* Add json_response method to utils [Victor Fernandez de Alba]
* Update docs [Victor Fernandez de Alba]

4.5.8 (2015-04-13)
------------------

* translate label back to previous page [Paco Gregori]
* Translate label back to previous page [Paco Gregori]
* add subject and creator to searchableText [Paco Gregori]
* add subject and creator to searchableText [Paco Gregori]

4.5.7 (2015-03-31)
------------------

* Merge branch 'develop' of github.com:UPCnet/genweb.core into develop [hanirok]
*  [hanirok]
* Traducciones [hanirok]
* Traucción workflow objectius [hanirok]
* Fix tests [Victor Fernandez de Alba]
* Images for content samples [hanirok]

4.5.6 (2015-03-13)
------------------

* Re-Fix last [Victor Fernandez de Alba]

4.5.5 (2015-03-13)
------------------

* Fix error introduced due to the new local user catalog index [Victor Fernandez de Alba]
* Merge branch 'develop' of github.com:UPCnet/genweb.core into develop [hanirok]
* Translate ServeisTIC view [hanirok]

4.5.4 (2015-03-12)
------------------

* Updated for not directly depend on PAM [Victor Fernandez de Alba]

4.5.3 (2015-03-12)
------------------

* Removed hard dependency on p.a.m. [Victor Fernandez de Alba]

4.5.2 (2015-03-11)
------------------

* add missing reset user catalog view [Victor Fernandez de Alba]

4.5.1 (2015-03-11)
------------------

* Fix mixed dependency on mrs.max, transferred to ulearn.core [Victor Fernandez de Alba]

4.5.0 (2015-03-11)
------------------

* Update the new settings on LDAP plugins [Victor Fernandez de Alba]
* Improvements to the get_safe_member_by_id [Victor Fernandez de Alba]
* Optimizations and improvements on templates and getMemberById [Victor Fernandez de Alba]
* Groups LDAP internal catalog [Victor Fernandez de Alba]
* Update Omega13 user search view. [Victor Fernandez de Alba]
* Do user catalog on creation too (for the case the user creation does not modifythe user properties. [Victor Fernandez de Alba]
* New components, GWUUID [Victor Fernandez de Alba]
* Add angular dependencies [Victor Fernandez de Alba]
* Add angular dependencies [Victor Fernandez de Alba]
* traduccion portlet estatico [hanirok]

4.4.50 (2015-03-04)
-------------------
* Re-released.


4.4.49 (2015-03-04)
-------------------



4.4.48 (2015-03-04)
-------------------

* Merge branch 'develop' of github.com:UPCnet/genweb.core into develop [Roberto Diaz]
* added utf codification to py [Roberto Diaz]

4.4.48 (2015-03-04)
-------------------

* Merge branch 'develop' of github.com:UPCnet/genweb.core into develop [Roberto Diaz]
* sort order in Tiny Templates [Roberto Diaz]

4.4.48 (2015-03-04)
-------------------

* Change name static portlet [hanirok]
* TinyMCE. Quitar de style y tablestyle los valores por defecto [Paco Gregori]
* Translate static portlet [hanirok]
* Merge branch 'develop' of github.com:UPCnet/genweb.core into develop [Paco Gregori]
* modificación literal fitxers compartits [Paco Gregori]

4.4.47 (2015-02-18)
-------------------

* Conditional allow users [Carles Bruguera]

4.4.46 (2015-02-18)
-------------------

* Add a generic ldap creator [Carles Bruguera]

4.4.45 (2015-02-18)
-------------------

* Add missing transform [Victor Fernandez de Alba]
* Portlets translations [hanirok]

4.4.44 (2015-02-17)
-------------------

* cambios en tinymce (modificación de estilos) [Paco Gregori]
* traduccions dates event [Paco Gregori]

4.4.43 (2015-02-12)
-------------------

* Add more patches [Victor Fernandez de Alba]

4.4.42 (2015-02-12)
-------------------

* Add missing metadata (non-indexed) user properties and fix patches [Victor Fernandez de Alba]

4.4.41 (2015-02-12)
-------------------

* Update patches whitelisted callers [Victor Fernandez de Alba]

4.4.40 (2015-02-12)
-------------------

* Update patches whitelisted callers [Victor Fernandez de Alba]

4.4.39 (2015-02-12)
-------------------

* Fix use case when the user searched is not on the local catalog but in a caller whitelisted [Victor Fernandez de Alba]

4.4.38 (2015-02-11)
-------------------

* Ensure username is on lowercase always as we always assume that [Victor Fernandez de Alba]
* Fix procedure [Victor Fernandez de Alba]

4.4.37 (2015-02-11)
-------------------



4.4.36 (2015-02-11)
-------------------

* New util for preserving UUIDs and retrieve them back [Victor Fernandez de Alba]

4.4.35 (2015-02-10)
-------------------

* Fix unicodeerrors [Victor Fernandez de Alba]

4.4.34 (2015-02-10)
-------------------

* trad portlets [Paco Gregori]
* trad portlets [Paco Gregori]

4.4.33 (2015-02-06)
-------------------

* Add LRF to tinyMCE [Victor Fernandez de Alba]

4.4.32 (2015-02-06)
-------------------

* New directory repoze.catalog based user properties [Victor Fernandez de Alba]

4.4.31 (2015-02-05)
-------------------

* Increase reaction to keypress for select2user JS plugin [Victor Fernandez de Alba]
* Patch to make user PropertiesUpdated event work [Victor Fernandez de Alba]
* Translate portlets name [hanirok]
* Traduir No hi ha elements js cerca [Pilar Marinas]
* traducciones [Paco Gregori]

4.4.30 (2015-01-13)
-------------------

* Fix translations for homepage portlets [Victor Fernandez de Alba]

4.4.29 (2015-01-08)
-------------------

* Fixing Travis [Victor Fernandez de Alba]
* Fix Travis [Victor Fernandez de Alba]
* New utils for link translations [Victor Fernandez de Alba]
* Fixing travis [Victor Fernandez de Alba]

4.4.28 (2014-12-30)
-------------------

* info [Paco Gregori]
* traducciones [Paco Gregori]

4.4.27 (2014-12-16)
-------------------

* New permissions for special portlets [Victor Fernandez de Alba]

4.4.26 (2014-12-16)
-------------------

* New permissions for special portlets [Victor Fernandez de Alba]

4.4.25 (2014-12-16)
-------------------

* Bad version

4.4.24 (2014-12-16)
-------------------

* Preemptive retire c.indexing from buildout [Victor Fernandez de Alba]

4.4.23 (2014-12-15)
-------------------

* Add i18n for missing Plone translations [Victor Fernandez de Alba]

4.4.22 (2014-12-15)
-------------------

* Merge branch 'develop' of github.com:UPCnet/genweb.core into develop [Victor Fernandez de Alba]

4.4.21 (2014-12-15)
-------------------

* Make Wbmasters able to manage portlets [Victor Fernandez de Alba]
* Add pref_lang to utils view [Victor Fernandez de Alba]
* Missing console.log [Victor Fernandez de Alba]
* View about only for editors [hanirok]
* és traduccions [Paco Gregori]
* és traduccions [Paco Gregori]
* Traducciones [hanirok]
* Traducció xarxes socials [Paco Gregori]
* Traducciones. Ficheros .po [Paco Gregori]

4.4.20 (2014-12-03)
-------------------

* Disable the patch that patched the searchUsers fuction on LDAPMultiPlugin. [Victor Fernandez de Alba]
* Cambios en traducciones [Francisco Gregori]
* Translations [hanirok]
* News translations [hanirok]
* Translations [hanirok]
* Merge branch 'develop' of github.com:UPCnet/genweb.core into develop [hanirok]
* Translation news [hanirok]
* Fix test [Victor Fernandez de Alba]
* Moved to g.upc [Victor Fernandez de Alba]
* Update to Plone 4.3.4 [Victor Fernandez de Alba]
* Try to fix Travis [Victor Fernandez de Alba]

4.4.19 (2014-11-14)
-------------------

* Working language selector conditional behavior [Victor Fernandez de Alba]
* Footer translations [hanirok]

4.4.18 (2014-11-10)
-------------------

* Fix tiny templates preview [Victor Fernandez de Alba]
* Add syndication enabled by default [Victor Fernandez de Alba]
* Update linkable Tiny objects list [Victor Fernandez de Alba]
* Fix link behavior [Victor Fernandez de Alba]
* Add c.indexing to build [Victor Fernandez de Alba]
* Updated templates for Tiny [Victor Fernandez de Alba]
* Regain Tiny save button functionality [Victor Fernandez de Alba]
* Get contact data [hanirok]

4.4.17 (2014-10-22)
-------------------

* New helper for mirror UUIDs from one site to another (in the same zope instance) [Victor Fernandez de Alba]

4.4.16 (2014-10-16)
-------------------

* New templates, i18n [Victor Fernandez de Alba]

4.4.15 (2014-10-16)
-------------------

* Merge branch 'develop' of github.com:UPCnet/genweb.core into develop [Victor Fernandez de Alba]
* Update and modernize some parts. Awesomeness from Plone5 [Victor Fernandez de Alba]
* New helper for re-setting a branch language [Victor Fernandez de Alba]

4.4.14 (2014-10-15)
-------------------

* Ignore node modules [Carles Bruguera]
* Apply changes to minified version [Carles Bruguera]
* Add new detection in case LDAP UPC is configured, fridge to the portal_url banid [Victor Fernandez de Alba]
* Update LDAP username [Victor Fernandez de Alba]
* Add typeahead and handlebars [Carles Bruguera]
* Migration cleanup and i18n [Victor Fernandez de Alba]

4.4.13 (2014-10-09)
-------------------

* Update the BLACK_LIST_IDS for the inheriting elements. Make portal_url work again with our code [Victor Fernandez de Alba]

4.4.12 (2014-10-09)
-------------------

* Improved clouseau [Victor Fernandez de Alba]

4.4.11 (2014-10-08)
-------------------

* Merge branch 'develop' of github.com:UPCnet/genweb.core into develop [hanirok]
* Añadir poder marcar contenidos como importantes [hanirok]

4.4.10 (2014-10-07)
-------------------

* i18n [Victor Fernandez de Alba]
* Reinstall controlpanel helper finished [Victor Fernandez de Alba]
* Fix helper [Victor Fernandez de Alba]
* Helper for reinstall control panel in all Plone instances of a Zope [Victor Fernandez de Alba]
* Add dependency [Victor Fernandez de Alba]
* Upload new example images [Victor Fernandez de Alba]
* Fix versioning preview of the selected version. [Victor Fernandez de Alba]

4.4.9 (2014-10-06)
------------------

* Fix calendar [Victor Fernandez de Alba]
* Default language [Victor Fernandez de Alba]

4.4.8 (2014-09-30)
------------------

* Fix path of example images [Victor Fernandez de Alba]
* Fix protected content [Victor Fernandez de Alba]

4.4.7 (2014-09-29)
------------------

* New custom font for Genweb. Fix resizer.js. Added SEO optimizer. [Victor Fernandez de Alba]
* Override of the default sendto_form redirecting to NotFound [Victor Fernandez de Alba]
* Patch for fixing the wcfc error on deleting objects. [Victor Fernandez de Alba]
* Patch for fixing the wcfc error on deleting objects. [Victor Fernandez de Alba]
* Test for IProtectedContent [Victor Fernandez de Alba]

4.4.6 (2014-09-22)
------------------

* New i18n [Victor Fernandez de Alba]

4.4.5 (2014-09-22)
------------------

* New interfaces for the news and events folders [Victor Fernandez de Alba]
* Fix listing of available templates [Victor Fernandez de Alba]
* Erase some unused backported from PAM utilities and views. [Victor Fernandez de Alba]
* Search patch and i18n [Victor Fernandez de Alba]

4.4.4 (2014-09-17)
------------------

* Add i18n [Victor Fernandez de Alba]

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
------------------
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
-----------

Nova versió del paquet, amb els viewlets updatats:

- Deprecat el viewlet de toolbar, updatant el de per defecte de Plone 4.
- Afegida l'acció d'usuari 'carpeta arrel'.
- Updatat el viewlet d'idiomes, utilitzant la estructura del original.
- Inclusió de la vista de utilitats genweb.utils per a tothom.
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
