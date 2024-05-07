# -*- coding:utf-8 -*-

from datetime import datetime
from typing import Any, List, Optional, Union

from pydantic import BaseModel, Field


class Response(BaseModel):
    code: Optional[int] = 0
    msg: Optional[str] = "success"
    data: Optional[Any] = None

class TextSettings(BaseModel):
    seed: int = -1
    duration: int = 4
    aspect_ratio: str = Field( 
        default="16:9",
        description="",
    )
    resolution: int = 720

class TextConfigs(BaseModel):
    pass

class DescriptionTextGenerateParam(BaseModel):
    """Generate by Text with Video Description"""

    config: TextConfigs
    is_public: bool = True
    settings: TextSettings
    prompt: str = Field(
        default="",
        description="Placeholder, keep it as an empty string, do not modify it",
    )

#图和视频生成视频时需要传入config字段描述上传的文件信息
'''
{
    "prompt":"实验室发生爆炸",
    "settings":{
        "seed":-1,
        "duration":2,
        "resolution":720,
        "aspect_ratio":1.7777777777777777
    },
    "is_public":true,
    "config":{
        "source_image":"gs://haiper_vb/u/662fd23eb66ade4501f0bd5b/2024-05-07T07-09-16-98a04634.png",
        "input_content_type":"image",
        "input_width":512,
        "input_height":512
    }
}
'''
class ImageConfigs(BaseModel):
    input_content_type: str = Field(
        default="image",
        description=""
    )
    input_height: int
    input_width: int
    source_image: str

class ImageSettings(BaseModel):
    seed: int = -1
    duration: int = 4
    aspect_ratio: float = 1.7777777777777777
    resolution: int = 720

class DescriptionImageGenerateParam(BaseModel):
    """Generate by Image with Video Description"""

    config: ImageConfigs
    is_public: bool = True
    settings: ImageSettings
    prompt: str = Field(
        default="",
        description="Placeholder, keep it as an empty string, do not modify it",
    )

'''
    {
        "prompt":"(((Lego style))), lego movie style, bright colours, block building style, ",
        "settings":
        {
            "seed":-1,
            "resolution":720,
            "strength":1,
            "aspect_ratio":1.7777777777777777
        },
        "is_public":true,
        "config":
        {
            "source_video":"gs://haiper_vb/jobs/662fd23eb66ade4501f0bd5b/663a0e8c359063fa61db4214/converted_video.mp4",
            "input_content_type":"video",
            "input_width":1280,
            "input_height":720,
            "clicks":[[[208,227],[203,192],[272,229]],[1,1,1]]
        }
    }
'''
class VideoConfigs(BaseModel):
    input_content_type: str = Field(
        default="video",
        description=""
    )
    input_height: int = 1280
    input_width: int = 720
    source_video: str
    clicks: list

class VideoSettings(BaseModel):
    seed: int = -1
    aspect_ratio: float = 1.7777777777777777
    resolution: int = 720
    strength: int = 1

class DescriptionVideoGenerateParam(BaseModel):
    """Generate by Video with Video Description"""

    config: VideoConfigs
    is_public: bool = True
    settings: VideoSettings
    prompt: str = Field(
        default="",
        description="Placeholder, keep it as an empty string, do not modify it",
    )

class UploadParam(BaseModel):
    '''upload param'''
    ext: str = Field(
        default="png",
        description="picture or video: png, mp4..."
    )
    content_type: str = Field(
        default="image/png",
        description="content type: image/png, video/mp4"
    )

class UploadValue(BaseModel):
    url: str
    key: str

class UploadResponse(BaseModel):
    status: str
    value: UploadValue