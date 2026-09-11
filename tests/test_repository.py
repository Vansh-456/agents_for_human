import pytest

from backend.repositories.dynamodb_repository import DynamoDBRepository


@pytest.fixture
def repo():
    repository = DynamoDBRepository()
    repository.reset()
    return repository


def test_vendor_persistence(repo):
    repo.save_vendor(
        "v1",
        {
            "name": "Test Restaurant",
            "trust_score": 0.95
        }
    )

    vendor = repo.get_vendor("v1")

    assert vendor["id"] == "v1"
    assert vendor["name"] == "Test Restaurant"
    assert vendor["trust_score"] == 0.95


def test_surplus_persistence(repo):
    repo.save_surplus(
        "s1",
        {
            "vendor_id": "v1",
            "quantity": 45,
            "safe_window_mins": 42
        }
    )

    surplus = repo.get_surplus("s1")

    assert surplus["id"] == "s1"
    assert surplus["vendor_id"] == "v1"
    assert surplus["quantity"] == 45


def test_all_surplus(repo):
    repo.save_surplus("s1", {"quantity": 20})
    repo.save_surplus("s2", {"quantity": 30})

    surplus = repo.get_all_surplus()

    ids = {item["id"] for item in surplus}

    assert "s1" in ids
    assert "s2" in ids


def test_allocation_persistence(repo):
    repo.save_allocation(
        "plan1",
        {
            "surplus_id": "s1",
            "ngo_id": "ngo1",
            "rider_id": "rider1",
            "status": "EXECUTING"
        }
    )

    allocation = repo.get_allocation("plan1")

    assert allocation["id"] == "plan1"
    assert allocation["surplus_id"] == "s1"
    assert allocation["ngo_id"] == "ngo1"
    assert allocation["status"] == "EXECUTING"


def test_event_recording(repo):
    event = repo.record_event(
        "SURPLUS_CREATED",
        "vendor_1",
        {
            "surplus_id": "s1",
            "quantity": 45
        }
    )

    events = repo.get_events()

    assert event["event_id"].startswith("evt_")
    assert event["event_type"] == "SURPLUS_CREATED"
    assert event["actor"] == "vendor_1"
    assert len(events) == 1
    assert events[0]["event_id"] == event["event_id"]


def test_event_history(repo):
    repo.record_event(
        "SURPLUS_CREATED",
        "vendor_1",
        {"quantity": 45}
    )

    repo.record_event(
        "ALLOCATION_CREATED",
        "system",
        {"plan_id": "plan1"}
    )

    events = repo.get_events()

    assert len(events) == 2
    assert events[0]["event_type"] == "SURPLUS_CREATED"
    assert events[1]["event_type"] == "ALLOCATION_CREATED"


def test_reset(repo):
    repo.save_surplus("s1", {"quantity": 45})
    repo.save_allocation("plan1", {"status": "EXECUTING"})
    repo.record_event(
        "SURPLUS_CREATED",
        "vendor_1",
        {"quantity": 45}
    )

    repo.reset()

    assert repo.get_all_surplus() == []
    assert repo.get_all_allocations() == []
    assert repo.get_events() == []