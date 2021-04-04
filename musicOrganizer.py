import os
import shutil
import mutagen
import re


class OrganizeMusic:
    def __init__(self, path):
        self.origin_path = path
        self.list_artists = []
        self.music_path = []
        self.directories = []

        for i in os.listdir(self.origin_path):
            regex = re.compile('.mp3$', flags=re.IGNORECASE)
            aux = regex.search(i)
            if not aux:
                self.directories.append(i.lower())

    def lowerMusicName(self):
        for nome in os.listdir(self.origin_path):
            os.rename(self.origin_path + nome, self.origin_path + nome.lower())

    @staticmethod
    def getArrayArtist(path):
        try:
            artist = mutagen.File(path).tags.getall('TPE1')

            if len(artist) > 0:
                aux = mutagen.File(path).tags.getall('TPE1')[0][0]
                artist = aux
            else:
                artist = 'desconhecido'
        except Exception as e:
            return 'desconhecido'

        return artist

    def getArtist(self):
        for root, dirs, files in os.walk(self.origin_path):
            for file in files:
                old_file_path = os.path.join(root, file)
                artist = self.getArrayArtist(old_file_path)

                aux = artist.strip()
                self.list_artists.append(aux.lower())
                root = root if root[-1] == '/' else root + '/'

                new_file_path = root + aux.lower() + '/' + file

                if len(dirs) == 0:
                    for i in self.directories:
                        if i in new_file_path:
                            new_file_path = new_file_path.replace(i+'/', '')

                music = (old_file_path, new_file_path)
                self.music_path.append(music)

        self.list_artists = set(self.list_artists)
        self.list_artists = list(self.list_artists)

    def createDir(self):
        for dir_name in self.list_artists:
            new_name_dir = self.origin_path + dir_name
            os.mkdir(new_name_dir)

    def moveMusic(self):
        for value1, value2 in self.music_path:
            old_path = value1
            new_path = value2
            shutil.move(old_path, new_path)

    def deleteDirsEmpty(self):
        for dir in self.directories:
            path = self.origin_path + dir
            os.removedirs(path)
