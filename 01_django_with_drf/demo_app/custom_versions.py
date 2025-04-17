from rest_framework.versioning import URLPathVersioning

class DefaultDemoVersion(URLPathVersioning):
    allowed_versions = ['v1']
    version_param = 'version'


class DemoViewVersion(DefaultDemoVersion):
    allowed_versions = ['v1', 'v2','v3']

class AnotherViewVersion(DefaultDemoVersion):
    allowed_versions = ['v1', 'v2']
