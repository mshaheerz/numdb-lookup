from core.lookups.normal import NormalLookup
from core.lookups.geocoding import GeocodingLookup
from core.lookups.truecaller import TruecallerLookup
from core.lookups.numverify import NumverifyLookup
from core.lookups.abstract_api import AbstractApiLookup
from core.lookups.veriphone import VeriphoneLookup
from core.lookups.ipqualityscore import IPQualityScoreLookup
from core.lookups.numlookupapi import NumLookupAPILookup
from core.lookups.telnyx import TelnyxLookup
from core.lookups.neutrino import NeutrinoLookup
from core.lookups.leakcheck import LeakCheckLookup
from core.lookups.cnam import CNAMLookup
from core.lookups.google_dork import GoogleDorkLookup
from core.lookups.social_media import SocialMediaLookup
from core.lookups.reputation import ReputationLookup
from core.lookups.web_presence import WebPresenceLookup
from core.lookups.ovh import OVHTelecomLookup
from core.lookups.disposable import DisposableLookup
from core.lookups.email_recovery import EmailRecoveryLookup
from core.lookups.enum_dns import ENUMLookup
from core.lookups.dnc_registry import DNCRegistryLookup

LOOKUP_REGISTRY = [
    # ── Offline / No API key ──
    NormalLookup(),
    GeocodingLookup(),

    # ── API-based lookups ──
    TruecallerLookup(),
    NumverifyLookup(),
    AbstractApiLookup(),
    VeriphoneLookup(),
    IPQualityScoreLookup(),
    NumLookupAPILookup(),
    TelnyxLookup(),
    NeutrinoLookup(),
    LeakCheckLookup(),
    CNAMLookup(),

    # ── OSINT (no API key) ──
    GoogleDorkLookup(),
    SocialMediaLookup(),
    ReputationLookup(),
    WebPresenceLookup(),

    # ── Advanced techniques (no API key) ──
    OVHTelecomLookup(),
    DisposableLookup(),
    EmailRecoveryLookup(),
    ENUMLookup(),
    DNCRegistryLookup(),
]


def get_all_lookups():
    return LOOKUP_REGISTRY
