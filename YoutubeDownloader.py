from pytube import YouTube
from tqdm import tqdm
import os
import time


def download_high_quality_video(url, output_path='./'):
    try:
        # Create a YouTube object
        yt = YouTube(url)

        # Get all available streams
        all_streams = yt.streams.filter(progressive=True, file_extension='mp4')

        # Filter streams for 1080p resolution
        video_stream = all_streams.filter(res='1080p').first()

        if not video_stream:
            # If no 1080p stream, try 720p
            video_stream = all_streams.filter(res='720p').first()

        if video_stream:
            # Get the total file size
            total_size = video_stream.filesize

            # Initialize tqdm with total file size
            progress_bar = tqdm(total=total_size, unit='B', unit_scale=True, ncols=100, ascii=True)

            # Download the video
            temp_filename = 'temp_video.mp4'
            temp_filepath = os.path.join(output_path, temp_filename)
            video_stream.download(output_path, filename=temp_filename)

            # Update progress bar manually based on download progress
            while os.path.exists(temp_filepath + '.part'):
                time.sleep(1)  # Adjust sleep interval if needed
                downloaded_size = os.path.getsize(temp_filepath)
                progress_bar.update(downloaded_size - progress_bar.n)

            # wait until it reaches 100%

            while progress_bar.n < total_size:
                time.sleep(1)
                progress_bar.update(total_size - progress_bar.n)

            # Rename the downloaded file to remove ".part" extension
            final_filename = os.path.splitext(temp_filename)[0] + '.mp4'
            final_filepath = os.path.join(output_path, final_filename)
            os.rename(temp_filepath, final_filepath)
           
            #Close progress bar 
            
            print("Download successful!")
            progress_bar.close()
        else:
            print("No suitable video stream available.")
    except Exception as e:
        print("An error occurred:", str(e))


if __name__ == "__main__":
    youtube_url = input("Enter the YouTube URL: ")
    output_folder = input("Enter the output folder (default is current directory): ")

    if output_folder:
        download_high_quality_video(youtube_url, output_folder)
    else:
        download_high_quality_video(youtube_url)
