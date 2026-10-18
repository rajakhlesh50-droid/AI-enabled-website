"""
Centurion University of Technology and Management (CUTM)
Backend Domain Models & Data Structures
"""

from dataclasses import dataclass, asdict, field
from typing import List, Optional
import datetime


@dataclass
class User:
    id: Optional[int] = None
    username: str = ""
    email: str = ""
    phone: Optional[str] = None
    name: str = ""
    password_hash: str = ""
    role: str = "student"
    created_at: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

    def to_dict(self):
        d = asdict(self)
        d.pop("password_hash", None)
        return d


@dataclass
class Lead:
    id: Optional[int] = None
    ref_id: str = ""
    name: str = ""
    email: str = ""
    phone: str = ""
    course: str = ""
    department: str = ""
    marks: Optional[float] = None
    city: str = ""
    state: str = ""
    message: str = ""
    score: int = 0
    status: str = "New"
    created_at: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

    def to_dict(self):
        return asdict(self)


@dataclass
class Event:
    id: str = ""
    type: str = "Conference"
    date: str = ""
    title: str = ""
    description: str = ""
    place: str = ""
    format: str = "In person"
    image: str = ""

    def to_dict(self):
        return asdict(self)


@dataclass
class EventRegistration:
    id: str = ""
    event_id: str = ""
    event_title: str = ""
    name: str = ""
    email: str = ""
    phone: str = ""
    created_at: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

    def to_dict(self):
        return asdict(self)


@dataclass
class Course:
    id: str = ""
    name: str = ""
    department: str = ""
    short_code: str = ""
    duration: str = ""
    eligibility: str = ""
    description: str = ""
    highlights: List[str] = field(default_factory=list)
    tag: str = ""
    seats: int = 60
    fee: str = ""
    icon: str = "🎓"

    def to_dict(self):
        return asdict(self)

