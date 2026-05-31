from typing import TypedDict, Annotated, Optional
from langgraph.graph.message import add_messages

class InstagramComments(TypedDict):
    username: str
    text: str

class InstagramUserInfo(TypedDict):
    bio: Optional[str]
    full_name: Optional[str]
    post_sayisi: Optional[int]
    takipci_sayisi: Optional[int]
    takip_sayisi: Optional[int]
    bio_linkleri: Optional[list]
    profil_pic: Optional[str]

class InstagramUserPosts(TypedDict):
    baslik: str
    like_count: int
    comment_count: int
    comments: Optional[list[InstagramComments]]

class InstagramState(TypedDict):
    messages: Annotated[list, add_messages]
    username: str
    user_general_info: Optional[InstagramUserInfo]
    user_medias: Optional[InstagramUserPosts]


