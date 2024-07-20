from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional
import time

@dataclass
class BaseReply:
    to_user_name: str
    from_user_name: str
    create_time: int = int(time.time())
    
    @abstractmethod
    def to_dict(self) -> dict:
        pass

@dataclass
class TextReply(BaseReply):
    content: str
    msg_type: str = "text"
    
    def to_dict(self) -> dict:
        return {
            "ToUserName": self.to_user_name,
            "FromUserName": self.from_user_name,
            "CreateTime": self.create_time,
            "MsgType": self.msg_type,
            "Content": self.content
        }

@dataclass
class ImageReply(BaseReply):
    media_id: str
    msg_type: str = "image"
    
    def to_dict(self) -> dict:
        return {
            "ToUserName": self.to_user_name,
            "FromUserName": self.from_user_name,
            "CreateTime": self.create_time,
            "MsgType": self.msg_type,
            "Image": {
                "MediaId": self.media_id
            }
        }

@dataclass
class Article:
    title: str
    description: str
    pic_url: str
    url: str

@dataclass
class NewsReply(BaseReply):
    articles: List[Article]
    msg_type: str = "news"
    
    def to_dict(self) -> dict:
        return {
            "ToUserName": self.to_user_name,
            "FromUserName": self.from_user_name,
            "CreateTime": self.create_time,
            "MsgType": self.msg_type,
            "ArticleCount": len(self.articles),
            "Articles": [
                {
                    "Title": article.title,
                    "Description": article.description,
                    "PicUrl": article.pic_url,
                    "Url": article.url
                } for article in self.articles
            ]
        }

class ReplyFactory:
    @staticmethod
    def create_text_reply(to_user: str, from_user: str, content: str) -> TextReply:
        return TextReply(to_user_name=to_user, from_user_name=from_user, content=content)
    
    @staticmethod
    def create_image_reply(to_user: str, from_user: str, media_id: str) -> ImageReply:
        return ImageReply(to_user_name=to_user, from_user_name=from_user, media_id=media_id)
    
    @staticmethod
    def create_news_reply(to_user: str, from_user: str, articles: List[Article]) -> NewsReply:
        return NewsReply(to_user_name=to_user, from_user_name=from_user, articles=articles)