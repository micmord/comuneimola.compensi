"""Definition of the ATProvvedimento content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.Archetypes.utils import DisplayList
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from comuneimola.compensi.interfaces.atprovvedimento import IATProvvedimento
from comuneimola.compensi.config import PROJECTNAME
from comuneimola.compensi import compensiMessageFactory as _

ATProvvedimentoSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    atapi.StringField('provision',
        required=True,
        storage=atapi.AnnotationStorage(migrate=True),
        vocabulary='provisionVocabulary',
        widget=atapi.SelectionWidget(
            label=_(u'provision_label', default=u'Provision'),
            description=_(u'provision_help', default=u"Insert a short text to describe the provision."),
            ),
    ),
    atapi.StringField('other_provision',
        widget=atapi.StringWidget(
            label=_(u'other_provision_label', default=u'Other provision'),
            description=_(u'other_provision_help', default=u"If you select other in the previous field, write here the value (max 60 characters)"),
            maxlength=60,
            size=70,
            ),
    ),
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
            description=_(u"abstract_help","An abstract of the provision"),
            rows=15,
            allow_file_upload=False
        ),
    ),
       atapi.StringField('amount',
        required=False,
        validators=('isFloat'),
        widget=atapi.StringWidget(
            label=_(u'amount_label', default=u'Amount'),
            description=_(u'amount_help',
            default=u"Insert the amount of remuneration (the amount is meant in Euro, format X.YY)"),
            size=40,
            ),
    ),
    atapi.TextField('note',
        required=False,
        storage=atapi.AnnotationStorage(migrate=True),
        widget=atapi.TextAreaWidget(
            label=_(u'note_label', default=u'Note'),
            rows=4,
            maxlength=400,
            ),
    ),
))

ATProvvedimentoSchema['title'].widget.label = _(u'title_provision_label', default=u'Provision id')
ATProvvedimentoSchema['description'].widget.label = _(u'description_provision_label', default=u'Provision description')
ATProvvedimentoSchema['effectiveDate'].widget.description = _(u'effectiveDate_help', default=u'If you set this date the item will be visible starting from this date. If you do not insert the date the item will be published immediately with the action of publication.')
ATProvvedimentoSchema['effectiveDate'].widget.visible = {'edit': 'invisible', 'view': 'visible'}
ATProvvedimentoSchema['expirationDate'].widget.visible = {'edit': 'invisible', 'view': 'visible'}

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.
ATProvvedimentoSchema['title'].storage = atapi.AnnotationStorage()
ATProvvedimentoSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    ATProvvedimentoSchema,
    folderish=True,
    moveDiscussion=False
)


class ATProvvedimento(folder.ATFolder):
    """AT Provvedimento"""
    implements(IATProvvedimento)

    portal_type = "ATProvvedimento"
    meta_type = "ATProvvedimento"
    schema = ATProvvedimentoSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    def provisionVocabulary(self):
        provisionTypes = DisplayList()
        provisionTypes.add('', _(u'-- not specified --'))
        for provisionType in self.aq_parent.getTipi_provvedimento():
            provisionTypes.add(provisionType, provisionType)
        provisionTypes.add('other', _(u'other'))
        return provisionTypes

    def show_alert(self):
        """
        We need to be authenticated;
        In this folderish object no link should be present
        """
        links = self.listFolderContents({'portal_type': 'ATLinkCompenso'})
        isAnon = self.portal_membership.isAnonymousUser()
        if len(links) == 0 and not isAnon:
            return True
        return False

atapi.registerType(ATProvvedimento, PROJECTNAME)
