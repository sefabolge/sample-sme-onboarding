import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_user_creation():
    user = User.objects.create_user(
        username="newuser",
        full_name="New User",
        password="securepass123"
    )
    assert user.username == "newuser"
    assert user.full_name == "New User"
    assert user.is_active
    assert not user.is_staff
