from django.shortcuts import render
import requests
# Create your views here.import os
from django.shortcuts import render
from django.http import JsonResponse
from openai import OpenAI
from django.conf import settings
import json
import requests
from django.views.decorators.csrf import csrf_exempt
from youtube_transcript_api import YouTubeTranscriptApi

# Load your OpenAI API key from an environment variable or secret management service
OPENAI_API_KEY = settings.OPENAI_API_KEY

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def summarize(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        video_url = data['url']
        print("youtube: ", video_url)

        # Extract video ID from the YouTube URL
        video_id = extract_video_id(video_url)
    

        # Fetch the transcript of the video
        transcript = get_video_transcript(video_id)

        # Summarize the transcript using OpenAI API
        if transcript:
            summary = summarize_text(transcript)
            return JsonResponse({'summary': summary})
        else:
            return JsonResponse({'error': 'Failed to fetch video transcript.'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

def extract_video_id(url):
    """
    Extract the video ID from a YouTube URL.
    """
    # Example URL formats:
    # https://www.youtube.com/watch?v=video_id
    # https://youtu.be/video_id
    # https://www.youtube.com/embed/video_id
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be" in url:
        return url.split("/")[-1]
    elif "embed" in url:
        return url.split("/")[-1]
    else:
        return None

def get_video_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_manually_created_transcript(['en'])
    except:
        try:
            transcript = transcript_list.find_generated_transcript(['en'])
        except:
            raise Exception("No suitable transcript found.")
    
    full_transcript = " ".join([part['text'] for part in transcript.fetch()])

    return full_transcript


# In a utils.py or wherever you prefer in your Django app


def summarize_text(text):
    endpoint = "https://api.openai.com/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {OPENAI_API_KEY}'
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": f"Summarize the following Youtube video transcript:\n\n{text}",}],
        "temperature": 0.7
    }
    response = requests.post(endpoint, headers=headers, json=data)
    print("response: ", response)
    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content']
    else:
        response.raise_for_status()