"""Automated non-GUI tests for the prototype repository and sync state model."""
import tempfile
from pathlib import Path
from app import Repository
from sync_simulation import Server, Operation

def test_repository_seed_search_and_empty():
    with tempfile.TemporaryDirectory() as td:
        repo=Repository(Path(td)/"test.db")
        assert len(repo.all()) == 3
        assert repo.all("Fort")[0][1] == "Old Fort"
        assert repo.all("Atlantis") == []
        assert repo.get("fort")[1] == "Old Fort"
        repo.close()

def test_sync_ack_conflict_duplicate():
    server=Server()
    a=Operation("A-1","A","visit-1",1,"11:00")
    b=Operation("B-1","B","visit-1",1,"12:00")
    assert server.apply(a)["status"] == "ACK"
    assert server.apply(b)["status"] == "CONFLICT"
    assert server.apply(a)["status"] == "DUPLICATE"
    assert server.items["visit-1"] == {"visit_time":"11:00","version":2}

if __name__=="__main__":
    test_repository_seed_search_and_empty()
    test_sync_ack_conflict_duplicate()
    print("PASS: repository seed/search/empty-state data tests")
    print("PASS: sync ACK/conflict/idempotent-retry tests")
