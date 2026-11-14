from uuid import UUID
from models.ticket import Ticket

class TicketRepository():
    def __init__(self):
        self.tickets = dict[UUID, Ticket]()

    def store(self, incoming_item: Ticket):
        self.tickets[incoming_item.ticket_id] = incoming_item

    def get_item(self, item_id: UUID) -> Ticket:
        try:
            return self.tickets[item_id]
        except KeyError:
            raise KeyError(f"Ticket with ID {item_id} not found.")

    def update_item(self, item_id: UUID, updated_item: Ticket):
        if item_id not in self.tickets:
            raise KeyError(f"Ticket with ID {item_id} not found.")
        self.tickets[item_id] = updated_item # Silently creates ticket if item_id does not exist
        return self.tickets[item_id]

    def delete_item(self, item_id: UUID) -> Ticket:
        try:
            return self.tickets.pop(item_id)
        except KeyError:
            raise KeyError(f"Ticket with ID {item_id} not found.")

    def get_all_items(self) -> list[Ticket]:
        return list(self.tickets.values())
