"""Definition of the ATAreaProvvedimenti content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from comuneimola.compensi.interfaces.atareaprovvedimenti import IATAreaProvvedimenti
from comuneimola.compensi.config import PROJECTNAME
from comuneimola.compensi import compensiMessageFactory as _

ATAreaProvvedimentiSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    atapi.TextField(name='abstract',
        required=False,
        searchable=False,
        #primary=True,
        storage=atapi.AnnotationStorage(migrate=True),
        validators=('isTidyHtmlWithCleanup',),
        #default_content_type = 'text/restructured',
        default_output_type = 'text/x-html-safe',
        #allowable_content_types=('text/plain', 'text/restructured', 'text/html',),
        widget=atapi.RichWidget(
            label=_(u"abstract_label",default=u"Abstract"),
            description=_(u"abstract_description","An abstract of the provision area"),
            rows=15,
            allow_file_upload=False
        ),
    ),
    atapi.LinesField(name='tipo_provvedimento',
        widget=atapi.LinesWidget(
            label=_(u"type_of_provision",
                    default=u"Type of provision"),
            description=_(u"type_of_provision",
                          default=u"List here the type of provision"),
            ),
        required=False,
    ),
))

ATAreaProvvedimentiSchema['title'].storage = atapi.AnnotationStorage()
ATAreaProvvedimentiSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    ATAreaProvvedimentiSchema,
    folderish=True,
    moveDiscussion=False
)


class ATAreaProvvedimenti(folder.ATFolder):
    """Area Provvedimenti"""
    implements(IATAreaProvvedimenti)

    portal_type = "ATAreaProvvedimenti"
    meta_type = "ATAreaProvvedimenti"
    schema = ATAreaProvvedimentiSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

atapi.registerType(ATAreaProvvedimenti, PROJECTNAME)
