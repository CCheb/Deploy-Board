"""
Testing suite for ticket_service.py and ticket_repository.py. Uses pytest fixtures to create a mock repository and mock tickets for testing.
Since both modules are tightly coupled and simple in designed, its worth to test them both together.
"""
import pytest

from service import ticket_service
from service.ticket_service import *
from models.ticket import *
from datetime import date
from repository.ticket_repository import TicketRepository
from uuid import UUID, uuid4


@pytest.fixture
def mock_ticket_repo(monkeypatch):
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


# Tests follow a Arrange-Act-Assert pattern. Most Arranges are handled by the fixtures above. 
# Act and Assert are handled in the test functions below.

def test_ticket_creation_passes(mock_ticket_repo, mock_client_ticket):
    response_ticket = create_ticket(mock_client_ticket)
    stored_ticket = mock_ticket_repo.get_item(response_ticket.ticket_id)

    check_for_proper_ticket(response_ticket)
    check_two_tickets_are_equal(response_ticket, stored_ticket)

# No test_ticket_creation_fails since pydantic is already handling model validation

def test_ticket_deletion_passes(mock_ticket_repo, mock_client_ticket):
    response_ticket = create_ticket(mock_client_ticket)
    deleted_ticket = delete_ticket(response_ticket.ticket_id)

    check_for_proper_ticket(deleted_ticket)
    check_two_tickets_are_equal(response_ticket, deleted_ticket)

    with pytest.raises(KeyError):
        mock_ticket_repo.get_item(response_ticket.ticket_id) # We know at this point that the ticket has been deleted, so this should raise a KeyError


def test_ticket_deletion_fails(mock_ticket_repo):
    non_existing_ticket_id : UUID = uuid4() # in UUID format
    with pytest.raises(KeyError):
        delete_ticket(non_existing_ticket_id)

    with pytest.raises(KeyError):
        mock_ticket_repo.get_item(non_existing_ticket_id)


def test_ticket_update_passes(mock_ticket_repo, mock_client_ticket):
    response_ticket = create_ticket(mock_client_ticket)

    updated_ticket = Ticket(
        ticket_id=response_ticket.ticket_id,
        title="Updated Test Ticket",
        description="This is an updated test ticket.",
        start_date=date.today(),
        due_date=date.today(),
        current_stage="In Progress",
        priority_level="High"
    )

    updated_response_ticket = update_ticket(response_ticket.ticket_id, updated_ticket)
    stored_updated_ticket = mock_ticket_repo.get_item(response_ticket.ticket_id)

    check_for_proper_ticket(updated_response_ticket)
    check_two_tickets_are_equal(updated_response_ticket, stored_updated_ticket)
    check_two_tickets_are_not_equal(response_ticket, updated_response_ticket)


def test_ticket_update_fails(mock_ticket_repo, mock_client_ticket):
    non_existing_ticket_id : UUID = uuid4() # in UUID format

    with pytest.raises(KeyError):
        update_ticket(non_existing_ticket_id, mock_client_ticket)

    with pytest.raises(KeyError):
        mock_ticket_repo.get_item(non_existing_ticket_id)


def test_get_ticket_passes(mock_ticket_repo, mock_client_ticket):
    response_ticket = create_ticket(mock_client_ticket)
    retrieved_ticket = get_ticket(response_ticket.ticket_id)

    check_for_proper_ticket(retrieved_ticket)
    check_two_tickets_are_equal(response_ticket, retrieved_ticket)


def test_get_ticket_fails(mock_ticket_repo):
    non_existing_ticket_id : UUID = uuid4() # in UUID format

    with pytest.raises(KeyError):
        get_ticket(non_existing_ticket_id)

    with pytest.raises(KeyError):
        mock_ticket_repo.get_item(non_existing_ticket_id)


def test_get_all_tickets_passes(mock_ticket_repo, mock_client_ticket):
    num_of_tickets_to_create = 2

    response_tickets = [create_ticket(mock_client_ticket) for _ in range(num_of_tickets_to_create)]  # Create two tickets

    all_tickets = get_all_tickets()

    assert len(all_tickets) == num_of_tickets_to_create
    assert mock_ticket_repo.get_all_items() == all_tickets  # Ensure the repository has the same tickets
    
    for response_ticket in response_tickets:
        assert response_ticket in all_tickets
        check_for_proper_ticket(response_ticket)

    
def test_get_all_tickets_empty(mock_ticket_repo):
    all_tickets = get_all_tickets()
    assert len(all_tickets) == 0


def check_for_proper_ticket(ticket: Ticket):
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

def check_two_tickets_are_not_equal(ticket1: Ticket, ticket2: Ticket):
    assert ticket1 != ticket2
