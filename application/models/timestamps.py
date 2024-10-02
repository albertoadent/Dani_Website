from .db import db
from datetime import datetime


class Timestamps:
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def get_timestamp_breakdown(self, property_name):
        attribute = getattr(self, property_name, None)
        if attribute and isinstance(attribute, datetime):
            return {
                "year": attribute.year,
                "month": attribute.month,
                "day": attribute.day,
                "hour": attribute.hour,
                "minute": attribute.minute,
            }
