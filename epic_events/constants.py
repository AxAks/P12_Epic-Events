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
STATUSES = [
    (1, 'created'),
    (2, 'ongoing'),
    (3, 'terminated')
]