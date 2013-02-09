from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from zope.component import getUtility


class IVistaprocedimenti190View(Interface):
    """
    vista procedimenti190 view interface
    """

    def test():
        """ test method"""


class vistaprocedimento190View(BrowserView):
    """
    vistaprocedimento190 browser view
    """
    implements(IVistaprocedimenti190View)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()
