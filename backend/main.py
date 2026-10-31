from fastapi import FastAPI, HTTPException
from models.ticket import *
from repository.ticket_repository import TicketRepository
from uuid import UUID

app = FastAPI()
repo = TicketRepository() # Always restarts on startup. Server instances will always have different repos

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/create-ticket", status_code=201)
def create_ticket(incoming_ticket: ClientTicket) -> Ticket:
    response_ticket = Ticket(**incoming_ticket.model_dump()) # Append a proper UUID
    repo.store(response_ticket)
    return response_ticket

@app.delete("/delete-ticket")
def delete_ticket(ticket_id: UUID) -> Ticket:
    try:
        deleted_ticket = repo.delete_ticket(ticket_id)
        return deleted_ticket
    except KeyError as e:
        raise HTTPException(status_code=404, detail=f"Error in deleting a ticket: {str(e)}")

@app.put("/update-ticket")
def update_ticket(ticket_id: UUID, updated_ticket: Ticket) -> Ticket:
    try:
        updated_ticket = repo.update_ticket(ticket_id, updated_ticket)
        return updated_ticket
    except KeyError as e:
        raise HTTPException(status_code=404, detail=f"Error in updating a ticket: {str(e)}")

@app.get("/get-ticket/{ticket_id}")
def get_ticket(ticket_id: UUID) -> Ticket:
    try: 
        ticket = repo.get_ticket(ticket_id)
        return ticket
    except KeyError as e:
        raise HTTPException(status_code=404, detail=f"Error in getting a ticket: {str(e)}")

@app.get("/get-all-tickets")
def get_all_tickets() -> list[Ticket]:
    return repo.get_all_tickets()