import datetime
class EmploiDuTempsDuJour(object):
    jours_semaine = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    def __init__(self, debutHeure:str, finHeure:str, corps:str ,dateComplet:str = None):
        dateComplet = str(dateComplet)
        weekdayNumber: int = datetime.date(eval(dateComplet.split("-")[0]), eval(EmploiDuTempsDuJour.f(dateComplet.split("-")[1])), eval(EmploiDuTempsDuJour.f(dateComplet.split("-")[2]))).weekday()
        self.__jour: str = EmploiDuTempsDuJour.jours_semaine[int(weekdayNumber)]
        self.__debutHeure: str = debutHeure
        self.__finHeure: str = finHeure
        self.__corps: str = corps
        self.__dateComplet: str = dateComplet

    @staticmethod
    def f(d:str):
        if d[0] == "0":
            return d[1]
        return d


    def getJour(self):
        return self.__jour

    def getDebutHeure(self):
        return self.__debutHeure

    def getFinHeure(self):
        return self.__finHeure

    def getDateComplet(self):
        return self.__dateComplet

    def getCorps(self):
        return self.__corps


    def setJour(self, jour:str):
        self.__jour = jour

    def setDebutHeure(self, debutHeure:str):
        self.__debutHeure = debutHeure

    def setFinHeure(self, finHeure:str):
        self.__finHeure = finHeure

    def setDateComplet(self, dateComplet:str):
        self.__dateComplet = dateComplet

    def setCorps(self, corps:str):
        self.__corps = corps

    def __str__(self):
        return "{} {} {} {}".format(self.__jour, self.__debutHeure, self.__finHeure, self.__dateComplet)