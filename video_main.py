import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('GOOGLE_API_KEY')
VIDEO_ID = os.getenv('VIDEO_ID')
WAIT_TIME = 10  # Tempo de espera em segundos

params = {
    "part": "snippet",
    "videoId": VIDEO_ID,
    "key": API_KEY,
    "maxResults": 100  # Pega até 100 comentários por página
}

def get_video_comments():
    comments = []
    next_page_token = None

    while True:
        if next_page_token:
            params["pageToken"] = next_page_token
        
        response = requests.get("https://www.googleapis.com/youtube/v3/commentThreads", params=params)
        data = response.json()

        if "items" not in data:
            print("Nenhum comentário encontrado")
            break
        
        for item in data["items"]:
            comment = item["snippet"]["topLevelComment"]
            author = comment["snippet"]["authorDisplayName"]
            message = comment["snippet"]["textDisplay"]
            like_count = comment["snippet"]["likeCount"]
            time = comment["snippet"]["publishedAt"]
            comments.append({"author": author, "message": message, "like_count": like_count, "time": time})

        next_page_token = data.get("nextPageToken")
        if not next_page_token:
            break
    
    output_file = "youtube_comments.json"
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(comments, file, ensure_ascii=False, indent=4)

    print(f"Total de comentários coletados: {len(comments)}")
    print(f"Comentários salvos em: {output_file}")


if __name__ == "__main__":
    get_video_comments()