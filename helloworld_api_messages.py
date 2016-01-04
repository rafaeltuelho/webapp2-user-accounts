"""ProtoRPC message class definitions for TicTicToe API."""


from protorpc import messages
import endpoints
import httplib

class ConflictException(endpoints.ServiceException):
  """Conflict exception that is mapped to a 409 response."""
  http_status = httplib.CONFLICT

class BoardMessage(messages.Message):
    """ProtoRPC message definition to represent a board."""
    state = messages.StringField(1, required=True)


class ScoresListRequest(messages.Message):
    """ProtoRPC message definition to represent a scores query."""
    limit = messages.IntegerField(1, default=10)
    class Order(messages.Enum):
        WHEN = 1
        TEXT = 2
    order = messages.EnumField(Order, 2, default=Order.WHEN)


class ScoreRequestMessage(messages.Message):
    """ProtoRPC message definition to represent a score to be inserted."""
    outcome = messages.StringField(1, required=True)


class ScoreResponseMessage(messages.Message):
    """ProtoRPC message definition to represent a score that is stored."""
    id = messages.IntegerField(1)
    outcome = messages.StringField(2)
    played = messages.StringField(3)

class UserRequestMessage(messages.Message):
    """ProtoRPC message definition to represent a user to be created."""
    user_name = messages.StringField(1)
    email = messages.StringField(2)
    name = messages.StringField(3)
    last_name = messages.StringField(4)
    password = messages.StringField(5)

class UserResponseMessage(messages.Message):
    """ProtoRPC message definition to represent a user created response."""
    user_name = messages.StringField(1)
    confirmation_link = messages.StringField(2)
    error_message = messages.StringField(3)
    created = messages.BooleanField(4)
