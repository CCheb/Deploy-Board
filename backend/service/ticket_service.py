from models.ticket import *
from repository.ticket_repository import TicketRepository
from uuid import UUID

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


def update_ticket(ticket_id: UUID, updated_ticket: Ticket):
    try:
        updated_ticket = repo.update_item(ticket_id, updated_ticket)
        return updated_ticket
    except KeyError as e:
        raise KeyError(f"Error in updating a ticket: {str(e)}")


def get_ticket(ticket_id: UUID) -> Ticket:
    try:
        ticket = repo.get_item(ticket_id)
        return ticket
    except KeyError as e:
        raise KeyError(f"Error in getting a ticket: {str(e)}")


def get_all_tickets() -> list[Ticket]:
    return repo.get_all_items()