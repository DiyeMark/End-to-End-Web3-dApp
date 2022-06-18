from enum import Enum


class CertificateStatus(Enum):
    UNREQUESTED = 'unrequested'
    OPTED = 'opted'
    APPROVED = 'approved'
    DECLINED = 'declined'
