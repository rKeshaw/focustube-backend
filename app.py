import json
import yt_dlp
from flask import Flask, request, jsonify
from flask_cors import CORS

# Initialize the Flask application
app = Flask(__name__)
# Configure Cross-Origin Resource Sharing to allow our front-end to connect
CORS(app, resources={r"/*": {"origins": "*"}})

# A simple 'health check' route for the server to confirm it's running
@app.route('/')
def health_check():
    return jsonify({'status': 'healthy'}), 200

# The main route that fetches the video stream URL
@app.route('/getVideo', methods=['GET'])
def get_video_stream():
    try:
        video_id = request.args.get('videoId')
        if not video_id:
            return jsonify({'error': 'Missing videoId.'}), 400

        youtube_url = f"https://www.youtube.com/watch?v={video_id}"
        
        # yt-dlp options to get the best video+audio stream
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'quiet': True,
        }

        # Extract the video information
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            stream_url = info.get('url')
            if not stream_url:
                raise Exception('No stream URL found by yt-dlp.')

            return jsonify({'streamUrl': stream_url})

    except Exception as e:
        print(f"CRITICAL BACK-END FAILURE: {e}")
        return jsonify({'error': 'The back-end failed to process the request.', 'details': str(e)}), 500

if __name__ == "__main__":
    # This part allows you to run the app locally for testing if you have Python installed
    app.run(host='0.0.0.0', port=8080)
