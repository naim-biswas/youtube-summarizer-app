function summarizeVideo() {
    const videoUrl = document.getElementById('videoUrl').value;
    const summaryElement = document.getElementById('summary');
    
    // Display the loading message
    summaryElement.style.display = 'block';
    summaryElement.innerHTML = '<p>The summary is being generated. Please wait...</p>';

    fetch('/summarize/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ url: videoUrl }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.summary) {
            summaryElement.innerHTML = `<p>${data.summary}</p>`;
        } else if (data.error) {
            summaryElement.innerHTML = `<p>${data.error}</p>`;
        }
        // Clear the input field
        document.getElementById('videoUrl').value = '';
    })
    .catch(error => {
        console.error('Error:', error);
        summaryElement.innerHTML = '<p>Failed to generate summary. Please try again later.</p>';
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}