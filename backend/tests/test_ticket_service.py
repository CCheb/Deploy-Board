import pytest


from service import ticket_service
from service.ticket_service import *
from models.ticket import *
from datetime import date
from repository.ticket_repository import TicketRepository


@pytest.fixture
def mock_ticket_repo(monkeypatch):
    # Arrange: create a fresh repository
    test_repo = TicketRepository()

    # Replace the service's global repository
    # This literally replaces the repo in ticket_service with our test_repo
    monkeypatch.setattr(ticket_service, "repo", test_repo)

    return test_repo


@pytest.fixture
def mock_client_ticket():
    return ClientTicket(
        title="Test Ticket",
        description="This is a test ticket.",
        start_date=date.today(),
        due_date=date.today(),
        current_stage="To Do",
        priority_level="Medium"
    )


# Tests follow a Arrange-Act-Assert pattern. Arrange is handled by the fixtures above. 
# Act and Assert are handled in the test functions below.

def test_ticket_creation_works(mock_ticket_repo, mock_client_ticket):
    response_ticket = create_ticket(mock_client_ticket)
    stored_ticket = mock_ticket_repo.get_item(response_ticket.ticket_id)

    check_for_proper_ticket(response_ticket)
    check_two_tickets_are_equal(response_ticket, stored_ticket)

def check_for_proper_ticket(ticket: Ticket):
    assert isinstance(ticket, Ticket)
    assert isinstance(ticket.ticket_id, UUID)

    assert hasattr(ticket, "ticket_id")
    assert hasattr(ticket, "title")
    assert hasattr(ticket, "description")
    assert hasattr(ticket, "start_date")
    assert hasattr(ticket, "due_date")
    assert hasattr(ticket, "current_stage")
    assert hasattr(ticket, "priority_level")

def check_two_tickets_are_equal(ticket1: Ticket, ticket2: Ticket):
    assert ticket1 == ticket2
    assert ticket1.model_dump() == ticket2.model_dump()


# Pydantic handles model validation before it hits create_ticket so we dont need 
# a function for testing an incoming invalid ticket. If the model is invalid, it will raise a ValidationError 
# before it even reaches the service layer.


