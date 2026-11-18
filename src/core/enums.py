from enum import Enum

class UsersRole(str, Enum):
    SUPERUSER = "superuser"
    ADMIN = "admin"
    BUYER = "buyer"
