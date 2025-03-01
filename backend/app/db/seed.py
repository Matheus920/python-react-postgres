import asyncio
import json
import logging
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.db.session import AsyncSessionLocal
from app.models.role import Permission, Role
from app.models.user import User
from app.models.resource import Resource, resource_permission

# Configure logging
logger = logging.getLogger(__name__)

# Flag to track if seeding has been done
_seeded = False

# Constants for seed data
NUM_RESOURCES = 100
ADMIN_EMAIL = "admin@example.com"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"  # In a real app, use a secure password

# Resource types for variety
RESOURCE_TYPES = [
    "document", "article", "report", "manual",
    "image", "video", "audio",
    "dataset", "spreadsheet", "analytics",
    "code_snippet", "repository", "example",
    "wiki", "tutorial", "guide",
    "presentation", "diagram", "chart"
]

# Tags for categorization
TAGS = [
    "important", "archived", "draft", "published", "featured",
    "work", "personal", "shared", "confidential", "public",
    "technical", "business", "creative", "educational", "reference",
    "project_a", "project_b", "project_c", "legacy", "new"
]

# Status options
STATUSES = ["draft", "review", "published", "archived", "deprecated"]

# Sample content templates
CONTENT_TEMPLATES = [
    "This is a {type} about {topic}. It contains important information for {audience}.",
    "{type} related to {topic}. Created for {audience} to use in their work.",
    "A comprehensive {type} covering {topic} in detail. Suitable for {audience}.",
    "Quick reference {type} for {topic}. Designed specifically for {audience}.",
    "{type} showcasing {topic} with examples. Perfect for {audience} learning this subject.",
    "An in-depth analysis {type} of {topic}. Provides insights for {audience}.",
    "Collection of best practices for {topic} in this {type}. Recommended for {audience}.",
    "Experimental {type} exploring new approaches to {topic}. May interest {audience}.",
    "Historical overview {type} of {topic} development. Valuable context for {audience}.",
    "Collaborative {type} on {topic} with contributions from multiple authors. Targeted at {audience}."
]

# Topics for content
TOPICS = [
    "data science", "machine learning", "web development", 
    "cloud computing", "cybersecurity", "mobile development",
    "database optimization", "UI/UX design", "DevOps practices",
    "blockchain", "artificial intelligence", "IoT", 
    "augmented reality", "virtual reality", "quantum computing",
    "agile methodologies", "project management", "team collaboration",
    "digital marketing", "content strategy", "user research"
]

# Audience types
AUDIENCES = [
    "developers", "designers", "managers", "executives",
    "beginners", "experts", "students", "teachers",
    "researchers", "analysts", "stakeholders", "clients",
    "team members", "partners", "customers", "general public"
]


async def create_roles_and_permissions(db: AsyncSession) -> Dict[str, Role]:
    """
    Create roles and permissions in the database.
    
    Args:
        db: Database session
        
    Returns:
        Dict[str, Role]: Dictionary of role name to role object
    """
    logger.info("Creating roles and permissions")
    
    # Check if roles already exist
    result = await db.execute(select(Role))
    existing_roles = result.scalars().all()
    if existing_roles:
        logger.info(f"Found {len(existing_roles)} existing roles")
        return {role.name: role for role in existing_roles}
    
    # Create permissions
    permissions = {
        "read_resource": Permission(name="read_resource", description="Can read resources"),
        "create_resource": Permission(name="create_resource", description="Can create resources"),
        "update_resource": Permission(name="update_resource", description="Can update resources"),
        "delete_resource": Permission(name="delete_resource", description="Can delete resources"),
        "share_resource": Permission(name="share_resource", description="Can share resources"),
        "manage_users": Permission(name="manage_users", description="Can manage users"),
        "manage_roles": Permission(name="manage_roles", description="Can manage roles"),
    }
    
    for permission in permissions.values():
        db.add(permission)
    
    # Create roles with permissions
    roles = {
        "admin": Role(
            name="admin",
            description="Administrator with full access",
            permissions=list(permissions.values())
        ),
        "editor": Role(
            name="editor",
            description="Can create and edit resources",
            permissions=[
                permissions["read_resource"],
                permissions["create_resource"],
                permissions["update_resource"],
                permissions["share_resource"]
            ]
        ),
        "author": Role(
            name="author",
            description="Can create resources",
            permissions=[
                permissions["read_resource"],
                permissions["create_resource"],
                permissions["update_resource"]
            ]
        ),
        "viewer": Role(
            name="viewer",
            description="Can only view resources",
            permissions=[permissions["read_resource"]]
        )
    }
    
    for role in roles.values():
        db.add(role)
    
    await db.commit()
    logger.info(f"Created {len(roles)} roles and {len(permissions)} permissions")
    
    return roles


async def create_users(db: AsyncSession, roles: Dict[str, Role]) -> Dict[str, User]:
    """
    Create users in the database.
    
    Args:
        db: Database session
        roles: Dictionary of role name to role object
        
    Returns:
        Dict[str, User]: Dictionary of username to user object
    """
    logger.info("Creating users")
    
    # Check if admin user already exists
    result = await db.execute(select(User).where(User.username == ADMIN_USERNAME))
    admin_user = result.scalars().first()
    if admin_user:
        logger.info("Admin user already exists")
        
        # Get all users
        result = await db.execute(select(User))
        existing_users = result.scalars().all()
        return {user.username: user for user in existing_users}
    
    # Create admin user
    admin_user = User(
        email=ADMIN_EMAIL,
        username=ADMIN_USERNAME,
        hashed_password=get_password_hash(ADMIN_PASSWORD),
        first_name="Admin",
        last_name="User",
        is_active=True,
        is_admin=True,
        roles=[roles["admin"]]
    )
    db.add(admin_user)
    
    # Create regular users with different roles
    users = {
        "editor1": User(
            email="editor1@example.com",
            username="editor1",
            hashed_password=get_password_hash("password"),
            first_name="Editor",
            last_name="One",
            is_active=True,
            is_admin=False,
            roles=[roles["editor"]]
        ),
        "editor2": User(
            email="editor2@example.com",
            username="editor2",
            hashed_password=get_password_hash("password"),
            first_name="Editor",
            last_name="Two",
            is_active=True,
            is_admin=False,
            roles=[roles["editor"]]
        ),
        "author1": User(
            email="author1@example.com",
            username="author1",
            hashed_password=get_password_hash("password"),
            first_name="Author",
            last_name="One",
            is_active=True,
            is_admin=False,
            roles=[roles["author"]]
        ),
        "author2": User(
            email="author2@example.com",
            username="author2",
            hashed_password=get_password_hash("password"),
            first_name="Author",
            last_name="Two",
            is_active=True,
            is_admin=False,
            roles=[roles["author"]]
        ),
        "viewer1": User(
            email="viewer1@example.com",
            username="viewer1",
            hashed_password=get_password_hash("password"),
            first_name="Viewer",
            last_name="One",
            is_active=True,
            is_admin=False,
            roles=[roles["viewer"]]
        ),
        "inactive_user": User(
            email="inactive@example.com",
            username="inactive_user",
            hashed_password=get_password_hash("password"),
            first_name="Inactive",
            last_name="User",
            is_active=False,
            is_admin=False,
            roles=[roles["viewer"]]
        ),
    }
    
    # Add admin user to the dictionary
    users[ADMIN_USERNAME] = admin_user
    
    # Add all users to the database
    for user in users.values():
        if user != admin_user:  # Admin user already added
            db.add(user)
    
    await db.commit()
    logger.info(f"Created {len(users)} users")
    
    return users


def generate_resource_metadata(resource_type: str, is_public: bool) -> Dict:
    """
    Generate metadata for a resource.
    
    Args:
        resource_type: Type of resource
        is_public: Whether the resource is public
        
    Returns:
        Dict: Resource metadata
    """
    # Select random tags (1-5)
    num_tags = random.randint(1, 5)
    tags = random.sample(TAGS, num_tags)
    
    # Generate creation and modification dates
    created_date = datetime.now() - timedelta(days=random.randint(0, 365))
    modified_date = created_date + timedelta(days=random.randint(0, 30))
    
    # Base metadata
    metadata = {
        "type": resource_type,
        "tags": tags,
        "status": random.choice(STATUSES),
        "created_date": created_date.isoformat(),
        "modified_date": modified_date.isoformat(),
        "version": f"1.{random.randint(0, 9)}",
        "is_public": is_public,
    }
    
    # Add type-specific metadata
    if resource_type in ["document", "article", "report", "manual", "wiki", "tutorial", "guide"]:
        metadata.update({
            "word_count": random.randint(500, 10000),
            "language": random.choice(["en", "es", "fr", "de", "zh"]),
            "category": random.choice(["technical", "business", "creative", "educational"]),
            "reading_time": random.randint(5, 60),
        })
    elif resource_type in ["image", "video", "audio"]:
        metadata.update({
            "format": random.choice(["jpg", "png", "mp4", "mp3", "wav"]),
            "duration": random.randint(10, 3600) if resource_type != "image" else None,
            "resolution": random.choice(["720p", "1080p", "4K"]) if resource_type != "audio" else None,
            "size_kb": random.randint(100, 10000),
        })
    elif resource_type in ["dataset", "spreadsheet", "analytics"]:
        metadata.update({
            "rows": random.randint(10, 10000),
            "columns": random.randint(5, 100),
            "format": random.choice(["csv", "xlsx", "json", "sql"]),
            "has_headers": random.choice([True, False]),
            "source": random.choice(["internal", "external", "third-party", "generated"]),
        })
    elif resource_type in ["code_snippet", "repository", "example"]:
        metadata.update({
            "language": random.choice(["python", "javascript", "java", "go", "rust", "c++"]),
            "lines": random.randint(10, 1000),
            "license": random.choice(["MIT", "Apache-2.0", "GPL-3.0", "proprietary"]),
            "dependencies": random.randint(0, 20),
        })
    elif resource_type in ["presentation", "diagram", "chart"]:
        metadata.update({
            "slides": random.randint(5, 50) if resource_type == "presentation" else None,
            "format": random.choice(["pptx", "pdf", "svg", "png"]),
            "theme": random.choice(["corporate", "minimal", "colorful", "technical"]),
        })
    
    # Remove None values
    return {k: v for k, v in metadata.items() if v is not None}


def generate_resource_content(resource_type: str) -> str:
    """
    Generate content for a resource.
    
    Args:
        resource_type: Type of resource
        
    Returns:
        str: Resource content
    """
    template = random.choice(CONTENT_TEMPLATES)
    topic = random.choice(TOPICS)
    audience = random.choice(AUDIENCES)
    
    content = template.format(type=resource_type, topic=topic, audience=audience)
    
    # Add some random paragraphs for longer content
    if random.random() < 0.7:  # 70% chance of longer content
        num_paragraphs = random.randint(1, 5)
        for _ in range(num_paragraphs):
            paragraph_template = random.choice(CONTENT_TEMPLATES)
            paragraph_topic = random.choice(TOPICS)
            paragraph_audience = random.choice(AUDIENCES)
            
            paragraph = paragraph_template.format(
                type=resource_type, 
                topic=paragraph_topic, 
                audience=paragraph_audience
            )
            
            content += f"\n\n{paragraph}"
    
    return content


async def create_resources(
    db: AsyncSession, 
    users: Dict[str, User]
) -> List[Resource]:
    """
    Create resources in the database.
    
    Args:
        db: Database session
        users: Dictionary of username to user object
        
    Returns:
        List[Resource]: List of created resources
    """
    logger.info(f"Creating {NUM_RESOURCES} resources")
    
    # Check if resources already exist
    result = await db.execute(select(Resource))
    existing_resources = result.scalars().all()
    if existing_resources:
        logger.info(f"Found {len(existing_resources)} existing resources")
        return existing_resources
    
    resources = []
    
    # Create resources with different characteristics
    for i in range(1, NUM_RESOURCES + 1):
        # Determine resource characteristics
        resource_type = random.choice(RESOURCE_TYPES)
        is_public = random.random() < 0.3  # 30% chance of being public
        
        # Select owner (weighted distribution)
        if i <= 40:  # 40% owned by admin
            owner = users[ADMIN_USERNAME]
        elif i <= 60:  # 20% owned by editors
            owner = users[random.choice(["editor1", "editor2"])]
        elif i <= 80:  # 20% owned by authors
            owner = users[random.choice(["author1", "author2"])]
        else:  # 20% owned by viewers
            owner = users[random.choice(["viewer1", "inactive_user"])]
        
        # Generate metadata
        metadata = generate_resource_metadata(resource_type, is_public)
        
        # Generate content
        content = generate_resource_content(resource_type)
        
        # Create resource
        resource = Resource(
            name=f"{resource_type.capitalize()} {i}",
            description=f"A {resource_type} resource with ID {i}",
            content=content,
            meta_data=json.dumps(metadata),
            is_public=is_public,
            owner_id=owner.id
        )
        
        # Add some edge cases
        if i == 95:
            # Very long name
            resource.name = "This is a resource with a very long name that might cause issues with display or storage limits in some systems - it's intentionally long to test edge cases"
        elif i == 96:
            # Special characters in metadata
            special_metadata = metadata.copy()
            special_metadata["special_chars"] = "!@#$%^&*()_+{}[]|\\:;\"'<>,.?/~`"
            resource.meta_data = json.dumps(special_metadata)
        elif i == 97:
            # Empty metadata
            resource.meta_data = "{}"
        elif i == 98:
            # Very long content
            resource.content = content * 20  # Repeat content 20 times
        elif i == 99:
            # Empty content
            resource.content = ""
        elif i == 100:
            # Unicode characters
            resource.name = "Unicode Resource 🚀 😊 🌍 ⭐ 🔥"
            resource.description = "Description with unicode: 你好 안녕하세요 こんにちは Привет"
        
        db.add(resource)
        resources.append(resource)
    
    await db.commit()
    logger.info(f"Created {len(resources)} resources")
    
    return resources


async def setup_resource_sharing(
    db: AsyncSession,
    resources: List[Resource],
    users: Dict[str, User]
) -> None:
    """
    Set up resource sharing between users.
    
    Args:
        db: Database session
        resources: List of resources
        users: Dictionary of username to user object
    """
    logger.info("Setting up resource sharing")
    
    # Check if sharing already exists
    result = await db.execute(select(resource_permission))
    existing_sharing = result.all()
    if existing_sharing:
        logger.info(f"Found {len(existing_sharing)} existing resource sharing records")
        return
    
    # Set up sharing for some resources
    for i, resource in enumerate(resources):
        # Skip some resources (no sharing)
        if i % 5 == 0:  # 20% of resources are not shared
            continue
        
        # Determine sharing pattern
        if i % 10 == 1:  # Share with all users
            for username, user in users.items():
                if user.id != resource.owner_id:  # Don't share with owner
                    permission_type = random.choice(["read", "write", "admin"])
                    await db.execute(
                        resource_permission.insert().values(
                            resource_id=resource.id,
                            user_id=user.id,
                            permission_type=permission_type
                        )
                    )
        elif i % 10 == 2:  # Share with one specific user
            user = users[random.choice(list(users.keys()))]
            if user.id != resource.owner_id:  # Don't share with owner
                permission_type = random.choice(["read", "write", "admin"])
                await db.execute(
                    resource_permission.insert().values(
                        resource_id=resource.id,
                        user_id=user.id,
                        permission_type=permission_type
                    )
                )
        elif i % 10 == 3:  # Share with multiple users, different permissions
            num_users = random.randint(2, 4)
            selected_users = random.sample(list(users.values()), num_users)
            for user in selected_users:
                if user.id != resource.owner_id:  # Don't share with owner
                    permission_type = random.choice(["read", "write", "admin"])
                    await db.execute(
                        resource_permission.insert().values(
                            resource_id=resource.id,
                            user_id=user.id,
                            permission_type=permission_type
                        )
                    )
        else:  # Default sharing pattern
            # Share with 1-2 random users
            num_users = random.randint(1, 2)
            selected_users = random.sample(list(users.values()), num_users)
            for user in selected_users:
                if user.id != resource.owner_id:  # Don't share with owner
                    permission_type = random.choice(["read", "write"])
                    await db.execute(
                        resource_permission.insert().values(
                            resource_id=resource.id,
                            user_id=user.id,
                            permission_type=permission_type
                        )
                    )
    
    await db.commit()
    logger.info("Resource sharing setup complete")


async def clean_db(db: AsyncSession) -> None:
    """
    Clean the database by deleting all records.
    
    Args:
        db: Database session
    """
    logger.info("Cleaning database")
    
    # Import the association tables
    from app.models.user import user_role
    from app.models.role import role_permission
    
    # Delete all resource permissions
    await db.execute(resource_permission.delete())
    
    # Delete all resources
    await db.execute(Resource.__table__.delete())
    
    # Delete all user roles
    await db.execute(user_role.delete())
    
    # Delete all users
    await db.execute(User.__table__.delete())
    
    # Delete all role permissions
    await db.execute(role_permission.delete())
    
    # Delete all roles
    await db.execute(Role.__table__.delete())
    
    # Delete all permissions
    await db.execute(Permission.__table__.delete())
    
    await db.commit()
    logger.info("Database cleaned")


async def seed_db(force: bool = False) -> None:
    """
    Seed the database with initial data.
    
    Args:
        force: Force seeding even if already seeded
    """
    global _seeded
    
    # Skip if already seeded and not forced
    if _seeded and not force:
        logger.info("Database already seeded, skipping")
        return
    
    logger.info("Seeding database")
    
    async with AsyncSessionLocal() as db:
        # Clean the database if force is True
        if force:
            await clean_db(db)
        
        # Create roles and permissions
        roles = await create_roles_and_permissions(db)
        
        # Create users
        users = await create_users(db, roles)
        
        # Create resources
        resources = await create_resources(db, users)
        
        # Set up resource sharing
        await setup_resource_sharing(db, resources, users)
    
    _seeded = True
    logger.info("Database seeding complete")


if __name__ == "__main__":
    # Run the seeding function when script is executed directly
    asyncio.run(seed_db(force=True))
