from fastapi import FastAPI, HTTPException
from models.ticket import Ticket, ClientTicket
from service import ticket_service
from uuid import UUID

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/create-ticket", status_code=201)
def create_ticket(incoming_ticket: ClientTicket) -> Ticket:
    return ticket_service.create_ticket(incoming_ticket)

@app.delete("/delete-ticket")
def delete_ticket(ticket_id: UUID) -> Ticket:
    try:
        return ticket_service.delete_ticket(ticket_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=f"Error in deleting a ticket: {str(e)}")

@app.put("/update-ticket")
def update_ticket(ticket_id: UUID, updated_ticket: Ticket) -> Ticket:
    try:
        return ticket_service.update_ticket(ticket_id, updated_ticket)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=f"Error in updating a ticket: {str(e)}")

@app.get("/get-ticket/{ticket_id}")
def get_ticket(ticket_id: UUID) -> Ticket:
    try: 
        return ticket_service.get_ticket(ticket_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=f"Error in getting a ticket: {str(e)}")

@app.get("/get-all-tickets")
def get_all_tickets() -> list[Ticket]:
    return ticket_service.get_all_tickets()