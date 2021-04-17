import datetime
class Diary:
    jours_semaine = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    def __init__(self, corps: str, dateComplet:str = None):
        dateComplet = str(dateComplet)
        weekdayNumber: int = datetime.date(eval(dateComplet.split("-")[0]), eval(Diary.f(dateComplet.split("-")[1])), eval(Diary.f(dateComplet.split("-")[2]))).weekday()
        self.__jour: str = Diary.jours_semaine[int(weekdayNumber)]

        self.__corps: str = corps
        self.__dateComplet: str = dateComplet

    @staticmethod
    def f(d:str):
        if d[0] == "0":
            return d[1]
        return d

    def getCorps(self):
        return self.__corps
        
    def getDateComplet(self):
        return self.__dateComplet

    def setDateComplet(self, dateComplet:str):
        self.__dateComplet = dateComplet

    def setCorps(self, corps:str):
        self.__corps = corps
