"""Definition of the ATProcedimento190 content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.Archetypes.utils import DisplayList
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from comuneimola.compensi.interfaces.atprocedimento190 import IATProcedimento190
from comuneimola.compensi.config import PROJECTNAME
from comuneimola.compensi import compensiMessageFactory as _

ATProcedimento190Schema = folder.ATFolderSchema.copy() + atapi.Schema((
    atapi.StringField('fiscal_data',
        required=True,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'fiscal_data_label', default=u'Tax code or VAT number'),
            description=_(u'fiscal_data_help', default=u"Insert the tax code or the VAT number"),
            size=60,
            ),
    ),

    atapi.StringField('office',
        required=True,
        vocabulary='officeVocab',
        widget=atapi.SelectionWidget(
            label=_(u'office_label', default=u'Office'),
            description=_(u'office_help', default=u"Select the office responsible"),
            ),
    ),

    atapi.StringField('responsible',
        required=True,
        widget=atapi.StringWidget(
            label=_(u'responsible_label', default=u'Charge of the procedure'),
            description=_(u'responsible_help', default=u"Specify the name of the charge of the procedure"),
            size=50,
            ),
    ),

    atapi.StringField('award_procedures',
        required=True,
        vocabulary='awardProceduresVocab',
        widget=atapi.SelectionWidget(
            label=_(u'award_procedures_label', default=u'Procedures for the award'),
            description=_(u'award_procedures_help', default=u"Select the award procedures"),
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

ATProcedimento190Schema['title'].widget.label = _(u'title_label', default=u'Name of the enterprise')
ATProcedimento190Schema['description'].widget.visible = False
ATProcedimento190Schema['effectiveDate'].widget.description = _(u'effectiveDate_help', default=u'If you set this date the item will be visible starting from this date. If you do not insert the date the item will be published immediately with the action of publication.')
ATProcedimento190Schema['effectiveDate'].widget.visible = {'edit': 'invisible', 'view': 'visible'}
ATProcedimento190Schema['expirationDate'].widget.visible = {'edit': 'invisible', 'view': 'visible'}

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.
ATProcedimento190Schema['title'].storage = atapi.AnnotationStorage()
ATProcedimento190Schema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    ATProcedimento190Schema,
    folderish=True,
    moveDiscussion=False
)


class ATProcedimento190(folder.ATFolder):
    """AT Procedimento 190"""
    implements(IATProcedimento190)

    portal_type = "ATProcedimento190"
    meta_type = "ATProcedimento190"
    schema = ATProcedimento190Schema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    def officeVocab(self):
        """ """
        offices = DisplayList()
        offices.add('', _(u'-- not specified --'))
        for office in self.aq_parent.getElenco_uffici():
            offices.add(office, office)
        return offices

    def awardProceduresVocab(self):
        """ """
        award_procedures = DisplayList()
        award_procedures.add('', _(u'-- not specified --'))
        for award_procedure in self.aq_parent.getModalita_affidamento():
            award_procedures.add(award_procedure, award_procedure)
        return award_procedures

    def amountTypeVocab(self):
        amountTypes = DisplayList()
        amountTypes.add('', _(u'-- not specified --'))
        for amountType in self.aq_parent.getNatura_importo():
            amountTypes.add(amountType, amountType)
        return amountTypes

    def normVocabulary(self):
        normTypes = DisplayList()
        normTypes.add('', _(u'-- not specified --'))
        for normType in self.aq_parent.getNorma_o_titolo():
            normTypes.add(normType, normType)
        normTypes.add('other', _(u'other'))
        return normTypes

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

atapi.registerType(ATProcedimento190, PROJECTNAME)
