import enum

class UserRole(str, enum.Enum):
    CUSTOMER = 'CUSTOMER'
    SALE = 'SALE'
    COORDINATOR = 'COORDINATOR'
    ADMIN = 'ADMIN'

class UserStatus(str, enum.Enum):
    ACTIVE = 'ACTIVE'
    LOCKED = 'LOCKED'
    DISABLED = 'DISABLED'

class PropertyKind(str, enum.Enum):
    LAND = 'LAND'
    APARTMENT = 'APARTMENT'
    HOUSE = 'HOUSE'
    VILLA = 'VILLA'
    TOWNHOUSE = 'TOWNHOUSE'
    COMMERCIAL = 'COMMERCIAL'

class PropertyStatus(str, enum.Enum):
    DRAFT = 'DRAFT'
    AVAILABLE = 'AVAILABLE'
    UNDER_OFFER = 'UNDER_OFFER'
    SOLD = 'SOLD'
    HIDDEN = 'HIDDEN'
    MAINTENANCE = 'MAINTENANCE'

class TourMode(str, enum.Enum):
    IN_PERSON = 'IN_PERSON'
    VIDEO = 'VIDEO'

class RequestStatus(str, enum.Enum):
    DRAFT = 'DRAFT'
    COLLECTING = 'COLLECTING'
    OPTIONS_PROPOSED = 'OPTIONS_PROPOSED'
    WAITING_APPROVAL = 'WAITING_APPROVAL'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'
    EXPIRED = 'EXPIRED'
    CANCELLED = 'CANCELLED'
    BOOKED = 'BOOKED'

class SlotStatus(str, enum.Enum):
    PROPOSED = 'PROPOSED'
    SELECTED = 'SELECTED'
    EXPIRED = 'EXPIRED'
    WITHDRAWN = 'WITHDRAWN'

class ApprovalStatus(str, enum.Enum):
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'
    EXPIRED = 'EXPIRED'
    CANCELLED = 'CANCELLED'

class AppointmentStatus(str, enum.Enum):
    CONFIRMED = 'CONFIRMED'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
    NO_SHOW = 'NO_SHOW'
    RESCHEDULED = 'RESCHEDULED'
    CANCELLED = 'CANCELLED'

class HoldStatus(str, enum.Enum):
    ACTIVE = 'ACTIVE'
    EXPIRED = 'EXPIRED'
    RELEASED = 'RELEASED'
    CONVERTED = 'CONVERTED'

class MessageRole(str, enum.Enum):
    USER = 'USER'
    ASSISTANT = 'ASSISTANT'
    TOOL = 'TOOL'
    SYSTEM = 'SYSTEM'
