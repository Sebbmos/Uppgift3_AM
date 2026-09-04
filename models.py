from pydantic import BaseModel, Field
from datetime import datetime, timezone
import uuid

def generate_package_id() -> str:
    return f"PKG-{uuid.uuid4().hex[:6].upper()}"

class Package(BaseModel):
    package_id: str = Field(default_factory=generate_package_id, alias="package_id")
    destination: str
    history: list[str] = []
    payload: str
    sent_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), alias="sent_at")

    model_config = {"populate_by_name": True}

p1 = Package(destination="Umeå", payload="3 kartonger kaffe")
print(p1.package_id) 
print(p1.sent_at)  
print(p1.model_dump(by_alias=True))
