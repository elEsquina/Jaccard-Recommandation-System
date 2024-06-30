from typing import Any
from my_classes import Session
from my_exceptions import UnicityError


class Shell:
    _instance = None

    class _Command:
        def __init__(self, func: callable) -> None:
            self.name = func.__name__
            self.doc = func.__doc__
            self.func = func

        def __call__(self, *args: Any, **kwds: Any) -> Any:
            return self.func(*args, **kwds)
    

    def __init__(self) -> None:
        if not Shell._instance is None:
            raise UnicityError()

        Shell._instance = self
        self.commands = []


    def __getitem__(self, key: str) -> callable:
        for event in self.commands:
            if event.name.lower() == key.lower():
                return event
        
        print(f"Command {key} was not found")
        return self["NOT_FOUND"]


    def on_command(self, inp) -> None:
        inp = inp.split(" ")

        if Session.get_session().current_user is None:
            cmd = inp[0].lower()

            if not (cmd == "login" or cmd == "create_account" or cmd == "help" or cmd == "quit"):
                print("First you got to login or create an account")
                self["help"]("login")
                self["help"]("create_account")
                return


        if len(inp) == 1:
            self[inp[0].lower()]()
        else:
            self[inp[0].lower()](*inp[1:])


    @staticmethod
    def get_shell():

        if Shell._instance is None:
            Shell()
        
        return Shell._instance
    

    @staticmethod
    def commandhandler(func):
        Shell.get_shell().commands.append(Shell._Command(func))

        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        
        return wrapper
    


class Facade: 
    session = Session.get_session()
    

    @staticmethod
    @Shell.commandhandler
    def help(command_name: str = None):
        """Command: help
        
        Description:
        Displays this message
        
        Usage:
        help [command_name (OPTIONAL)]

        Arguments: 
        command_name (Optional): The command you want to know more details about!
        """

        if not command_name is None:
            print(Shell.get_shell()[command_name].doc)
            return
        
        for command in Shell.get_shell().commands:
            if command.name.lower() == "NOT_FOUND".lower():
                continue
            
            print(command.doc)


    @staticmethod
    @Shell.commandhandler
    def login(id: int, password: str) -> None:
        """Command: login

        Description:
        Log in to the system with the specified user ID and password.

        Usage:
        login [id] [password]

        Arguments:
        [id]: The ID of the user.
        [password]: The password for the user.
        """

        Facade.session.login(int(id), password)


    @staticmethod
    @Shell.commandhandler
    def logout() -> None:
        """Command: logout

        Description:
        Log out from the current user session.

        Usage:
        logout
        """
        
        Facade.session.logout()


    @staticmethod
    @Shell.commandhandler
    def recommend(query: str = None) -> None:
        """Command: recommend

        Description:
        Get recommended videos based on the given query.

        Usage:
        recommend [query (OPTIONAL)]

        Arguments:
        [query]: (Optional) The query for video recommendations.
        """

        heap = Facade.session.recommend(query)
        i = 0
        while len(heap) != 0 and i < 30:
            vid_id = heap.pop().id
            print(Facade.session.registered_videos[vid_id], end="\n\n")
            i += 1


    @staticmethod
    @Shell.commandhandler
    def search(query: str) -> None:
        """Command: search

        Description:
        Search for videos based on the given query.

        Usage:
        search [query]

        Arguments:
        [query]: The query for video search.
        """

        stack = Facade.session.search(query)

        while len(stack) != 0:
            entry_ = stack.pop()
            vid_id = entry_.id
            print(Facade.session.registered_videos[vid_id], end="\n\n")


    @staticmethod
    @Shell.commandhandler
    def create_account(username: str, password: str) -> None:
        """Command: create_account

        Description:
        Create a new user account with the specified username and password.

        Usage:
        create_account [username] [password]

        Arguments:
        [username]: The username for the new account.
        [password]: The password for the new account.
        """

        Facade.session.create_account(username, password)
    

    @staticmethod
    @Shell.commandhandler
    def delete_account(password: str) -> None:
        """Command: delete_account

        Description:
        Delete the current user account.

        Usage:
        delete_account [password]

        Arguments:
        [password]: The password to confirm the account deletion.
        """

        Facade.session.delete_account(password)


    @staticmethod
    @Shell.commandhandler
    def quit():
        """Command: quit

        Description:
        Quit the application and save the current session.

        Usage:
        quit
        """
        
        Facade.session.save()
        exit()


    @staticmethod
    @Shell.commandhandler
    def upload(title: str) -> None:
        """Command: upload

        Description:
        Upload a new video with the specified title.

        Usage:
        upload [title]

        Arguments:
        [title]: The title of the video to upload.
        """

        Facade.session.current_user.upload(title)


    @staticmethod
    @Shell.commandhandler
    def unupload(video_ID: int) -> None:
        """Command: unupload

        Description:
        Remove the video with the specified ID from the system.

        Usage:
        unupload [video_ID]

        Arguments:
        [video_ID]: The ID of the video to remove.
        """
    
        Facade.session.current_user.unupload(int(video_ID))


    @staticmethod
    @Shell.commandhandler
    def like(video_ID: int) -> None:
        """Command: like

        Description:
        Add a like to the video with the specified ID.

        Usage:
        like [video_ID]

        Arguments:
        [video_ID]: The ID of the video to like.
        """

        Facade.session.current_user.like(int(video_ID))


    @staticmethod
    @Shell.commandhandler
    def dislike(video_ID: int) -> None:
        """Command: dislike

        Description:
        Add a dislike to the video with the specified ID.

        Usage:
        dislike [video_ID]

        Arguments:
        [video_ID]: The ID of the video to dislike.
        """

        Facade.session.current_user.dislike(int(video_ID))


    @staticmethod
    @Shell.commandhandler
    def subscribe(user_ID: int) -> None:
        """Command: subscribe

        Description:
        Subscribe to the user with the specified ID.

        Usage:
        subscribe [user_ID]

        Arguments:
        [user_ID]: The ID of the user to subscribe to.
        """
        
        Facade.session.current_user.subscribe(int(user_ID))


    @staticmethod
    @Shell.commandhandler
    def unsubscribe(user_ID: int) -> None:
        """Command: unsubscribe

        Description:
        Unsubscribe from the user with the specified ID.

        Usage:
        unsubscribe [user_ID]

        Arguments:
        [user_ID]: The ID of the user to unsubscribe from.
        """

        Facade.session.current_user.unsubscribe(int(user_ID))


    @staticmethod
    @Shell.commandhandler
    def watch_video(video_ID: int) -> None:
        """Command: watch_video

        Description:
        Simulate watching a video with the specified ID.

        Usage:
        watch_video [video_ID]

        Arguments:
        [video_ID]: The ID of the video to watch.
        """

        Facade.session.current_user.watch_video(int(video_ID))
    

    @staticmethod
    @Shell.commandhandler
    def info(id: int) -> None:
        """Command: info

        Description:
        Displays information based on the entered ID.

        Usage:
        info [id]

        Arguments:
        [id]: The ID of the thing you want to view information about.
        """

        if str(id) in Facade.session.registered_users:
            print(Facade.session.registered_users[str(id)])
        elif str(id) in Facade.session.registered_videos:
            print(Facade.session.registered_videos[str(id)])
        else:
            print("THE ID wasnt found in the system")


    @staticmethod
    @Shell.commandhandler
    def NOT_FOUND(*args):
        pass 


shell = Shell.get_shell()

hello = """
  _   _      _ _
 | | | |    | | |
 | |_| | ___| | | ___
 |  _  |/ _ \ | |/ _ \\
 | | | |  __/ | | (_) |
 |_| |_|\___|_|_|\___/

"""

print(hello)

print("=================================")
print("Type help for a list of commands!")
print("Type quit to save and exit!")
print("=================================\n\n\n")

while True:
    inp = input(">> ")

    try:
        shell.on_command(inp.lower())
    except Exception as e:
        print(e)

    print("===============\n")