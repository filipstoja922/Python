#Igra memorije
#Python version 3.6
__author__ = "Filip Stojanovic 2877"
from tkinter import *
import random, threading, time, os
try:
    import winsound
except ImportError:
    print("[INFO] Modul \"winsound\" se nije ocitao.")

class Application(Frame):
    def __init__(self, master):
        super(Application, self).__init__(master)
        self.grid()
        self.omoguci_poruke = True #Postaviti na False da onemogucis debugging poruke u konzoli
        self.brojevi = ["1", "2", "3", "4"]
        self.log_name = "Rezultati.txt"
        self.proveri_logfile()
        try:
            self.path = os.path.abspath("")
        except:
            self.path = None
        self.seq_active = False
        self.started = False
        self.seq_duzina_granica = 5
        self.rezultat = 0
        self.broj_granica = 4
        self.seq_duzina = self.broj_granica
        self.create_widgets()
        self.name = "None"
        self.debugging = False
        self.ime_Unos = Entry(self)
        self.ime_Unos.grid(row = 5, column = 2, sticky = W)
        self.ime_Unos.insert(0, "Unesi ime")
        self.submit_name_bttn = Button(self, text = "Potvrdi ime", command = self.unesi_ime, bg = "purple", fg = "white")
        self.submit_name_bttn.grid(row = 5, column = 2, sticky = E)
        if self.omoguci_poruke:
            print("[INFO] Poruke se mogu iskljuciti promenom self.omoguci_poruke na False .")
            print("[INFO] Duzina seq: " + str(self.broj_granica))
            print("[INFO] Rezultat: " + str(self.rezultat))
            print("[INFO] Granica seq: " + str(self.seq_duzina_granica))
            print("[INFO] Ime: " + self.log_name)
            if self.path:
                print("[INFO] Putanja: %s" %self.path)
            print("[INFO] Postavi ime na \"$dev_user\" za debbuging.")

    def thread_main(self):
        t1 = threading.Thread(target=self.proveri)
        t1.start()

    def prikazi_seq(self):
        """Pokazuje sekvencu tako sto boji kocke u crveno"""
        self.seq_active = True
        self.resetuj_btn()
        time.sleep(0.1)
        for x in self.sequence:
            if x == "1":
                self.bttn1["bg"] = "red"
            elif x == "2":
                self.bttn2["bg"] = "red"
            elif x == "3":
                self.bttn3["bg"] = "red"
            else:
                self.bttn4["bg"] = "red"
            time.sleep(0.2)
            self.resetuj_btn()
            time.sleep(0.2)
        self.seq_active = False
        self.bttn1["relief"] = "raised"
        self.bttn2["relief"] = "raised"
        self.bttn3["relief"] = "raised"
        self.bttn4["relief"] = "raised"

    def resetuj_btn(self):
        """resetuje dugmice"""
        self.bttn1["bg"] = "white"
        self.bttn2["bg"] = "white"
        self.bttn3["bg"] = "white"
        self.bttn4["bg"] = "white"
        self.bttn1["relief"] = "sunken"
        self.bttn2["relief"] = "sunken"
        self.bttn3["relief"] = "sunken"
        self.bttn4["relief"] = "sunken"

    def thread_sequence(self):
        """Kontrolise multithreading prikazi_seq funkcije"""
        t2 = threading.Thread(target=self.prikazi_seq)
        t2.start()

    def start(self):
        """Pokrece se kada kliknemo na start
        Pokrenuce se samo ako je prikazi_seq funkcija zavrsena (tj. ako je self.seq_active na False)"""
        
        if not self.seq_active:
            if self.omoguci_poruke:
                print("[EVENT] Dugme: Start")
            self.name = self.ime_Unos.get()
            self.thread_beep(500, 100)
            self.started = False
            self.attempt = ""
            self.gen_sequence() #Random generise novu seq
            if self.name == "$dev_user":
                self.debugging = True
                if self.omoguci_poruke:
                    print("[DEBUG] Seq:", self.sequence)
            self.thread_sequence() #Poziva multithreading prikazi_seq funkije()
            self.started =  True
            self.thread_main() #Poziva multithreading proveri() funkcije

    def set_options(self, item, value, targets=[], exceptions=[]):
        """Za lakse koriscenje. Za promenu vise vrednosti odjednom"""
        if not targets:
            for x in self.widgets:
                if x not in exceptions:
                    x[item] = value
        else:
            for x in targets:
                x[item] = value

    def thread_beep(self, pitch, duration):
        """Omogucava beeping dok su drugi procesi pokrenuti. izbegava zastajanje programa."""
        try:
            t4 = threading.Thread(target=winsound.Beep, args=(pitch, duration))
            t4.start()
        except: #Beeping nece raditi ako se igrica pokrene na drugi OS osim windowsa
            pass
                
    def proveri(self):
        """Proverava da li se uneta seq poklapa sa generisanom """
        while self.started:
            if len(self.attempt) >= self.broj_granica:
                if self.attempt == self.sequence:
                    self.thread_beep(600, 200)
                    self.thread_beep(800, 200)
                    self.rezultat += 1
                    if self.omoguci_poruke:
                        print("[INFO] Seq pogodjena!")
                        print("[INFO] Rezultat povecan za 1 ({})".format(self.rezultat))
                    if self.rezultat % self.seq_duzina_granica == 0 and self.rezultat != 0:
                        self.thread_beep(800, 200)
                        self.thread_beep(1000, 200)
                        self.thread_beep(1200, 200)
                        self.broj_granica += 1
                        if self.omoguci_poruke:
                            print("[INFO] Seq duzina povecana za 1 ({})".format(self.broj_granica))
                        self.sequence_length_lbl["bg"] = "lightgreen"
                    self.started = False
                    self.set_options("bg", "lightgreen", [self.score_lbl, self.bttn1, self.bttn2, self.bttn3, self.bttn4])
                    time.sleep(0.1)
                else:
                    self.thread_beep(400, 200)
                    self.thread_beep(150, 200)
                    if self.omoguci_poruke:
                        print("[INFO] Seq se ne poklapa.")
                    if self.rezultat > 0:
                        self.rezultat -= 1
                        if self.rezultat % self.seq_duzina_granica == self.seq_duzina_granica - 1:
                            self.broj_granica -= 1
                            self.thread_beep(170, 200)
                            self.thread_beep(150, 200)
                            self.thread_beep(130, 200)
                            if self.omoguci_poruke:
                                print("[INFO] Seq duzina smanjena za 1 ({})".format(self.broj_granica))
                            self.sequence_length_lbl["bg"] = "red"
                        if self.omoguci_poruke:
                            print("[INFO] Rezultat smanjen za 1 ({})".format(self.rezultat))
                    self.started = False
                    self.set_options("bg", "red", [self.score_lbl, self.bttn1, self.bttn2, self.bttn3, self.bttn4])
                    time.sleep(0.1)
                self.create_widgets()
                self.configure(background="black")

    def gen_sequence(self): #Generise Seq
        """Generise seq iz brojeva odredjene duzine."""
        self.sequence = "".join(random.choice(self.brojevi) for x in range(self.broj_granica))

    def unesi_ime(self):
        """Unosi ime u Rezultat.log fajl. Ako ime nije uneto, \"None\" je ispisano ako ime."""
        self.name = self.ime_Unos.get().strip()
        self.ime_Unos.grid_forget()
        self.submit_name_bttn.grid_forget()

    def create_widgets(self):
        """Kreira tkinter widgets"""
        self.bttn1 = Button(self, text = "\n\t1\t\n\n", command = lambda: self.button_press(1), font=("Helvetica", 12, "bold"), bg = "white", relief = SUNKEN) #lambda dozvoljava da prosledimo parametre funkciji
        self.bttn1.grid(row = 1, column = 0, sticky = W)
        self.bttn2 = Button(self, text = "\n\t2\t\n\n", command = lambda: self.button_press(2), font=("Helvetica", 12, "bold"), bg = "white", relief = SUNKEN)
        self.bttn2.grid(row = 1, column = 1, sticky = W)
        self.bttn3 = Button(self, text = "\n\t3\t\n\n", command = lambda: self.button_press(3), font=("Helvetica", 12, "bold"), bg = "white", relief = SUNKEN)
        self.bttn3.grid(row = 2, column = 0, sticky = W)
        self.bttn4 = Button(self, text = "\n\t4\t\n\n", command = lambda: self.button_press(4), font=("Helvetica", 12, "bold"), bg = "white", relief = SUNKEN)
        self.bttn4.grid(row = 2, column = 1, sticky = W)
        self.start_bttn = Button(self, text = "Start", command = self.start, bg = "purple", fg = "white")
        self.start_bttn.grid(row = 3, column = 2, sticky = E)
        self.score_lbl = Label(self, text = "Score: " + str(self.rezultat), bg = "black", fg = "white")
        self.score_lbl.grid(row = 1, column = 2, sticky = E)
        self.sequence_length_lbl = Label(self, text = "Duzina seq: " + str(self.broj_granica), bg = "black", fg = "white")
        self.sequence_length_lbl.grid(row = 2, column = 2, sticky = E)
        self.info_lbl = Label(self, text = "Metropolitan Univerzitet", anchor = W, justify = LEFT, bg = "black", fg = "white")
        self.info_lbl.grid(row = 4, column = 2, sticky = E)
        self.widgets = [self.bttn1, self.bttn2, self.bttn3, self.bttn4, self.start_bttn, self.score_lbl, self.sequence_length_lbl, self.info_lbl]

    def proveri_logfile(self):
        """Proverava da li log fajl postoji. Ako ne postoji kreira novi."""
        try:
            with open(self.log_name, "r") as f:
                f.read()
        except:
            if self.omoguci_poruke:
                print("[INFO] Kreiranje %s..." %self.log_name)
            with open(self.log_name, "w") as f:
                f.write("Rezultat Fajl - Kreiran: " + str(time.ctime(time.time())))
    
    def on_delete(self):
        """Kreira unos u log fijl kada se tkinter GUI zatvori koristeci Windows close dugme."""
        if self.omoguci_poruke:
            print("[INFO] Prekinuto: WM_DELETE_WINDOW")
        if self.name == "" or self.name == "Unesi ime":
            self.name = "None"
        if self.omoguci_poruke:
            print("[INFO] Upisivanje u %s..." %self.log_name)
        with open(self.log_name, "a") as f:
            if not self.debugging:
                f.write("\n" + str(time.ctime(time.time())) + " / Ime: " + self.name + " - Rezultat: " + str(self.rezultat))
            else:
                f.write("\n" + str(time.ctime(time.time())) + " / Ime: $dev_user - Rezultat: " + str(self.rezultat))
        if self.omoguci_poruke:
            print("[INFO] Zatvaranje app...")
        root.destroy()
        if self.omoguci_poruke:
            print("[INFO] Gotovo.\n[INFO] Izlaz.")
        
    def button_press(self, num): #Hendluje button press 
        if self.started:
            if not self.seq_active:
                if self.omoguci_poruke:
                    print("[EVENT] Button:", num)
                self.attempt += str(num)
        else:
            if self.omoguci_poruke:
                print("[EVENT] Dugmici su trenutno onemoguceni!")
        

def main():
    global root, app
    root = Tk()
    root.title("Igra memorije")
    root.configure(background="black")
    app = Application(root)
    app.configure(background="black")
    root.protocol("WM_DELETE_WINDOW", app.on_delete)
    root.mainloop()

if __name__ == "__main__":
    main()
