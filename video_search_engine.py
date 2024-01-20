from dataclasses import dataclass
from typing import Dict, List
from dotenv import dotenv_values
from googleapiclient.discovery import build
from pytube import YouTube
import uuid


@dataclass
class Thumbnail:
    url: str
    width: int
    height: int

@dataclass
class Thumbnails:
    default: Thumbnail
    medium: Thumbnail
    high: Thumbnail

@dataclass
class Snippet:
    publishedAt: str
    channelId: str
    title: str
    description: str
    thumbnails: Thumbnails
    channelTitle: str
    liveBroadcastContent: str
    publishTime: str

@dataclass
class ID:
    kind: str
    videoId: str

@dataclass
class SearchResult:
    kind: str
    etag: str
    id: ID
    snippet: Snippet

URL = str
Success = bool

def parse_youtube_response(data: Dict) -> SearchResult:
    thumbnail_data = data['snippet']['thumbnails']
    thumbnail_objs = Thumbnails(
        default=Thumbnail(**thumbnail_data['default']),
        medium=Thumbnail(**thumbnail_data['medium']),
        high=Thumbnail(**thumbnail_data['high'])
    )

    snippet_data = {key: value for key, value in data['snippet'].items() if key != 'thumbnails'}
    snippet = Snippet(**snippet_data, thumbnails=thumbnail_objs)

    id_obj = ID(**data['id'])

    return SearchResult(kind=data['kind'], etag=data['etag'], id=id_obj, snippet=snippet)

def search_youtube(key_words: List[str]) -> List[URL]:
    config = dotenv_values(".env") 
    api_key = config['YOUTUBE_API_KEY']
    youtube = build('youtube', 'v3', developerKey=api_key)
    keywords = ' '.join(key_words)
    request = youtube.search().list(
        q=keywords,
        part='snippet',
        type='video',
        maxResults=10
    )
    response = request.execute()
    video_urls = []
    for item in response['items']:
        video = parse_youtube_response(item)
        video_id = video.id.videoId
        video_urls.append(f'https://www.youtube.com/watch?v={video_id}')
    return video_urls

def download_youtube_video(url: URL) -> str | None:
    file_name = str(uuid.uuid4())
    try:
        yt = YouTube(url)
        video_stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        if video_stream is None:
            return None
        video_name = f'{file_name}.mp4'
        video_stream.download(filename=video_name)
        return video_name
    except Exception as e:
        return None
