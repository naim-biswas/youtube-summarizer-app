from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from youtube_transcript_api import YouTubeTranscriptApi
import json
import requests
import logging

# Load your OpenAI API key from an environment variable or secret management service
OPENAI_API_KEY = settings.OPENAI_API_KEY

# Configure logging
logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def summarize(request):
    if request.method == 'POST':
        try:
            # Debugging: log the request body
            logger.debug(f"Request body: {request.body}")

            # Ensure the content type is application/json
            if request.content_type != 'application/json':
                return JsonResponse({'error': 'Invalid content type. Expected application/json.'}, status=400)

            data = json.loads(request.body)
            video_url = data.get('url')
            if not video_url:
                return JsonResponse({'error': 'Missing "url" in request body.'}, status=400)

            logger.info(f"Received YouTube URL: {video_url}")

            # Extract video ID from the YouTube URL
            video_id = extract_video_id(video_url)
            if not video_id:
                return JsonResponse({'error': 'Invalid YouTube URL format.'}, status=400)

            logger.info(f"Extracted video ID: {video_id}")

            # Fetch the transcript of the video
            transcript = get_video_transcript(video_id)

            # Summarize the transcript using OpenAI API
            if transcript:
                summary = summarize_text(transcript)
                return JsonResponse({'summary': summary})
            else:
                return JsonResponse({'error': 'Failed to fetch video transcript.'}, status=500)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format.'}, status=400)
        except Exception as e:
            logger.error(f"Error in summarizing video: {e}")
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

def extract_video_id(url):
    """
    Extract the video ID from a YouTube URL.
    """
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
    except Exception as e:
        logger.warning(f"Manually created transcript not found: {e}")
        try:
            transcript = transcript_list.find_generated_transcript(['en'])
        except Exception as e:
            logger.error(f"Generated transcript not found: {e}")
            raise Exception("No suitable transcript found.")
    
    full_transcript = " ".join([part['text'] for part in transcript.fetch()])
    return full_transcript

def summarize_text(text):
    endpoint = "https://api.openai.com/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {OPENAI_API_KEY}'
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": f"Summarize the following YouTube video transcript:\n\n{text}"}],
        "temperature": 0.7
    }
    response = requests.post(endpoint, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content']
    else:
        response.raise_for_status()
