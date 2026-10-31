from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import date
from typing import Literal

class ClientTicket(BaseModel):
    title: str = Field(..., max_length=200)
    description: str | None = Field(default=None)
    start_date: date = Field(default_factory=date.today)
    due_date: date | None = Field(default=None)
    current_stage: Literal["To Do", "In Progress", "Done"] = Field(default="To Do")
    priority_level: Literal["Low", "Medium", "High"] = Field(default="Medium")

class Ticket(ClientTicket):
    ticket_id: UUID = Field(default_factory=uuid4)