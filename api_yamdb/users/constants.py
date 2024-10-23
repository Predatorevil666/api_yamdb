from users.roles import Roles


MAX_ROLE_LENGTH = max(len(role.value) for role in Roles)

EMAIL_LENGTH = 254
USERNAME_LENGTH = 150
CONFIRMATION_LENGTH = 6
