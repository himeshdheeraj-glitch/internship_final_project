from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    AGENT = "agent"
    SELLER = "seller"
    BUYER = "buyer"

class PropertyStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    SOLD = "sold"

class NotificationType(str, Enum):
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "danger"

JWT_SUBJECT_ACCESS = "access"
JWT_SUBJECT_REFRESH = "refresh"
