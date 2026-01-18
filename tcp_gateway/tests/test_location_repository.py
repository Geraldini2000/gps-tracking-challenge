from tcp_gateway.repositories.in_memory_location_repository import InMemoryLocationRepository


def test_save_and_get_last_location():
    repo = InMemoryLocationRepository()

    repo.save_last_location("ABC123", {"latitude": 10.0})
    result = repo.get_last_location("ABC123")

    assert result["latitude"] == 10.0


def test_fifo_overwrite_last_location():
    repo = InMemoryLocationRepository()

    repo.save_last_location("ABC123", {"latitude": 10.0})
    repo.save_last_location("ABC123", {"latitude": 20.0})

    result = repo.get_last_location("ABC123")

    assert result["latitude"] == 20.0
