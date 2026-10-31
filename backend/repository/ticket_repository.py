from uuid import UUID
from models.ticket import Ticket

class TicketRepository:
    def __init__(self):
        self.tickets = dict[UUID, Ticket]()

    def store(self, incoming_ticket: Ticket):
        self.tickets[incoming_ticket.ticket_id] = incoming_ticket

    def get_ticket(self, ticket_id: UUID) -> Ticket:
        try:
            return self.tickets[ticket_id]
        except KeyError:
            raise KeyError(f"Ticket with ID {ticket_id} not found.")

    def update_ticket(self, ticket_id: UUID, updated_ticket: Ticket):
        self.tickets[ticket_id] = updated_ticket
        return self.tickets[ticket_id]

    def delete_ticket(self, ticket_id: UUID) -> Ticket:
        try:
            return self.tickets.pop(ticket_id)
        except KeyError:
            raise KeyError(f"Ticket with ID {ticket_id} not found.")

    def get_all_tickets (self) -> list[Ticket]:
        return list(self.tickets.values())
