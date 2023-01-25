from django.conf import settings

class AppSettings(object):

    def __init__(self, prefix):
        self.prefix = prefix

    def _setting(self, name, default):
        return getattr(settings, self.prefix + name, default)

    @property
    def USE_SASS(self):
        """ Category choices for a support request ticket """
        return self._setting('USE_SASS', False)


app_settings = AppSettings('STYLIST_')