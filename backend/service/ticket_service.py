from models.ticket import *
from repository.ticket_repository import TicketRepository

repo = TicketRepository() # Always restarts on startup. Server instances will always have different repos


def create_ticket(incoming_ticket: ClientTicket) -> Ticket:
    response_ticket = Ticket(**incoming_ticket.model_dump()) # Append a proper UUID
    repo.store(response_ticket)
    return response_ticket


def delete_ticket(ticket_id: UUID) -> Ticket:
    try:
        deleted_ticket = repo.delete_item(ticket_id)
        return deleted_ticket
    except KeyError as e:
        raise KeyError(f"Error in deleting a ticket: {str(e)}")