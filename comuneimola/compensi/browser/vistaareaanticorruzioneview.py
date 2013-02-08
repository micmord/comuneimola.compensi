from zope.interface import implements, Interface
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility


class IVistaareaanticorruzioneView(Interface):
    """
    vistaareaanticorruzione view interface
    """

    def contenuti_folder():
        """ test method"""

    def show_export_button():
        """ policy to decide how can see the button"""


class vistaareaanticorruzioneView(BrowserView):
    """
    vistaareaanticorruzione browser view
    """
    implements(IVistaareaanticorruzioneView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    def contenuti_folder(self):
        path = '/'.join(self.context.getPhysicalPath())
        query = {'path': {'query': path, 'depth': 1}}
        brains = self.portal_catalog(**query)
        return brains

    def show_export_button(self):
        """
        Right now, everybody can see it
        """
        return True
