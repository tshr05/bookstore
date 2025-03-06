from bookstore.utils import create_access_token
from datetime import timedelta

def test_create_access_token():
    """Test JWT token creation"""
    token = create_access_token(data={"sub": "test@example.com"}, expires_delta=timedelta(minutes=5))
    assert isinstance(token, str)
    assert len(token) > 10
