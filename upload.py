from googleapiclient.http import MediaFileUpload
import pandas as pd
from google_apis import create_service

def video_categories():
    video_categories = service.videoCategories().list(part='snippet', regionCode='US').execute()
    df = pd.DataFrame(video_categories.get('items'))
    return pd.concat([df['id'], df['snippet'].apply(pd.Series)[['title']]], axis=1)

API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube']
# SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
client_file = 'client_secrets.json'
service = create_service(client_file, API_NAME, API_VERSION, SCOPES)


"""
Step 1. Uplaod Video
"""
def subida(video, title, description,tags):
    request_body = {
        'snippet': {
            'title': title,
            'description': description,
            'categoryId': 27,
            'tags': [tags]
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': False
        },
        'notifySubscribers': False
    }

    video_file = video
    media_file = MediaFileUpload(video_file)
    # print(media_file.size() / pow(1024, 2), 'mb')
    # print(media_file.to_json())
    # print(media_file.mimetype())

    response_video_upload = service.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=media_file
    ).execute()
    uploaded_video_id = response_video_upload.get('id')

