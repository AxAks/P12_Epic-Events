"""
Declaration of constants used throughout the project
"""

# Users Roles
MANAGER = 1
SALES = 2
SUPPORT = 3
USERS_ROLES = (
    (MANAGER, 'Manager'),
    (SALES, 'Sales'),
    (SUPPORT, 'Support'),
)

# Events
CREATED = 1
ONGOING = 2
TERMINATED = 3
STATUSES = [
    (CREATED, 'created'),
    (ONGOING, 'ongoing'),
    (TERMINATED, 'terminated')
]