# YouTube Video Summarizer

This project is a web application that summarizes YouTube videos. It uses the YouTube Transcript API to fetch the transcript of a video and then uses OpenAI to generate a summary of the transcript.
<br/>
Link: https://youtube-summarizer-fbe026bb7c16.herokuapp.com/

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need to have Python and Django installed on your machine. You also need to have an OpenAI API key and a YouTube Data API key.

### Installing

1. Clone the repository:
    ```bash
    git clone https://github.com/naim-biswas/youtube-video-summarizer.git
    ```

2. Navigate to the project directory:
    ```bash
    cd youtube-video-summarizer
    ```

3. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Set the environment variables `SECRET_KEY` and `OPENAI_API_KEY'.

5. Run the Django server:
    ```bash
    python manage.py runserver
    ```

Now you should be able to access the application at `localhost:8000`.

## Deployment

This application is currently deployed on Heroku.<br/>
Link: https://youtube-summarizer-fbe026bb7c16.herokuapp.com/

## Built With

* [Django](https://www.djangoproject.com/) - The web framework used
* [OpenAI](https://openai.com/) - Used to generate the summaries
* [YouTube Transcript API](https://github.com/jdepoix/youtube-transcript-api) - Used to fetch the video transcripts

## Authors

* **Your Name** - *Initial work* - [Naim Biswas](https://github.com/naim-biswas)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
