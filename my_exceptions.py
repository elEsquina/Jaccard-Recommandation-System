class SysMessages:
    """Class containing system messages.
    This class provides system messages used for various operations.
    """

    WrongPassword = "Wrong password!"
    LoggingSuccess = "Successfully logged in as {}"
    UserCreated = "New user was created with ID: {}"
    UserDeleted = "User with ID {} was deleted"
    Loggout = "Successfully logged out"
    Upload = "New video with ID {} was created"
    Unupload = "The video was deleted"
    Liked = "Video with ID {} successfully liked"
    Disliked = "Video with ID {} successfully disliked"
    Subscribe = "Successfully subscribed to ID {}"
    Unsubscribe = "Successfully unsubscribed to ID {}"
    Watch_video = "Successfully watched video with ID {}"

class ErrorMessages:
    """Class containing error messages.
    This class provides error messages for various error scenarios.
    """

    InvalidName = "Invalid name!"

    #Session
    SessionUnicity = "You can only create one object out of the session class"
    LoggingError = "You need to be logged in to perform this operation"

    #User
    UserNotFound = "User with ID {} was not found"
    SubscribeError = "You can't subscribe (unsubscribe) to a user that you already subscribed to (unsubscribe to)"
    InvalidPassword = "Invalid password!"

    #Video
    VideoNotFound = "Video with ID {} was not found"
    VideoNotOwned = "You are not the author of this video"



class UnicityError(Exception):
    def __init__(self, *args: object) -> None:
        """Exception raised for errors related to unicity.

        Args:
            *args: Variable length argument list.
        """

        super().__init__(*args)


class EmptyError(Exception):
    def __init__(self) -> None:
        """Exception raised for indicating an empty data structure."""

        super().__init__("Your structure is empty")


class LoggingError(Exception):
    def __init__(self) -> None:
        """Exception raised for errors related to logging."""

        super().__init__(ErrorMessages.LoggingError)
