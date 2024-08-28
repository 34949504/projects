import subprocess
import datetime
import random




#Quiero que puede extraer un frame en un tiempo expecifico y guardarlo
#Preguntar varias veces por un mismo video

class Extractor():
    def __init__(self):
        self.time = "00:00:00"

        self.sec = "00"
        self.hr = "00"
        self.min = "00"
        self.frame_name = ""
        self.file_location = []
        self.folder_location = "C:\\Users\\gerar\\Documents\\frame_collector\\"
        self.minute_nd_hr = True


        self.sufijo = ""
        self.timestamps = []



    def asking(self):

        chose = input("Extraer 1 frame de un video(0)\nExtraer varios frames de un video(1)")


        if chose == "0":
            self.oneframe()

        elif chose == "1":
            self.variosframe()



    def variosframe(self):
        self.multiple_frames()
        count = 0
        for i in self.timestamps:
            h = i[0]
            m = i[1]
            s = i[2]

            subprocess.run(["ffmpeg","-i",f'{self.file_location[0]}',"-ss",f"{h}:{m}:{s}","-vframes","1",f"{self.folder_location}{self.sufijo + str(count)}.png"])
            count +=1


    def oneframe(self):
        self.asking_info()
        for i in self.file_location:
            s = self.sec
            h = self.hr
            m = self.min

            subprocess.run(["ffmpeg","-i",f'{i}',"-ss",f"{h}:{m}:{s}","-vframes","1",f"{self.folder_location}{self.frame_name}"])

            self.file_location = []


    def asking_info(self):

        self.file_location.append(input("Entra la dirección del video: "))
        self.frame_name = input("Entra el nombre del frame o enter: ")
        if self.frame_name == "":
            now = datetime.datetime.now()
            timestamp = int(now.timestamp())
            timestamp = int(timestamp + random.randint(0,1000) / (random.randint(1,10)))
            self.frame_name =f"frame_{timestamp}.png"





        self.sec = input("Escribe el segundo(0-59): ")
        self.min = input("Escriba el minuto(0-59) o enter: ")
        if self.min != "":
            self.minute_nd_hr = False
            self.hr = input("Escriba la hora(0-59): ")

        else:

            self.min = "00"



    def multiple_frames(self):
        self.file_location.append(input("Entra la dirección del video: "))
        self.sufijo = input("Entra sufijo: ")
        ton = True

        while ton:
            self.sec = input("Escribe el segundo(0-59) o exit: ")
            if self.sec == "exit":
                ton = False
                break
            self.min = input("Escriba el minuto(0-59) o enter: ")
            if self.min != "":
                self.minute_nd_hr = False
                self.hr = input("Escriba la hora(0-59): ")

            else:

                self.min = "00"
                self.hr = "00"


            self.timestamps.append(self.formating(self.hr,self.min,self.sec))
            print("\n\n")








    def formating(self,hr,min,secs):

        if int(secs) < 10:
            secs = f"0{int(secs)}"

        try:
            if int(min) < 10:
                min = f"0{int(min)}"
        except:pass
        try:
            if int(hr) < 10:
                hr = f"0{int(hr)}"
        except:pass

        return (hr,min,secs)




bo = Extractor()
bo.asking()





