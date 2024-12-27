class BaseConfig(object):
    ADMIN_EMAIL='test@maio.com'

class LiveConfig(BaseConfig):
    SITE_ADDRESS='https://site.com'

class TestConfig(BaseConfig):
    SITE_ADDRESS='https://testsite.com'

    