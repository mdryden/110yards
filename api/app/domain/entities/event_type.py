# generated by datamodel-codegen:
#   filename:  event_type.json
#   timestamp: 2021-03-19T11:37:46+00:00

from __future__ import annotations

from pydantic import BaseModel


class EventType(BaseModel):
    event_type_id: int
    name: str
    title: str
