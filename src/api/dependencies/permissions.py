from fastapi import Depends

from src.api.dependencies.token_validation import get_current_user

from src.schemas.users import UsersResponse

from src.core.enums import UsersRole

from src.core.exception.permisions import PermissionDeniedException


def require_admin_or_superuser(current_user: UsersResponse = Depends(get_current_user)) -> UsersResponse:
    if current_user.role not in {UsersRole.SUPERUSER, UsersRole.ADMIN}:
        raise PermissionDeniedException()
    return current_user

def require_superuser(current_user: UsersResponse = Depends(get_current_user)) -> UsersResponse:
    if current_user.role != UsersRole.SUPERUSER:
        raise PermissionDeniedException()
    return current_user

