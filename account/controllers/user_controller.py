from django.contrib.auth.models import User
from django.db.models.query import QuerySet


def register_new_user(user_data: dict) -> User:
    """
    Create a new user in the database.
    """
    user_instance = User.objects.create(
        username=user_data['username'],
        email=user_data['email'],
        first_name=user_data['first_name'],
        last_name=user_data['last_name']
    )

    user_instance.set_password(user_data['password'])
    user_instance.save()

    return user_instance


def retrieve_user_by_id(user_id: int) -> User:
    """ Get user information by ID.
    """
    user_instance = User.objects.get(id=user_id)
    return user_instance


def retrieve_all_users() -> QuerySet:
    """ Get all users registred in the system.
    """
    users = User.objects.all()
    return users
