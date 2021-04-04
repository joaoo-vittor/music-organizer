import sys
import os
import pwd
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from interface.design import *
from musicOrganizer import OrganizeMusic


class MusicOrganizer(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        super().setupUi(self)
        self.nMusicasOrg.setDisabled(True)
        self.nMusicasOrg.setStyleSheet(
            "* {background: white; color: #000; font-weight: 700;}"
        )
        self.path = None

        if (sys.platform).lower() == 'linux':
            aux = pwd.getpwall()
            aux1 = aux[len(aux)-6]
            self.history_path = '/home/' + aux1.pw_name + '/Music/'
            self.path = self.history_path
            self.inputPath.setText(self.path)

        self.btnPath.clicked.connect(self.get_path)
        self.btnOrganizar.clicked.connect(self.organizer)

    def get_path(self):
        if str(sys.platform).lower() == 'linux':
            self.path = QFileDialog.getExistingDirectory(
                QFileDialog(),
                caption='Seleciona Uma Pasta',
                directory=self.path
            )

            if len(self.path) == 0:
                self.path = self.history_path

            if self.path[-1] != '/':
                self.path = self.path + '/'

            self.inputPath.setText(self.path)

    def organizer(self):
        if self.path != None and isinstance(self.path, str):
            try:
                org = OrganizeMusic(self.path)
                org.lowerMusicName()
                org.getArtist()
                org.createDir()
                org.moveMusic()
                qtd_musicas = len(org.music_path)
                self.nMusicasOrg.setText(str(qtd_musicas))
                org.deleteDirsEmpty()
            except Exception as e:
                self.nMusicasOrg.setText('Erro Inesperado!')


if __name__ == '__main__':
    qt = QApplication(sys.argv)
    musicOrg = MusicOrganizer()
    musicOrg.show()
    qt.exec_()
