# -*- coding: utf-8 -*-

import itertools
import json
import magic
import requests
import transaction

from bs4 import BeautifulSoup, element
from DateTime import DateTime
from five import grok
from plone import api
from plone.app.contenttypes.behaviors.richtext import IRichText
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.namedfile.file import NamedBlobFile, NamedBlobImage
from Products.CMFPlone.interfaces import IPloneSiteRoot
from urlparse import urljoin
from zope.component import getUtility


#
# HERRAMIENTA DE MIGRACIÓN HACIA GENWEB
#####################################################################
# A partir de un formato como el siguiente...
# {
#   "RECORDS":[
#     {
#       "id":3245,
#       "title":"19a  Edició del Premi Joan Roset i Ventosa",
#       "alias":"19a-edicio-del-premi-joan-roset-i-ventosa",
#       "contingut":"<p>Un any més, el CETIVG convoca el Premi JOAN ROSET I VENTOSA<\/p>\r\n \r\n<p>L&rsquo;objectiu d'aquest guardó de distingir el millor projecte d&rsquo;enginyeria d&rsquo;àmbit industrial. Està adreçat a tots els estudiants dels Graus en Enginyeries d&rsquo;àmbit Industrial, Grau en Enginyeria de Disseny Industrial i Desenvolupament del Producte que hagin defensat i superat el TFG durant els cursos 2016-2017 i el present curs, a l&rsquo;EPSEVG.<\/p>\r\n<p>El jurat tindrà en compte projectes que fomentin valors com&nbsp;la qualitat, la innovació, la sostenibilitat i la viabilitat tècnica i on, a més, es tinguin en compte aspectes que suposin una millora del medi ambient i la societat.&nbsp;<\/p>\r\n<div>L'autor o autora del projecte guanyador rebrà un any de col&middot;legiació gratuïta, un diploma de reconeixement i 1.000 euros. D'altra banda, el professor o professora que hagi realitzat la tutoria del projecte premiat rebrà també el corresponent diploma de reconeixement i un premi en metàl&middot;lic de 300 euros.&nbsp;<\/div>\r\n<div>&nbsp;<\/div>\r\n<div>La data límit per a presentar les candidatures és el 4 de maig 2018.<\/div>\r\n<div>&nbsp;<\/div>\r\n<div>Trobareu tota la informació, les bases i la butlleta d'inscripció, al següent <a href=\"http:\/\/www.cetivg.cat\/Canales\/Ficha.aspx?IdMenu=5cde343e-7879-44c7-bfdc-aea7991e72b8&amp;Cod=332937fa-8004-4694-9e20-852fbdb16e31&amp;Idioma=ca-ES\" target=\"_blank\">enllaç<\/a>.<\/div>\r\n<p>&nbsp;<\/p>",
#       "created":"2018\/3\/23 11:45:17",
#       "sectionid":9
#     },
#     {
#       "id":3244,
#       "title":"Convocatòria Mobilitat UPC-Xina curs 2018-2019",
#       "alias":"convocatoria-mobilitat-upc-xina-curs-2018-2019",
#       "contingut":"<p>S'ha obert la convocatòria per realitzar una estada de mobilitat acadèmica dins del programa UPC-Xina durant el curs 2018-2019<\/p>\r\n \r\n<p>El text de la convocatòria amb la descripció de les places, requisits i documentació a aportar es pot consultar a la <a href=\"https:\/\/www.upc.edu\/sri\/ca\/estudiantat\/mobilitat-estudiants\/mobilitat-destudiantat-de-la-upc\/estudiar-a-lestranger\/xina\/programa-de-mobilitat-academica-destudiants-upc-xina\/places-upc-de-mobilitat-academica-a-la-xina\" target=\"_blank\">web<\/a> del Gabinet de Relacions Internacionals de la UPC.<\/p>\r\n<p>El termini per presentar les sol&middot;licituds finalitza el proper 4 d'abril.<\/p>\r\n<p><img src=\"images\/stories\/comunicacio\/Noticies\/2017_2018\/cartell_1.jpg\" alt=\"cartell_1.jpg\" align=\"baseline\" width=\"300\" height=\"169\" \/><\/p>",
#       "created":"2018\/3\/23 11:14:31",
#       "sectionid":9
#     }
#   ]
# }
# ...la herramienta trata de generar artículos de noticias de Genweb.
#
# Dado que las propiedades de las noticias de Joomla y las de Genweb
# no son las mismas, se realizan las siguientes transformaciones:
#   id -> no hace falta
#   title -> title
#   alias -> short-name
#   contingut -> text (IRichText)
#   created -> creation_date
#   sectionid -> depende del valor, lo sitúa en una carpeta u otra
#     1 -> "Principal"
#     2 -> "Curs actual"

#
# PASOS A SEGUIR PARA MIGRAR CONTENIDOS
#####################################################################
#  1. Dentro del idioma catalán, y de la carpeta de 'Notícies', cread
#     MANUALMENTE la siguiente jerarquía de carpetas
#     - ca
#       - Notícies (noticies)
#         - Principal (principal)
#         - Curs actual (curs-actual)
#         - Annexos de notícies (annexos-de-noticies)
#           - Documents (documents)
#           - Imatges (imatges)
#
#  2. En la carpeta /tmp (atención, que la ruta es absoluta) debería
#     haber un archivo "migration.json" con los contenidos de Joomla,
#     siguiendo el siguiente formato:
#         {'RECORDS': [n1, n2, n3, ...]}
#     donde nj tiene el siguiente formato:
#         {       "id":                int,
#              "title":     unicode-string,
#              "alias": non-unicode-string,
#          "contingut":     unicode-string,
#            "created":        date-string,
#          "sectionid":                int}
#
#  3. Entrad en la siguiente ruta:
#       http://{base}/migrateEPSEVG
#     donde {base} puede ser, por ejemplo, www.epsevg.upc.edu
#
#  4. De las tres opciones que aparecen (cleanUp, runMigration,
#     checkLog), clicad en runMigration y esperad entre hora y media
#     y dos horas.
#
#  5. En consola va apareciendo en tiempo real el progreso de la
#     migración. En caso de que haya algún fallo, se ignora la
#     noticia que lo causa y se pasa a la siguiente.
#
#  6. Una vez acabada la migración, en el explorador web aparece en
#     texto plano un registro de todas las acciones con este formato:
#
#        Reading news...
#        250 news need to be migrated
#
#
#        1 of 250
#        title    : 19a  Edició del Premi Joan Roset i Ventosa
#        alias    : 19a-edicio-del-premi-joan-roset-i-ventosa
#        section  : Curs Actual
#        creation : 2018-03-23 11:45:17
#
#
#
#
#        2 of 250
#        title    : Convocatòria Mobilitat UPC-Xina curs 2018-2019
#        alias    : convocatoria-mobilitat-upc-xina-curs-2018-2019
#        section  : Curs Actual
#        creation : 2018-03-23 11:14:31
#
#          INFO   : internal link found
#                 :   -> {URL interno a documento}
#                 :   file downloaded successfully!
#                 :     -> imatges/cartell_1.jpg
#
#        ...
#
#        Quins enllaços tenen les següents noticies?
#        {
#            "principal": {
#                "{alias-noticia}": [
#                    "{ruta-relativa-a-archivo}"
#                ],
#                ...
#            },
#            "curs-actual": {
#                "{alias-noticia}": [
#                    "{ruta-relativa-a-archivo}"
#                ],
#                ...
#            }
#        }
#
#        Quines noticies referencien els següents enllaços?
#        {
#            "{ruta-relativa-a-archivo}": {
#                "principal": [
#                    "{alias-noticia}",
#                    ...
#                ],
#                "curs-actual": [
#                    "{alias-noticia}",
#                    ...
#                ]
#            },
#            ...
#        }
#
#        Done!
#
#
#  7. Este log se puede comprobar clicando en checkLog, o accediendo
#     a /tmp/migration.log
#     Cabe decir que en caso de error, aparecerá la razón bajo el
#     título ERROR, de la misma manera que los no errores aparecen
#     bajo el título INFO.
#
#  8. En caso de querer eliminar todo lo generado para volver a
#     iniciar el proceso, clicad en cleanUp.

#
# PREVIO AL FUNCIONAMIENTO
#####################################################################
#  - "contingut" está escrito en formato HTML, con enlaces e imágenes
#  - Además, contiene nodos de <script> y <style>, que deberían ser
#    ignorados.
#  - Estos enlaces e imágenes contienen rutas, que pueden ser:
#    - Internas o externas
#    - Imágenes o documentos (separación a petición del cliente)
#  - Los enlaces externos no presentan ningún problema, son los
#    internos, ya que si se trata de una migración, es porque TODOS
#    los contenidos se acabarán borrando en un futuro. Es por ello
#    que hace falta controlar qué enlaces internos se están usando
#    desde el noticiario, para así descargar los archivos y prevenir
#    su eliminacion permanente.

#
# CÓMO FUNCIONA?
#####################################################################
#  -  Lee tantas noticias en /tmp/migration.json como las hay
#     especificadas en newsLimit y, para cada una...
#  1. Se parsea el código HTML de cada noticia y, en caso de
#     encontrar un enlace interno, se reemplaza por una ruta relativa
#     siguiendo el siguiente proceso:
#    - Se comprueba si existe un dominio en la ruta. Si no, es enlace
#      interno. Si sí, se comprueba que el dominio sea
#      www.epsevg.upc.edu.
#    - En caso de que sea enlace interno, se descarga el fichero y
#      se crea un contenido Dexterity de tipo File o Image a partir
#      de él, ubicándolo según indique el mime-type del archivo.
#    - En la noticia, se cambia la ruta interna por una ruta relativa
#      al nuevo archivo creado.
#    - Como se puede dar el caso de que muchas noticias usen el mismo
#      recurso, se guarda una lista de los enlaces internos que han
#      sido tratados y, antes de tratar el enlace actual, se
#      comprueba si está en la lista, reutilizando la ruta relativa
#      en caso afirmativo.
#  2. Se crea un contenido Dexterity de tipo News Item, con contenido
#     el código fuente ya tratado y con atributos principales los que
#     aparecen en el JSON original.
#  3. Se crea una entrada en el log, informando de todas las acciones
#     y decisiones tomadas e informando en caso de error.


class migrateEPSEVG(grok.View):
    grok.context(IPloneSiteRoot)
    grok.name('migrateEPSEVG')
    grok.require('cmf.ManagePortal')

    treatedLinks = {}
    linksInSpecNews = {}
    newsWithSpecLink = {}
    newsAlias = ''
    logPath = ''
    portal = None
    portalCatalog = None
    logFileHandler = None
    normalizer = None

    imgTypes = ['jpg', 'jpeg', 'gif', 'png']
    docTypes = ['doc', 'docx', 'pdf']

    newsLimit = -1
    basePath = '/EPSEVG'
    newsBasePath = '/ca/noticies'
    newsFilePath = '/annexos-de-noticies'

    def isInternal(self, link):
        surelyNotInternal = [
            'mailto',
            'file'
        ]
        for prefix in surelyNotInternal:
            if link.startswith(prefix):
                return False

        surelyInternal = [
            'http://www.epsevg.upc.edu',
            'https://www.epsevg.upc.edu',
            'http://epsevg.upc.edu',
            'https://epsevg.upc.edu'
        ]
        for prefix in surelyInternal:
            if link.startswith(prefix):
                return True

        mostLikelyNotInternal = [
            'http:',
            'https:',
        ]
        for prefix in mostLikelyNotInternal:
            if link.startswith(prefix):
                return False

        mostLikelyInternal = [
            '/',
            'index',
            'images',
            'files',
            'imatges',
            'curs-actual',
            'docs',
            'estudis-epsevg',
        ]
        for prefix in mostLikelyInternal:
            if link.startswith(prefix):
                return True

        return False

    def solveLink(self, link):
        return urljoin('https://www.epsevg.upc.edu/', link)

    def shouldDownload(self, link):
        for suffix in itertools.chain(self.imgTypes, self.docTypes):
            if link.lower().endswith(suffix):
                return True
        return False

    def splitFilePathInfo(self, link):
        fileType = link.split('.')[-1].lower()
        filePath = '/'
        if fileType in self.imgTypes:
            filePath += 'imatges/'
        elif fileType in self.docTypes:
            filePath += 'documents/'

        fileName = self.normalizer.normalize(link.split('/')[-1].split('.')[:-1])

        if fileName[0] == '_':
            fileName = 'x' + fileName

        return [filePath, fileName, fileType]

    def getFirstNonOccupiedPath(self, preNameList, postNameList, **kwargs):
        copyNum = 0
        copyStr = ''
        first = True
        results = []
        while len(results) or first:
            if first:
                first = False
            else:
                copyNum += 1
                copyStr = '-' + str(copyNum)
            results = self.portalCatalog.unrestrictedSearchResults(
                           path=''.join(itertools.chain(preNameList, [copyStr], postNameList)),
                           **kwargs)
        return copyStr

    def downloadFile(self, link, innerDest):
        try:
            fileData = requests.get(link, stream=True, timeout=15).raw.read()
        except Exception as e:
            self.info['err'].append('  file not downloaded! (maybe link is broken?)')
            self.info['err'].append('    -> ' + str(e))
            return link

        filePathType = innerDest.split('/')[-2]
        fileId = innerDest.split('/')[-1]
        fileName = link.split('/')[-1]
        innerPortal = self.portal['annexos-de-noticies'][filePathType]


        namedBlob = {
            'data': fileData,
            'contentType': magic.Magic(mime=True).from_buffer(fileData),
            'filename': unicode(fileName)
        }

        if filePathType == 'imatges':
            innerPortal.invokeFactory('Image', id=fileId, title=fileName)
            innerPortal[fileId].image = NamedBlobImage(**namedBlob)
        elif filePathType == 'documents':
            innerPortal.invokeFactory('File', id=fileId, title=fileName)
            innerPortal[fileId].file = NamedBlobFile(**namedBlob)

        self.info['inf'].append('  file downloaded successfully!')
        self.info['inf'].append('    -> ' + filePathType + '/' + fileId)

        return '../annexos-de-noticies/' + filePathType + '/' + fileId

    def treatLink(self, link):
        if self.isInternal(link):
            link = self.solveLink(link)
            self.info['inf'].append('internal link found')
            self.info['inf'].append('  -> ' + link)
            if link in self.treatedLinks:
                self.info['inf'].append('  link already processed!')
            else:
                linkDest = link
                if self.shouldDownload(link):
                    filePathInfo = self.splitFilePathInfo(link)
                    preNameList = [self.basePath, self.newsBasePath, self.newsFilePath, filePathInfo[0], filePathInfo[1]]
                    postNameList = ['.', filePathInfo[2]]
                    innerDest = self.getFirstNonOccupiedPath(preNameList, postNameList)
                    linkDest = self.downloadFile(link, ''.join(
                                       itertools.chain(preNameList, [innerDest], postNameList)))
                else:
                    self.info['inf'].append('  not a file, will not attempt to download')

                self.treatedLinks.update({link: linkDest})
            link = self.treatedLinks[link]


            if not self.newsPath in self.linksInSpecNews:
                self.linksInSpecNews.update({self.newsPath: {}})
            if not self.newsAlias in self.linksInSpecNews[self.newsPath]:
                self.linksInSpecNews[self.newsPath].update({self.newsAlias: []})
            self.linksInSpecNews[self.newsPath][self.newsAlias].append(link)

            if not link in self.newsWithSpecLink:
                self.newsWithSpecLink.update({link: {}})
            if not self.newsPath in self.newsWithSpecLink[link]:
                self.newsWithSpecLink[link].update({self.newsPath: []})
            self.newsWithSpecLink[link][self.newsPath].append(self.newsAlias)

        return link

    def parseContent(self, content):
        for elm in content:
            if type(elm) is element.Tag:
                if elm.name in ['script', 'style']:
                    elm.extract()
                    self.info['inf'].append('removing \'%s\' node' % elm.name)
                elif elm.name in ['iframe', 'embed']:
                    pass
                else:
                    for attr in ['href', 'src']:
                        if elm.has_attr(attr):
                            elm[attr] = self.treatLink(elm[attr].encode('utf-8', 'ignore'))
                    self.parseContent(elm)

    def logPrint(self, txt):
        self.logFileHandler.write(txt + '\n')
        print(txt) # unica llamada a print en todo el codigo

    def logInfo(self):
        self.logPrint('\n')

        self.logPrint('%d of %d' % (self.info['cnt'], self.info['tot']))

        self.info['sec'] = {
            'principal': 'Principal',
            'curs-actual': 'Curs Actual'
        }.get(self.info['sec'], '---unknown---')

        self.logPrint('title    : %s' % self.info['ttl'])
        self.logPrint('alias    : %s' % self.info['ali'])
        self.logPrint('section  : %s' % self.info['sec'])
        self.logPrint('creation : %s' % self.info['cre'].strftime('%Y-%m-%d %H:%M:%S'))

        first = True
        for inf in self.info['inf']:
            if first:
                self.logPrint('')
            self.logPrint('  %s   : %s' % ('INFO' if first else '    ', inf))
            first = False

        first = True
        for err in self.info['err']:
            if first:
                self.logPrint('')
            self.logPrint('  %s  : %s' % ('ERROR' if first else '     ', err))
            first = False

        self.logPrint('\n')

    def cleanUp(self):
        for obj in self.portalCatalog.unrestrictedSearchResults(path=self.basePath+self.newsBasePath+'/principal/', portal_type='News Item') + \
                   self.portalCatalog.unrestrictedSearchResults(path=self.basePath+self.newsBasePath+'/curs-actual/', portal_type='News Item') + \
                   self.portalCatalog.unrestrictedSearchResults(path=self.basePath+self.newsBasePath+self.newsFilePath+'/imatges/', portal_type='Image') + \
                   self.portalCatalog.unrestrictedSearchResults(path=self.basePath+self.newsBasePath+self.newsFilePath+'/documents/', portal_type='File'):
            api.content.delete(obj=obj.getObject())
        return 'cleanup done!'

    def checkLog(self):
        with open(self.logPath, 'r') as self.logFileHandler:
            return '<pre>' + self.logFileHandler.read() + '</pre>'

    def runMigration(self):
        self.logFileHandler = open(self.logPath, 'wb')
        portalNoticies = self.portal
        self.normalizer = getUtility(IIDNormalizer)

        self.treatedLinks = {}
        self.linksInSpecNews = {}
        self.newsWithSpecLink = {}

        self.logPrint('Reading news...')

        jsonPath = '/tmp/migration.json'
        with open(jsonPath, 'r') as newsFile:
            newsList = json.loads(newsFile.read())['RECORDS']
        if self.newsLimit != -1:
            newsList = newsList[:self.newsLimit]

        self.logPrint('%d news need to be migrated' % len(newsList))

        for counter, news in enumerate(newsList):

            self.info = {
                'tot': len(newsList),
                'ttl': news['title'],
                'cnt': counter + 1,
                'err': [],
                'inf': []
            }

            if news['sectionid'] == 1:
                self.newsPath = 'principal'
            elif news['sectionid'] == 9:
                self.newsPath = 'curs-actual'

            self.newsAlias = self.normalizer.normalize(news['alias'])
            self.newsAlias += self.getFirstNonOccupiedPath(
                                   [self.basePath, self.newsPath, '/', self.newsAlias],
                                   [], portal_type='News Item')

            sourceCode = BeautifulSoup(news['contingut'].replace('\/', '/'), 'html.parser')

            try:
                self.parseContent(sourceCode)
            except Exception as e:
                self.info['err'].append('fatal error parsing the content')
                self.info['err'].append('   reason: ' + str(e))


            creationDate = DateTime(news['created'])
            try:
                portalNoticies[self.newsPath].invokeFactory(
                    type_name='News Item',
                    id=self.newsAlias,
                    title=news['title'],
                    text=IRichText['text'].fromUnicode(sourceCode)
                )
                portalNoticies[self.newsPath][self.newsAlias].creation_date = creationDate
                portalNoticies[self.newsPath][self.newsAlias].setModificationDate(creationDate)
                portalNoticies[self.newsPath][self.newsAlias].reindexObject(idxs=['created', 'modified'])
            except Exception as e:
                self.info['err'].append('fatal error creating the news object')
                self.info['err'].append('   reason: ' + str(e))

            self.info['cre'] = creationDate
            self.info['ali'] = self.newsAlias
            self.info['sec'] = self.newsPath
            self.logInfo()

            transaction.get().commit()

        self.logPrint('\n')

        self.logPrint('\n')
        self.logPrint('\n')
        self.logPrint('\n')
        self.logPrint('Quins enllaços tenen les següents noticies?')
        self.logPrint(json.dumps(self.linksInSpecNews, indent=4, sort_keys=True))
        self.logPrint('\n')
        self.logPrint('\n')
        self.logPrint('\n')
        self.logPrint('Quines noticies referencien els següents enllaços?')
        self.logPrint(json.dumps(self.newsWithSpecLink, indent=4, sort_keys=True))
        self.logPrint('\n')
        self.logPrint('\n')
        self.logPrint('\n')
        self.logPrint('Done!')
        self.logFileHandler.close()

        return self.checkLog()

    def render(self):
        self.portalCatalog = api.portal.get_tool('portal_catalog')
        self.portal = api.portal.get()['ca']['noticies']
        self.logPath = '/tmp/migration.log'

        if 'cleanUp' in self.request.form:
            return self.cleanUp()

        if 'checkLog' in self.request.form:
            return self.checkLog()

        if 'runMigration' in self.request.form:
            return self.runMigration()

        return 'usage: /migrateEPSEVG?[<b><a href="?cleanUp">cleanUp</a></b>|<b><a href="?checkLog">checkLog</a></b>|<b><a href="?runMigration">runMigration</a></b>]'