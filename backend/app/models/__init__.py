from app.models.user import User
from app.models.role import Role, Permission
from app.models.resource import Resource

# For Alembic to detect all models
__all__ = ["User", "Role", "Permission", "Resource"]
