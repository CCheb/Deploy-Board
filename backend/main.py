from fastapi import FastAPI, HTTPException
from models.ticket import *
from service.ticket_service import *
from uuid import UUID

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/create-ticket", status_code=201)
def create_ticket(incoming_ticket: ClientTicket) -> Ticket:
    return create_ticket(incoming_ticket)

@app.delete("/delete-ticket")
def delete_ticket(ticket_id: UUID) -> Ticket:
    try:
        return delete_ticket(ticket_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=f"Error in deleting a ticket: {str(e)}")

@app.put("/update-ticket")
def update_ticket(ticket_id: UUID, updated_ticket: Ticket) -> Ticket:
    try:
        updated_ticket = repo.update_item(ticket_id, updated_ticket)
        return updated_ticket
    except KeyError as e:
        raise HTTPException(status_code=404, detail=f"Error in updating a ticket: {str(e)}")

@app.get("/get-ticket/{ticket_id}")
def get_ticket(ticket_id: UUID) -> Ticket:
    try: 
        ticket = repo.get_item(ticket_id)
        return ticket
    except KeyError as e:
        raise HTTPException(status_code=404, detail=f"Error in getting a ticket: {str(e)}")

@app.get("/get-all-tickets")
def get_all_tickets() -> list[Ticket]:
    return repo.get_all_items()