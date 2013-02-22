"""Definition of the ATAreaAnticorruzione content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from comuneimola.compensi.interfaces.atareaanticorruzione import IATAreaAnticorruzione
from comuneimola.compensi.config import PROJECTNAME
from comuneimola.compensi import compensiMessageFactory as _

ATAreaAnticorruzioneSchema = folder.ATFolderSchema.copy() + atapi.Schema((
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
            description=_(u"abstract_description","An abstract of the anticorruzione area"),
            rows=15,
            allow_file_upload=False
        ),
    ),
    atapi.LinesField(name='elenco_uffici',
        widget=atapi.LinesWidget(
            label=_(u"office_list",
                    default=u"Office List"),
            description=_(u"office_list_description",
                          default=u"List here offices for current area"),
            ),
        required=False,
    ),
    atapi.LinesField(name='publication_type_list',
        widget=atapi.LinesWidget(
            label=_(u"type_of_publication_list",
                    default=u"Type of publication list"),
            description=_(u"type_of_publication_list_description",
                          default=u"List here the type of publication you need"),
            ),
        required=False,
    ),
))

ATAreaAnticorruzioneSchema['title'].storage = atapi.AnnotationStorage()
ATAreaAnticorruzioneSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    ATAreaAnticorruzioneSchema,
    folderish=True,
    moveDiscussion=False
)


class ATAreaAnticorruzione(folder.ATFolder):
    """Area Anticorruzione"""
    implements(IATAreaAnticorruzione)

    portal_type = "ATAreaAnticorruzione"
    meta_type = "ATAreaAnticorruzione"
    schema = ATAreaAnticorruzioneSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

atapi.registerType(ATAreaAnticorruzione, PROJECTNAME)
