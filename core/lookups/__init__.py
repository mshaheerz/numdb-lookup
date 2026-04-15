from core.lookups.normal import NormalLookup
from core.lookups.truecaller import TruecallerLookup
from core.lookups.numverify import NumverifyLookup
from core.lookups.abstract_api import AbstractApiLookup
from core.lookups.veriphone import VeriphoneLookup
from core.lookups.ipqualityscore import IPQualityScoreLookup

LOOKUP_REGISTRY = [
    NormalLookup(),
    TruecallerLookup(),
    NumverifyLookup(),
    AbstractApiLookup(),
    VeriphoneLookup(),
    IPQualityScoreLookup(),
]


def get_all_lookups():
    return LOOKUP_REGISTRY
