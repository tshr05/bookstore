import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Session
from bookstore.database import get_db  # ✅ No need to import `engine` again
from fastapi.testclient import TestClient
from bookstore.main import app

TEST_DATABASE_URL = "sqlite:///./test_test.db"

# ✅ Use a single engine for testing
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def test_db():
    """Creates a fresh test database."""
    SQLModel.metadata.create_all(engine)
    session = Session(engine)
    yield session
    session.close()
    SQLModel.metadata.drop_all(engine)  # ✅ Cleanup after tests

@pytest.fixture(scope="module")
def client():
    """Test client for FastAPI."""
    test_client = TestClient(app)
    return test_client

@pytest.fixture(scope="module")
def override_get_db(test_db):
    """Overrides the get_db dependency with the test database."""
    def _get_db():
        yield test_db

    app.dependency_overrides[get_db] = _get_db  # ✅ Correct override
    yield
    app.dependency_overrides.clear()  # ✅ Cleanup after tests
