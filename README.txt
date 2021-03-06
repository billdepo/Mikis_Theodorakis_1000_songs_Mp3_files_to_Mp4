A Python app to combine:
- audio tracks
- images
- text (description, title etc)

to create video files and publish to a YouTube Channel using the YouTube API.

Here we converted almost 1000 songs (mp3 files) to mp4 video files from the legendary Greek composer Mikis Theodorakis and later uploaded them to YouTube. 

Required packages:

- mutagen
- Pillow
- moviepy
- pandas

________________________
main.py:
________________________
- Goes through a number of subdirectories with audio tracks (mp3 files)
  
  mp3 directory format:
  --- Audio_tracks
          | --- THEODORAKIS MIKIS 52 CD (could be any name or multiple subdirectories)
                    | --- Mikis Theodorakis CD01
                              | --- 01 track title.mp3
                              | --- 02 track title.mp3
                               ...
                              | --- 18 track title.mp3
                              | --- 1000 Cover.jpg
                    | --- Mikis Theodorakis CD02
                            | --- ...
                     ...
                    | --- Mikis Theodorakis CD52 (could be any name for the subdirectories)
                    
- Extract information from mp3 files and saves the info in a dataframe which is then exported as an .xlsx file ("df_saved.xlsx"):
  - CD number
  - track number
  - CD path
  - track path
  - songs list
  - image file
  - title
  - singer
  - video path (where it will be stored once generated)
  - video created flag (TRUE / FALSE)
  - description
  
- Finally, combine the mp3 files with the CD folder's image of each audio track (mp3) to generate a video file in .mp4 format. Directory where generated videos are stored:
  --- Video_tracks


________________________
upload_video.py:
________________________

- Script to upload a single video file on YouTube channel
- Authentication to YouTube API happens by using a local json file "client_secrets.json"
- Arguments are given when running the script (video_path, video_title, video_description, video_keywords/tags)

________________________
stixoi_info_song_titles_and_urls.xlsx:
________________________

- Excel file with 124,574 records extracted from stixoi.info with the lyrics url of the song and its title (converted to capital letters and removed accentuation). This way one can search for the title of the song they are intrested in and easily access the relavant html page from stixoi.info and subsequently extract the lyrics.
