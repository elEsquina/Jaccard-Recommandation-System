import json 
from typing import Optional
from functools import total_ordering
from my_exceptions import *
from my_datastructures import Array, Heap, Stack
from recommendation_core import jacard_calculation, extract_keywords, ratio_additivity


def GenerateID(x): 
    """An ID generator.

    Args:
        x (int): Starting value for ID generation.

    Yields:
        int: The generated ID.
    """

    while True:
        yield x
        
        x += 1
        with open("RuntimeID.json", "w") as file:
            json.dump(x, file)


def handle_login_error(func) -> callable:
    """Decorator to handle login errors.

    Args:
        func (callable): The function to be decorated.

    Returns:
        callable: The decorated function.
    """

    def wrapper(*args, **kwargs):
        if Session.get_session().current_user is None:
            raise LoggingError()
        
        return func(*args, **kwargs) 

    return wrapper


class Video:
    def __init__(self, name: str, owner_id: int, id: int) -> None:
        """Initialize a Video object.

        Args:
            name (str): The name of the video.
            owner_id (int): The ID of the video owner.
            id (int): The ID of the video.
        """

        self.set_name(name)
        self.set_owner_id(owner_id)

        self.id = id    
        self.likes = 0
        self.dislikes = 0
        self.views = 0
        self.tags = Array(str)
         

    def is_author(self, user_ID: int) -> bool :
        """Check if the user owns this video.

        Args:
            user_ID (int): The ID of the user to check.

        Returns:
            bool: True if the user owns the video, False otherwise.
        """ 

        if not str(user_ID) in Session.get_session().registered_users:
            print(ErrorMessages.UserNotFound.format(str(user_ID)))
            return False

        return user_ID == self.get_owner_id() 
        

    #Setters: 
    def set_name(self, new_name: str) -> None :
        if new_name == " " or new_name == "":
            raise ValueError(ErrorMessages.InvalidName)
        
        self.name = new_name 
    
    def set_owner_id(self, new_owner_id: int) -> None:
        self.owner_id = new_owner_id 
    
    #Getters:
    def get_name(self) -> str:
        return self.name
    
    def get_id(self) -> int:
        return self.id
    
    def get_owner_id(self) -> int:
        return self.owner_id 
    
    def get_likes(self) -> int:
        return self.likes
    
    def get_dislikes(self) -> int:
        return self.dislikes
    
    def get_views(self) -> int:
        return self.views
    

    def __repr__(self) -> str :
        """Return a string representation of the video.

        Returns:
            str: The string representation of the video.
        """  

        tags_string = ", ".join([self.tags[index] for index in range(len(self.tags))])

        return f"""Name: {self.get_name()}
ID: {self.get_id()}
Owner id:{self.get_owner_id()}
Likes: {self.get_likes()}
Dislikes: {self.get_dislikes()}
Views: {self.get_views()}
Tags: {tags_string}""" 


class User:
    def __init__(self, name: str, id: int) -> None:
        """Initialize a User object.

        Args:
            name (str): The name of the user.
            id (int): The ID of the user.
        """ 

        self.set_name(name)

        self.id = id
        self.video_count = 0 
        self.subscriber_count = 0
        self.tags = [] 
        self.uploaded_videos = []
        self.subscribed_to = []
        self.watch_history = Stack()

        #Storage: 
        self.session = Session.get_session()
        self.registered_videos = Session.get_session().registered_videos
        self.registered_users = Session.get_session().registered_users
        self.__password = None
        
        
    def upload(self, title: str) -> Video:
        """Add a video with a specific title to the system.

        Args:
            title (str): The title of the video.

        Returns:
            Video: The uploaded video object.
        """

        made_id = self.session.get_id()
        video = Video(title, self.get_id(), made_id)

        keywords = extract_keywords(title)
        video.tags = Array(str, len(keywords) + 1)
        
        for index, keyword in enumerate(keywords):
            video.tags[index] = keyword

        self.registered_videos[str(made_id)] = video 
        self.uploaded_videos.append(int(made_id))
        self.video_count += 1

        print(SysMessages.Upload.format(str(made_id)))
        return video 


    def unupload(self, video_ID: int) -> None:
        """Remove the video with a specific ID from the system.

        Args:
            video_ID (int): The ID of the video to remove.

        Raises:
            ValueError: If the video is not found or not owned by the user.
        """
        
        if not str(video_ID) in self.uploaded_videos:
            raise ValueError(ErrorMessages.VideoNotFound.format(str(video_ID)))

        if not self.registered_videos[str(video_ID)].is_author(self.get_id()):
            raise ValueError(ErrorMessages.VideoNotOwned)

        self.uploaded_videos.remove(int(video_ID))
        del self.registered_videos[str(video_ID)]
        self.video_count-=1

        print(SysMessages.Unupload)
                
  
    def like(self, video_ID: int) -> None :
        """Add a like to the video with a specific ID.

        Args:
            video_ID (int): The ID of the video to like.

        Raises:
            ValueError: If the video is not found.
        """

        if not str(video_ID) in self.registered_videos:
            raise ValueError(ErrorMessages.VideoNotFound.format(str(video_ID)))        

        print(SysMessages.Liked.format(str(video_ID)))

        self.registered_videos[str(video_ID)].likes += 1
        
         
    def dislike(self, video_ID: int) -> None :
        """Add a dislike to the video with a specific ID.

        Args:
            video_ID (int): The ID of the video to dislike.

        Raises:
            ValueError: If the video is not found.
        """


        if not str(video_ID) in self.registered_videos:
            raise ValueError(ErrorMessages.VideoNotFound.format(str(video_ID)))
        
        print(SysMessages.Disliked.format(str(video_ID)))

        self.registered_videos[str(video_ID)].dislikes += 1
           
                
    def subscribe(self, user_ID: int) -> None:
        """Subscribe to a user with a specific ID.

        Args:
            user_ID (int): The ID of the user to subscribe to.

        Raises:
            ValueError: If the user is not found or already subscribed.
        """

        if not str(user_ID) in self.registered_users:
            raise ValueError(ErrorMessages.UserNotFound.format(str(user_ID)))
        
        if not user_ID in self.subscribed_to:
            self.subscribed_to.append(int(user_ID))
            self.registered_users[str(user_ID)].subscriber_count += 1
            print(SysMessages.Subscribe.format(str(user_ID)))

        else:
            raise ValueError(ErrorMessages.SubscribeError)
            
             
    def unsubscribe(self, user_ID: int) -> None:
        """Unsubscribe from a user with a specific ID.

        Args:
            user_ID (int): The ID of the user to unsubscribe from.

        Raises:
            ValueError: If the user is not found or not subscribed.
        """

        if not str(user_ID) in self.registered_users:
            raise ValueError(ErrorMessages.UserNotFound.format(str(user_ID)))
        

        if user_ID in self.subscribed_to:
            self.subscribed_to.remove(user_ID)

            print(SysMessages.Unsubscribe.format(str(user_ID)))
            
        else:
            raise ValueError(ErrorMessages.SubscribeError)


    def watch_video(self, video_ID: int) -> None:
        """Simulate watching a video with a specific ID.

        Args:
            video_ID (int): The ID of the video to watch.

        Raises:
            ValueError: If the video is not found.
        """

        if not str(video_ID) in self.registered_videos:
            raise ValueError(ErrorMessages.VideoNotFound.format(str(video_ID)))
        
        self.watch_history.push(video_ID)
        
        video = self.registered_videos[str(video_ID)]
        video.views += 1
        
        print(SysMessages.Watch_video.format(str(video_ID)))

        for index in range(len(video.tags)):
            self.tags.append(video.tags[index])
        
        if len(self.tags) > 10:
            for val in self.tags[:len(self.tags) - 10]:
                if val in self.tags: self.tags.remove(val)
     
        
    def __repr__(self) -> str :
        """Return a string representation of the user.

        Returns:
            str: The string representation of the user.
        """ 

        uploaded_vids = ", ".join([self.registered_videos[str(id)].get_name() for id in self.uploaded_videos])
        subscribed_to = ", ".join([self.registered_users[str(id)].get_name() for id in self.subscribed_to])

        if uploaded_vids == '':
            uploaded_vids = "Nothing"
        if subscribed_to == '':
            subscribed_to = "No one"

        return f"""User: {self.get_name()}
ID: {self.get_id()}
Uploaded Videos: {uploaded_vids}
Subscribed To: {subscribed_to}
Video Count: {self.get_video_count()}
Subscriber Count: {self.get_subscriber_count()}"""


    #Setters
    def set_name(self, new_name: str) -> None :
        if new_name == " " or new_name == "":
            raise ValueError(ErrorMessages.InvalidName)
        
        self.name = new_name
    
    def set_password(self, new_password: str) -> None:
        if new_password == " " or new_password == "":
            raise ValueError(ErrorMessages.InvalidPassword)
        
        self.__password = new_password

    #Getters    
    def get_name(self) -> str:  
        return self.name
    
    def get_id(self) -> int:
        return self.id
    
    def get_video_count(self) -> int:
        return self.video_count
    
    def get_subscriber_count(self) -> int:
        return self.subscriber_count
    
    def get_password(self) -> str:
        return self.__password
    

class Session: #USES SINGLETON PATTERN TO ONLY INSTANTIATE ONE UNIQUE CLASS
    _instance = None

    @total_ordering
    class _entry: 
        def __init__(self, id: int, score: float) -> None:
            """Initialize an object with an ID and a score.

            Args:
                id (int): The ID associated with the object.
                score (float): The score associated with the object.
            """

            self.id = id 
            self.score = score 

        def __lt__(self, other):
            return self.score > other.score

        def __eq__(self, other):
            return self.score == other.score
            

    def __init__(self) -> None:
        """Initialize a Session object."""

        if not Session._instance is None:
            raise UnicityError(ErrorMessages.SessionUnicity)
        
        Session._instance = self 
        
        with open("RuntimeID.json", "r") as file:
            x = json.load(file)
            self.id_gen = GenerateID(int(x) + 2)

        self.current_user: User = None
        self.registered_videos = {}
        self.registered_users = {}
        self.load()
    

    def login(self, id: int, password: str) -> User:
        """Authenticate as a user to be simulated upon.

        Args:
            id (int): The ID of the user.
            password (str): The password of the user.

        Returns:
            User: The authenticated user.

        Raises:
            ValueError: If the user ID is not found or the password is incorrect.
        """

        if not str(id) in self.registered_users:
            raise ValueError(ErrorMessages.UserNotFound.format(str(id))) 
        
        fetched_user = self.registered_users[str(id)]
        if fetched_user.get_password() == password:
            self.current_user = fetched_user 

            print(SysMessages.LoggingSuccess.format(fetched_user.get_name()))
            return fetched_user
        
        print(SysMessages.WrongPassword)

    
    @handle_login_error
    def logout(self) -> None:
        """Logs out the user"""

        self.current_user = None
        print(SysMessages.Loggout)


    @handle_login_error
    def recommend(self, Query: Optional[str] = None) -> Heap:
        """Return the heap containing the recommendations.

        Args:
            Query (Optional[str], optional): To replace user's tags with the Query's. Defaults to None.

        Returns:
            Heap: The heap containing the recommendations.
        """

        return_heap = Heap(self._entry)

        tags_set: set
        if Query is None:
            tags_set = set(self.current_user.tags)
        else: 
            tags_set = set(extract_keywords(Query))
        
        for ID, video in self.registered_videos.items():
            score = jacard_calculation(tags_set, set(video.tags))
            score = ratio_additivity(score, video.get_likes(), video.get_dislikes(), video.get_views())
            
            return_heap.push(self._entry(ID, score))
        
        return return_heap      


    @handle_login_error
    def search(self, Query: str) -> Stack:
        """Return a stack containing videos with similar titles.

        Args:
            Query (str): The query to search for videos.

        Returns:
            Stack: The stack containing the videos.
        """

        heap = self.recommend(Query= Query)
        return_stack = Stack()
        for _ in range(15):
            return_stack.push(heap.pop())
        
        return return_stack.reverse()


    def create_account(self, username: str, password: str) -> User:
        """Create a user.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            User: The created user.
        """

        new_id = int(self.get_id())
        new_user = User(username, new_id) 

        new_user.set_password(password)
        self.registered_users[str(new_id)] = new_user 
        print(SysMessages.UserCreated.format(str(new_id)))
        
        return new_user


    @handle_login_error
    def delete_account(self, password: str) -> None:
        """Delete the user from the system and all their videos.

        Args:
            password (str): The password of the user.

        Raises:
            ValueError: If the password is incorrect.
        """

        user = self.current_user
        if user.get_password() == password:
            self.logout()
            del self.registered_users[str(user.get_id())]
            print(SysMessages.UserDeleted)

        else: 
            print(SysMessages.WrongPassword)


    def get_id(self) -> int:
        """Generate an ID.

        Returns:
            int: The generated ID.
        """

        return next(self.id_gen)


    def load(self) -> None:
        """Loads the dataset into the system"""

        with open("videos.json", "r") as file:
            #Video_ID: (title, like_count, dislike_count, views, OwnerID, [ *Tags ])
            for ID, misc in json.load(file).items():
                video_obj = Video(misc[0], misc[4], int(ID))

                video_obj.likes = misc[1]
                video_obj.dislikes = misc[2]
                video_obj.views = misc[3]

                video_obj.tags = Array(str, len(misc[-1]) + 1)
                
                for index in range(len(misc[-1])):
                    video_obj.tags[index] = misc[-1][index]

                self.registered_videos[str(ID)] = video_obj
        

        with open("users.json", "r") as file:
            #"ID": [name, video_count, subscriber_count, [TAGS], [SUBSCRIBED_TO], [UPLOADED_VIDEOS], [HISTORY], password]
            for ID, misc in json.load(file).items():
                user_obj = User(misc[0], int(ID))

                user_obj.video_count = misc[1]
                user_obj.subscriber_count = misc[2]
                user_obj.tags = misc[3].copy()
                user_obj.subscribed_to = misc[4].copy()
                user_obj.uploaded_videos = misc[5].copy()
                user_obj.set_password(misc[-1])

                for vid_id in reversed(misc[6]):
                    user_obj.watch_history.push(vid_id)
                
                self.registered_users[str(ID)] = user_obj
    

    def save(self) -> None:
        """Saves the system into the dataset"""

        registered_videos, registered_users = {
            ID: [obj.get_name(), obj.get_likes(), obj.get_dislikes(), obj.get_views(), 
                 obj.get_owner_id(), [obj.tags[index] for index in range(len(obj.tags))] ]

            for ID, obj in self.registered_videos.items()
        }, {
            ID: [obj.get_name(), obj.get_video_count(), obj.get_subscriber_count(), obj.tags.copy(), 
                 obj.subscribed_to.copy(), obj.uploaded_videos.copy(), [obj.watch_history.pop() for _ in range(len(obj.watch_history))], obj.get_password() ]

            for ID, obj in self.registered_users.items()
        }
        
        with open("videos.json", "w") as file:
            json.dump(registered_videos, file, indent=2)
        
        with open("users.json", "w") as file:
            json.dump(registered_users, file, indent=2)


    @staticmethod
    def get_session():
        """Get the session instance.

        Returns:
            Session: The session instance.
        """
        
        if Session._instance is None:
            Session()
            
        return Session._instance
    
