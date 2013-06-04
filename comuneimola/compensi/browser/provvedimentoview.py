from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from comuneimola.compensi.interfaces.atareacompensi import IMoneyFormat
from zope.component import getUtility


class IProvvedimentoView(Interface):
    """
    provvedimento view interface
    """

    def test():
        """ test method"""


class ProvvedimentoView(BrowserView):
    """
    provvedimento browser view
    """
    implements(IProvvedimentoView)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.mf = getUtility(IMoneyFormat)

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def get_money_format(self, value):
        """
        call the money format utility and convert the value
        """
        if value == "":
            return None
        return self.mf.moneyfmt(value)
