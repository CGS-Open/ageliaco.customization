# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
)
from plone.testing import z2

import ageliaco.customization


class AgeliacoCustomizationLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=ageliaco.customization)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "ageliaco.customization:default")


# SESAMATH_CUSTOMIZATION_FIXTURE = SesamathCustomizationLayer()
#
#
# SESAMATH_CUSTOMIZATION_INTEGRATION_TESTING = IntegrationTesting(
#     bases=(SESAMATH_CUSTOMIZATION_FIXTURE,),
#     name='SesamathCustomizationLayer:IntegrationTesting',
# )
#
#
# SESAMATH_CUSTOMIZATION_FUNCTIONAL_TESTING = FunctionalTesting(
#     bases=(SESAMATH_CUSTOMIZATION_FIXTURE,),
#     name='SesamathCustomizationLayer:FunctionalTesting',
# )
#
#
# SESAMATH_CUSTOMIZATION_ACCEPTANCE_TESTING = FunctionalTesting(
#     bases=(
#         SESAMATH_CUSTOMIZATION_FIXTURE,
#         REMOTE_LIBRARY_BUNDLE_FIXTURE,
#         z2.ZSERVER_FIXTURE,
#     ),
#     name='SesamathCustomizationLayer:AcceptanceTesting',
# )
