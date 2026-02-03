import uuid
from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, Float, String

from backend.fastapi_app.db.session import Base


class InteractionLog(Base):
    __tablename__ = "interaction_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    request_text = Column(String, nullable=False)
    response_text = Column(String, nullable=False)
    model = Column(String, nullable=True)
    user_id = Column(String, nullable=True)

    risk_score = Column(Float, nullable=False)
    severity = Column(String, nullable=False)
    labels = Column(JSON, nullable=False, default=list)
