from app.models.campaign import Campaign
from app.models.user import User


campaigns: list[Campaign] = []

users: list[User] = [
    User(user_id=1, name="Alice", email="alice@example.com", segment_id=101),
    User(user_id=2, name="Bob", email="bob@example.com", segment_id=102),
    User(user_id=3, name="Charlie", email="charlie@example.com", segment_id=101)
]