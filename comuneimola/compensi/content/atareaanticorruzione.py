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

    atapi.LinesField(name='elenco_uffici',
        widget=atapi.LinesWidget(
            label=_(u"office_list",
                    default=u"Office List"),
            description=_(u"office_list_description",
                          default=u"List here offices for current area"),
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
