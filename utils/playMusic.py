import threading

from playsound import playsound


class PlayMusic:
    music_path= "sound"

    @classmethod
    def chaosu(self):

        PlayMusic.playMusic(PlayMusic.music_path + "/" +"速度过快.mp3")

    @classmethod
    def playMusic(self,musicPath):
        def run(path):
            if not path:
                return
            playsound(path)

        param = {"path": musicPath}
        thread = threading.Thread(target=run,kwargs=param)
        thread.setDaemon(True)
        thread.start()

