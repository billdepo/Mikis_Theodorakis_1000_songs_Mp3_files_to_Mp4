# imports
import pandas as pd
import os
import glob
from mutagen.mp3 import MP3
from PIL import Image
from pathlib import Path
from moviepy import editor

# functions definition
def cd_number(audio_dir):
    """
    Extracts from a directory path the CDXX number and returns it
    """
    import re  # regular expression to search for CDXX format where XX any combination of natural numbers eg 00, 45, etc
    audio_dir = audio_dir.split('/')[-1]
    x = re.search(r"CD[0-9][0-9]", audio_dir)
    return x.group()


def get_cd_img_file(cd_path):
    """
    Input: CD path
    Returns: path of the jpg file in the CD directory that contains the list of songs for that particular CD
    """
    images_list = glob.glob(f'{cd_path}/*.jpg')
    return fix_path(images_list)  # just a single imagefile


def track_number(audio_path):
    """
    Input: audio file path
    Returns: Number of track in CD
    """
    # return audio_path.split('/')[-1][:2]
    import re
    x = re.search(r"[0-9][0-9]", audio_path.split('/')[-1])
    return x.group()


def fix_path(my_list):
    """
    Input: list of paths or single string path with Windows format (\\ instead of /)
    Output: fixed list of paths or single string containing only /
    """

    def replace_slash(path):
        '''replcae double backslashes in Windows paths to forward ones (compatible with UNIX)'''
        new_path = path.replace('\\', '/')
        return new_path

    if isinstance(my_list, list):  # if it's a list return the fixed list of items
        my_new_list = []
        for item in my_list:
            fixed_item = replace_slash(item)
            my_new_list.append(fixed_item)

        return my_new_list

    elif isinstance(my_list, str):  # if it's a string just return the fixed one
        return replace_slash(my_list)


def add_1000_cover_jpg_file_to_all_cds(df):
    """
    adds a 1000 Cover.jpg file to all existing CD paths if it's not already there
    This is useful to parse then the jpg files along with the mp3s to create video files combining the mp3s and jpgs
    """
    import shutil, os

    image_to_add = f"{df.loc[0, 'CD path']}/1000  Cover.jpg"

    for i in range(len(df)):
        cd_path = df.loc[i, 'CD path']

        # add the 1000 cover file if not already there
        if not os.path.isfile(f"{df.loc[i, 'CD path']}/1000  Cover.jpg"):
            shutil.copy(image_to_add, cd_path)

def parse_track(track_id, df, videos_dir):
    song_cd = df.loc[track_id, 'CD']
    song_track_num = df.loc[track_id, 'track']
    song_title = df.loc[track_id, 'title']
    song_singer = df.loc[track_id, 'singer']

    video_title = f'{song_title} - {song_singer}'
    video_description = f'1000 τραγούδια του Μίκη Θεοδωράκη\n\
                        {song_cd}\n\
                        Track {song_track_num}\n\
                        Title: {song_title}\n\
                        Music: Μίκης Θεοδωράκης\n\
                        Singer: {song_singer}\n\n\
                        Πραγματοποιείται μια προσπάθεια να ανέβουν στο youtube και τα περίπου 1000 τραγούδια του Μίκη Θεοδωράκη που συγκεντρώθηκαν από μια ομάδα φίλων\
                        της μουσικής του Μίκη στο http://mikis1000songs.blogspot.gr/ ώστε να φτάσουν τα τραγούδια του σε κάθε γωνιά της ελληνικής γης και σε κάθε πτυχή της ελληνικής ψυχής.\n\n\
                        ΑΠΟΠΟΙΗΣΗ: Το οπτικό και ηχητικό υλικό του βίντεο δε μου ανήκει. Το παρόν δημιουργήθηκε μόνο για λόγους ψυχαγωγίας και δεν αποσκοπεί σε παραβίαση πνευματικών δικαιωμάτων.'

    video_path = f'{videos_dir}/{song_cd}TR{song_track_num} {song_title} - {song_singer}.mp4'
    return (video_path, video_title, video_description)

#classes definition
'''
Creating class MP3ToMP4 which contains methods to convert
an audio to a video using a list of images.
'''

class MP3ToMP4:
    def __init__(self, folder_path, audio_path, video_path_name):
        """
        :param folder_path: contains the path of the root folder.
        :param audio_path: contains the path of the audio (mp3 file).
        :param video_path_name: contains the path where the created
                                video will be saved along with the
                                name of the created video.
        """
        self.folder_path = folder_path
        self.audio_path = audio_path
        self.video_path_name = video_path_name
        # Calling the create_video() method.
        self.create_video()
    def get_length(self):
        """
        This method reads an MP3 file and calculates its length
        in seconds.
        :return: length of the MP3 file
        """
        song = MP3(self.audio_path)
        return int(song.info.length)
    def get_images(self):
        """
        This method reads the filenames of the images present
        in the folder_path of type '.jpg' and stores it in the
        'images' list.
        Then it opens the images, resizes them and appends them
        to another list, 'image_list'
        :return: list of opened images
        """
        path_images = Path(self.folder_path)
        images = list(path_images.glob('*.jpg'))
        image_list = list()
        for image_name in images:
            image = Image.open(image_name).resize((800, 800), Image.ANTIALIAS)
            image_list.append(image)
        return image_list
    def create_video(self):
        """
        This method calls the get_length() and get_images()
        methods internally. It then calculates the duration
        of each frame. After that, it saves all the opened images
        as a gif using the save() method. Finally it calls the
        combine_method()
        :return: None
        """
        length_audio = self.get_length()
        image_list = self.get_images()
        duration = int(length_audio / len(image_list)) * 1000
        image_list[0].save(self.folder_path + "temp.gif",
                           save_all=True,
                           append_images=image_list[1:],
                           duration=duration)
        # Calling the combine_audio() method.
        self.combine_audio()
    def combine_audio(self):
        """
        This method attaches the audio to the gif file created.
        It opens the gif file and mp3 file and then uses
        set_audio() method to attach the audio. Finally, it
        saves the video to the specified video_path_name
        :return: None
        """
        video = editor.VideoFileClip(self.folder_path + "temp.gif")
        audio = editor.AudioFileClip(self.audio_path)
        final_video = video.set_audio(audio)
        final_video.write_videofile(self.video_path_name, fps=60)

if __name__ == '__main__':
    # initial values -- REQUIRED TO BE SET
    current_working_dir = os.getcwd()  # eg 'C:\\Users\\User\\Downloads\\Mp3toMp4'
    current_working_dir = fix_path(current_working_dir)  # covert windows-styled path to unix compatible (forward slashes)
    audio_file_type = 'mp3'  # initialization
    audio_dir_suffix = 'Audio_tracks'  # directory within our current working directory that audio files exist
    videos_dir = f'{current_working_dir}/Video_tracks' #select the path to save generated videos

    audio_dir = fix_path(f'{current_working_dir}/{audio_dir_suffix}')
    inner_dir = glob.glob(f'{audio_dir}/*')  # get any subdir
    inner_dir = fix_path(inner_dir)

    for item in inner_dir:  # for each inner dir search for final (last) dirs
        all_audio_dirs = glob.glob(f'{item}/*')
        all_audio_dirs = fix_path(all_audio_dirs)

    cd = []
    track = []
    cd_path = []
    track_path = []
    cd_songs_list_img = []

    for current_cd_path in all_audio_dirs:  # for each CD path in the list of all CD paths
        cd_num = cd_number(current_cd_path)
        cd_audio_tracks = glob.glob(f'{current_cd_path}/*.{audio_file_type}')  # gets all filetypes specified eg *.mp3
        cd_audio_tracks = fix_path(cd_audio_tracks)
        cd_list_img = get_cd_img_file(current_cd_path)

        for audio_track in cd_audio_tracks:  # for each track within each CD
            cd.append(cd_num)
            track.append(track_number(audio_track))
            cd_path.append(current_cd_path)
            track_path.append(audio_track)
            cd_songs_list_img.append(cd_list_img)

    df = pd.DataFrame({'CD': cd,
                       'track': track,
                       'CD path': cd_path,
                       'track path': track_path,
                       'CD songs list jpg': cd_songs_list_img
                       })

    track_title = []
    track_singer = []
    mp3_items = []

    for i in range(len(df)):
        track1 = df.loc[i]
        track1_mp3 = MP3(track1['track path'])
        track_title.append(track1_mp3['TIT2'])
        track_singer.append(track1_mp3['TPE1'])
        mp3_items.append(track1_mp3)

    df['title'] = track_title
    df['singer'] = track_singer
    df['mp3'] = mp3_items

    video_path = []
    video_title = []
    video_description = []

    for video in range(len(df)):
        path, title, description = parse_track(video, df, videos_dir)
        video_path.append(path)
        video_title.append(title)
        video_description.append(description)

    df['video title'] = video_title
    df['video description'] = video_description
    df['video path'] = video_path
    df['video created'] = None

    #create the video files
    for current_track in range(len(df)): #for all ~1000 songs
        folder_path = df.loc[current_track, 'CD path'] #'C:/Users/User/Downloads/Mp3toMp4/Audio_tracks/THEODORAKIS MIKIS  52 CD/' its the path of the CD where it will look in there for images
        audio_path = df.loc[current_track, 'track path'] #'C:/Users/User/Downloads/Mp3toMp4/Audio_tracks/THEODORAKIS MIKIS  52 CD/Mikis Theodorakis CD01/01 - -- ----- ---- - --------.-----S.mp3'

        videos_dir = f'{current_working_dir}/Video_tracks' #select the path to save generated videos
        video_path_name, video_title, video_description = parse_track(current_track, df, videos_dir)

        if os.path.isfile(video_path_name): #if there is already a video file created
            df.loc[current_track, 'video created'] = True #set the df to true
        else: #case video doesn't exist => we need to create it
            try:
                MP3ToMP4(folder_path, audio_path, video_path_name) # Invoking the parameterized constructor of the MP3ToMP4 class.
                df.loc[current_track, 'video created'] = True #if the video file is created update the df 'video created' column
            except:
                raise(f'Error while creating the video file for {audio_path}')

    #save dataframe with all the info to csv
    df.to_excel(f'{current_working_dir}/results_of_script.xlsx')