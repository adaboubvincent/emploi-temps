from tkcalendar import Calendar, DateEntry
import sqlite3
try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    import Tkinter as tk
    import ttk

from EmploiDuTempsDuJour import EmploiDuTempsDuJour

#heures = ["{} h".format(i) for i in range(24)]
heures = []
for i in range(24):
    if i < 10 :
        heures.append("0{} h".format(i))
    else:
        heures.append("{} h".format(i))

#minutes = ["{} min".format(i) for i in range(60)]
minutes = []
for i in range(60):
    if i < 10 :
        minutes.append("0{} min".format(i))
    else:
        minutes.append("{} min".format(i))


dateSelected: str = ""
count = 0
datasValues: list = []
dateChoose: str = ""
verifyModifyTypeEmploi = False

fenetre = tk.Tk()
w, h = fenetre.winfo_screenwidth(), fenetre.winfo_screenheight()
#fenetre.overrideredirect(1)
fenetre.geometry("%dx%d+%d+%d" %(750,580,(fenetre.winfo_screenwidth()-750)/2,(fenetre.winfo_screenheight()-580)/2))
#fenetre.geometry("750x500")
fenetre.minsize(100,100)
fenetre.config(bg="white")
fenetre.title("Emploi")
f1: tk.Frame = tk.Frame(fenetre, width = 1000, height = 900, bg = "blue")
emploiAujourdHuiFrame: tk.Frame = tk.Frame(fenetre, width = 1000, height = 900, bg = "red")
emploiJourFrame: tk.Frame = tk.Frame(fenetre, width = 1000, height = 900, bg = "white")
emploiDUnJourFrame: tk.Frame = tk.Frame(fenetre, width = 1000, height = 900, bg = "white")


DB_NAME: str = 'emploi.db'
def connexionDB():
    #SQLite3 instancié
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    
    cur.execute('''CREATE TABLE IF NOT EXISTS emploi
        (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,jour text, debutHeure text, finHeure text, corps text, dateComplet text);
        ''')
    cur.execute('''CREATE TABLE IF NOT EXISTS diary
        (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,jour text, corps text, dateComplet text);
        ''')

    con.commit()
    con.close()

if __name__ == '__main__':
    connexionDB()

def print_sel(cal):
    global dateSelected
    dateSelected = cal.selection_get()
    emploi_jour()

def calendrier():
    destroy_all_frame()
    global f1
    f1 = tk.Frame(fenetre, width = 1000, height = 900, bg = "blue")
    f1.pack(fill="both", expand=1)

    cal = Calendar(f1, selectmode='day', disabledforeground='red',
        cursor="hand1")
    
    date = cal.datetime.today() + cal.timedelta(days=2)
  
    cal.calevent_create(date + cal.timedelta(days=-2), 'Reminder 1', 'reminder')
    cal.tag_config('reminder', background='red', foreground='yellow')
    cal.pack(fill="both", expand=True)
    
    ttk.Button(f1, text="Mon emploi sur ce jour", padding = 5, command=lambda:print_sel(cal)).pack(fill="both")
    
    fenetre.update()


def emploiAujourdHui():
    destroy_all_frame()
    global emploiAujourdHuiFrame, dateSelected
    emploiAujourdHuiFrame = tk.Frame(fenetre, width = 1000, height = 900, bg = "white")
    emploiAujourdHuiFrame.pack(fill="both", expand=1)

    # libellé

    libelle = ttk.Label(emploiAujourdHuiFrame, text = 'Emploi du temps')

    libelle.pack(padx = 10, pady = 10)

    tableau = ttk.Treeview(emploiAujourdHuiFrame, columns=('heureDebut', 'heureFin', 'activite'))

    tableau.heading('heureDebut', text='Début heure')

    tableau.heading('heureFin', text='Fin Heure')

    tableau.heading('activite', text='Activité')

    tableau['show'] = 'headings' 

    tableau.column("heureDebut", anchor="center")
    tableau.column("heureFin", anchor="center") 
    tableau.column("activite", anchor="center") 
    tableau.pack(padx = 10, pady = (0, 10))

    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    import datetime, time

    date = time.localtime()
    date_now = ("{}/{}/{}".format(date[2],date[1],date[0])).split("/")
    dateSelected = datetime.date(int(date_now[2]), int(date_now[1]), int(date_now[0]))
    
    cur.execute('''SELECT debutHeure, finHeure, corps FROM emploi WHERE dateComplet=? ORDER BY debutHeure''', \
        (dateSelected,))
    resultat = cur.fetchall()
    con.close()
    
    if len(resultat):
        global count
        for enreg in resultat:
            #tableau.insert('', 'end', iid=enreg[0], values=(enreg[0], enreg[1], enreg[2]))
            tableau.insert('', 'end',iid=count, text=f'{count + 1}', values=(enreg[0], enreg[1], enreg[2]))
            count+=1
    else:
        libelle.configure(text = 'Il n\'y a pas encore un emploi pour la journée d\'aujourd\'hui.')
        tableau.pack_forget()

    def calling(event):
        global datasValues
        selectedRow = tableau.item(tableau.focus())
        datasValues = selectedRow['values']

    def rightClickMenu(event):
        global datasValues
        if datasValues != []:
            def modifier():
                global verifyModifyTypeEmploi
                verifyModifyTypeEmploi = False
                
                con = sqlite3.connect(DB_NAME)
                cur = con.cursor()
                cur.execute('''SELECT id FROM emploi WHERE debutHeure=? AND finHeure=? AND corps=?''', \
                    (str(datasValues[0]), str(datasValues[1]), str(datasValues[2])))
                idEmploiJourModifier = cur.fetchone()[0]
                con.close()
                emploi_jour_modifier(idEmploiJourModifier)

                
            def suprimer():
                con = sqlite3.connect(DB_NAME)
                cur = con.cursor()
                cur.execute('''DELETE FROM emploi WHERE debutHeure=? AND finHeure=? AND corps=?''', \
                    (str(datasValues[0]), str(datasValues[1]), str(datasValues[2])))
                con.commit()
                con.close()
                emploiAujourdHui()

            def popup(event):
                menu.post(event.x_root, event.y_root)


            menu = tk.Menu(tableau, tearoff=0)
            menu.add_command(label="Modifier", command=modifier)
            menu.add_command(label="Supprimer", command=suprimer)
            tableau.bind("<Button-3>", popup)
            

    tableau.bind("<3>", rightClickMenu)



    tableau.bind('<<TreeviewSelect>>', calling)

    ttk.Button(emploiAujourdHuiFrame, text="Mon emploi sur ce jour", padding = 5, command=emploi_jour).pack(fill="both")
    fenetre.update()



""" def set_focus(event=None):
    x, y = emploiJourFrame.winfo_pointerxy()
    emploiJourFrame.winfo_containing(x, y).focus() """




def emploi_jour_modifier(idEmploiJourModifier: int):
    destroy_all_frame()
    global emploiJourFrame
    emploiJourFrame = tk.Frame(fenetre, width = 1000, height = 900, bg = "white")
    emploiJourFrame.pack(fill="both")

    def modifierEmploi(debutHeure, finHeure, corps):
        global verifyModifyTypeEmploi

        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        values = (debutHeure, finHeure, corps, idEmploiJourModifier)
        cur.execute('''UPDATE emploi SET debutHeure=?, finHeure=?, corps=? WHERE id=?''', values)
        con.commit()
        con.close()
        if verifyModifyTypeEmploi:
            tableauActiviteEmploiDUnJour()
        else:
            emploiAujourdHui()
    
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute('''SELECT debutHeure, finHeure, corps  FROM emploi WHERE id=?''', (idEmploiJourModifier,))
    obj = cur.fetchone()
    con.close()
    
    try:
        debutH = obj[0].split(" ")[0] + " h"
        debutM = obj[0].split(" ")[2] + " min"

        finH = obj[1].split(" ")[0] + " h"
        finM = obj[1].split(" ")[2] + " min"
        
    except Exception as e:
        debutH = obj[0].split(" ")[0]
        debutM = obj[0].split(" ")[2]

        finH = obj[1].split(" ")[0]
        finM = obj[1].split(" ")[2]

    corpsAMod = obj[2]


    ttk.Label(emploiJourFrame, text='Debut(Heure, Minutes)',
        font = ("arial", 10, "bold")).place(x=0, y=10)
    listComboHeureDebut = ttk.Combobox(emploiJourFrame, values=heures,
        font = ("arial", 10, "bold"))
    listComboHeureDebut.set(debutH)
    listComboHeureDebut.place(x=300, y=10)
    listComboMinutesDebut = ttk.Combobox(emploiJourFrame, values=minutes,
        font = ("arial", 10, "bold"))
    listComboMinutesDebut.set(debutM)
    listComboMinutesDebut.place(x=500, y=10)

    ttk.Label(emploiJourFrame, text='Fin(Heure, Minutes)',
        font = ("arial", 10, "bold")).place(x=0, y=85)
    listComboHeureFin = ttk.Combobox(emploiJourFrame, values=heures,
        font = ("arial", 10, "bold"))
    listComboHeureFin.set(finH)
    listComboHeureFin.place(x=300, y=85)
    listComboMinutesFin = ttk.Combobox(emploiJourFrame, values=minutes,
        font = ("arial", 10, "bold"))
    listComboMinutesFin.set(finM)
    listComboMinutesFin.place(x=500, y=85)

    ttk.Label(emploiJourFrame, text='Corps',
        font = ("arial", 10, "bold")).place(x=0, y=160)
    corpsEmploi = tk.StringVar()
    corpsEntry = ttk.Entry(emploiJourFrame,text = "Corps",font = ("arial", 13, "bold"),
        textvariable=corpsEmploi)
    corpsEntry.insert(0, corpsAMod)
    corpsEntry.place(x=300,y=160)
    
    ttk.Button(emploiJourFrame, text="Modifier", padding = 5, command=lambda:modifierEmploi(listComboHeureDebut.get()+" "+listComboMinutesDebut.get(),\
        listComboHeureFin.get()+" "+listComboMinutesFin.get(), corpsEmploi.get())).place(x=200, y=230)

    
    fenetre.update()




def enteteEmploiDUnJour():
    destroy_all_frame()
    global emploiDUnJourFrame
    emploiDUnJourFrame = tk.Frame(fenetre, width = 1000, height = 900, bg = "white")
    emploiDUnJourFrame.pack(fill="both", expand=1)

    ttk.Label(emploiDUnJourFrame, text='Choisir la date').place(x=10, y=10)
    
    cal = DateEntry(emploiDUnJourFrame, width=12, background='darkblue',
                    foreground='white', borderwidth=2)
    cal.place(x=200, y=10)

    def getDate():
        global dateChoose
        dateChoose =  cal.get_date()
        tableauActiviteEmploiDUnJour()
        
    ttk.Button(emploiDUnJourFrame, text="Rechercher", padding = 5, command=getDate).place(x=500, y=10)
    
def emploiDUnJour():
    if dateChoose == "":
        enteteEmploiDUnJour()
    else:
        tableauActiviteEmploiDUnJour()
    


def tableauActiviteEmploiDUnJour():
    
    global emploiDUnJourFrame, dateChoose
    enteteEmploiDUnJour()
    # libellé

    libelle = ttk.Label(emploiDUnJourFrame, text = 'Emploi du temps du {} ({})'.format(EmploiDuTempsDuJour("", "", "", dateChoose).getJour(),
    dateChoose))

    libelle.pack(padx = 10, pady = 50)

    tableau = ttk.Treeview(emploiDUnJourFrame, columns=('heureDebut', 'heureFin', 'activite'))

    tableau.heading('heureDebut', text='Début heure')

    tableau.heading('heureFin', text='Fin Heure')

    tableau.heading('activite', text='Activité')

    tableau['show'] = 'headings' 

    tableau.column("heureDebut", anchor="center")
    tableau.column("heureFin", anchor="center") 
    tableau.column("activite", anchor="center") 
    tableau.pack(padx = 10, pady = (0, 10))

    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    
    cur.execute('''SELECT debutHeure, finHeure, corps FROM emploi WHERE dateComplet=? ORDER BY debutHeure''', \
        (dateChoose,))
    resultat = cur.fetchall()
    con.close()
    
    if len(resultat):
        global count
        for enreg in resultat:
            #tableau.insert('', 'end', iid=enreg[0], values=(enreg[0], enreg[1], enreg[2]))
            tableau.insert('', 'end',iid=count, text=f'{count + 1}', values=(enreg[0], enreg[1], enreg[2]))
            count+=1
    else:
        libelle.configure(text = 'Il n\'y a pas d\'emploi du temps sur cette jour.')
        tableau.pack_forget()

    
    def calling(event):
        global datasValues
        selectedRow = tableau.item(tableau.focus())
        datasValues = selectedRow['values']

    def rightClickMenu(event):
        global datasValues
        if datasValues != []:
            def modifier():
                global verifyModifyTypeEmploi
                verifyModifyTypeEmploi = True
                con = sqlite3.connect(DB_NAME)
                cur = con.cursor()
                cur.execute('''SELECT id FROM emploi WHERE debutHeure=? AND finHeure=? AND corps=?''', \
                    (str(datasValues[0]), str(datasValues[1]), str(datasValues[2])))
                idEmploiJourModifier = cur.fetchone()[0]
                con.close()
                emploi_jour_modifier(idEmploiJourModifier)

                
            def suprimer():
                con = sqlite3.connect(DB_NAME)
                cur = con.cursor()
                cur.execute('''DELETE FROM emploi WHERE debutHeure=? AND finHeure=? AND corps=?''', \
                    (str(datasValues[0]), str(datasValues[1]), str(datasValues[2])))
                con.commit()
                con.close()
                tableauActiviteEmploiDUnJour()

            def popup(event):
                menu.post(event.x_root, event.y_root)


            menu = tk.Menu(tableau, tearoff=0)
            menu.add_command(label="Modifier", command=modifier)
            menu.add_command(label="Supprimer", command=suprimer)
            tableau.bind("<Button-3>", popup)
            

    tableau.bind("<3>", rightClickMenu)

    tableau.bind('<<TreeviewSelect>>', calling)

    fenetre.update()
    




def emploi_jour():
    destroy_all_frame()
    global emploiJourFrame, dateSelected
    emploiJourFrame = tk.Frame(fenetre, width = 1000, height = 900, bg = "white")
    emploiJourFrame.pack(fill="both")

    def ajouterEmploi(debutHeure, finHeure, corps, dateComplet):

        objetEmploiDuJour = EmploiDuTempsDuJour(debutHeure, finHeure, corps, dateComplet)
        
        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        values = (objetEmploiDuJour.getJour(), objetEmploiDuJour.getDebutHeure(), \
            objetEmploiDuJour.getFinHeure(), objetEmploiDuJour.getCorps(), objetEmploiDuJour.getDateComplet())
        cur.execute('''INSERT INTO emploi(jour, debutHeure, finHeure, corps, dateComplet) VALUES(?,?,?,?,?)
                ''', values)
        con.commit()
        con.close()


        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        cur.execute('''SELECT * FROM emploi''')
        con.close()

        
        emploiAujourdHui()
       

    """         con = sqlite3.connect(DB_NAME)
        for line in con.iterdump():
            print(line)
        con.close() """



    ttk.Label(emploiJourFrame, text='Debut(Heure, Minutes)',
        font = ("arial", 10, "bold")).place(x=0, y=10)
    listComboHeureDebut = ttk.Combobox(emploiJourFrame, values=heures,
        font = ("arial", 10, "bold"))
    listComboHeureDebut.insert(0, "00 h")
    listComboHeureDebut.place(x=300, y=10)

    listComboMinutesDebut = ttk.Combobox(emploiJourFrame, values=minutes,
        font = ("arial", 10, "bold"))
    listComboMinutesDebut.insert(0, "00 min")
    listComboMinutesDebut.place(x=500, y=10)

    ttk.Label(emploiJourFrame, text='Fin(Heure, Minutes)',
        font = ("arial", 10, "bold")).place(x=0, y=85)
    listComboHeureFin = ttk.Combobox(emploiJourFrame, values=heures,
        font = ("arial", 10, "bold"))
    listComboHeureFin.insert(0, "00 h")
    listComboHeureFin.place(x=300, y=85)
    listComboMinutesFin = ttk.Combobox(emploiJourFrame, values=minutes,
        font = ("arial", 10, "bold"))
    listComboMinutesFin.insert(0, "00 min")
    listComboMinutesFin.place(x=500, y=85)

    ttk.Label(emploiJourFrame, text='Corps',
        font = ("arial", 10, "bold")).place(x=0, y=160)
    corpsEmploi = tk.StringVar()
    corpsEntry = ttk.Entry(emploiJourFrame,text = "Corps",font = ("arial", 13, "bold"),
        textvariable=corpsEmploi)
    """     corpsEntry.focus()
    corpsEntry.bind("<1>", set_focus) """
    corpsEntry.place(x=300,y=160)
    
    ttk.Button(emploiJourFrame, text="Ajouter", padding = 5, command=lambda:ajouterEmploi(listComboHeureDebut.get()+" "+listComboMinutesDebut.get(),\
        listComboHeureFin.get()+" "+listComboMinutesFin.get(), corpsEmploi.get(), dateSelected)).place(x=200, y=230)





    
    fenetre.update()

def hide_all_frame():
    global f1, emploiAujourdHuiFrame, emploiJourFrame, emploiDUnJourFrame
    f1.pack_forget()
    emploiAujourdHuiFrame.pack_forget()
    emploiJourFrame.pack_forget()
    emploiDUnJourFrame.pack_forget()

def destroy_all_frame():
    global f1, emploiAujourdHuiFrame, emploiJourFrame, emploiDUnJourFrame
    f1.destroy()
    emploiDUnJourFrame.destroy()
    emploiAujourdHuiFrame.destroy()
    emploiJourFrame.destroy()


#Menu bar config
menubar = tk.Menu(fenetre)


filemenu1 = tk.Menu(menubar)
filemenu1.add_command(label="Aujourd'hui", command=emploiAujourdHui)
filemenu1.add_command(label="D'une journée", command=emploiDUnJour)
menubar.add_cascade(label="Emploi du temps", menu=filemenu1)

filemenu = tk.Menu(menubar)
filemenu.add_command(label="Ouvrir Calendrier", command=calendrier)
menubar.add_cascade(label="Calendrier", menu=filemenu)
import sys
filemenu2 = tk.Menu(menubar)
filemenu2.add_command(label="Sortir", command=sys.exit)
menubar.add_cascade(label="Autre", menu=filemenu2)

fenetre.config(menu=menubar)

emploiAujourdHui()
fenetre.mainloop()



""" 
root = tk.Tk()
example2(root)
#ttk.Button(root, text='Calendar with events', command=example2).pack(padx=10, pady=10)
root.mainloop() """




""" def example1():
    def print_sel():
        print(cal.selection_get())
        cal.see(datetime.date(year=2016, month=2, day=5))

    top = tk.Toplevel(root)

    import datetime
    today = datetime.date.today()

    mindate = datetime.date(year=2018, month=1, day=21)
    maxdate = today + datetime.timedelta(days=5)
    print(mindate, maxdate)

    cal = Calendar(top, font="Arial 14", selectmode='day', locale='en_US',
                   mindate=mindate, maxdate=maxdate, disabledforeground='red',
                   cursor="hand1", year=2018, month=2, day=5)
    cal.pack(fill="both", expand=True)
    ttk.Button(top, text="ok", command=print_sel).pack()


def example3():
    top = tk.Toplevel(root)

    ttk.Label(top, text='Choose date').pack(padx=10, pady=10)

    cal = DateEntry(top, width=12, background='darkblue',
                    foreground='white', borderwidth=2, year=2010)
    cal.pack(padx=10, pady=10)


ttk.Button(root, text='DateEntry', command=example3).pack(padx=10, pady=10)
ttk.Button(root, text='Calendar', command=example1).pack(padx=10, pady=10)
 """


