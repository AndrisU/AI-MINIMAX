import tkinter as tk # Importē tkinter bibliotēku grafiskās lietotāja saskarnes (GUI) izveidei
from enum import Enum # Importē Enum klasi, lai izveidotu ērti lietojamu enumerāciju
from tkinter import messagebox # Importē messagebox funkcionalitāti no tkinter, lai parādītu ziņojumu logus
from tkinter import Tk, font # Importē Tk un font funkcionalitāti no tkinter

# Definē funkciju, kas centrē logu ekrāna vidū
def center_window(window, width=None, height=None):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    if width is None:
        width = window.winfo_width()
    if height is None:
        height = window.winfo_height()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f"{width}x{height}+{x}+{y}")

# Definē funkciju, kas atjaunina loga ģeometriju un izvietojumu ekrāna vidū
def update_geometry(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

# Definē enumerāciju "Player" ar divām vērtībām, USER un COMPUTER
class Player(Enum):
    USER = 0
    COMPUTER = 1

# Definē spēles klasi, kas satur spēles loģiku un metodes
class Game:
    
    def __init__(self, starting_number=12902400, target_number=7):
        # Inicializē spēles stāvokli ar norādīto sākuma un mērķa skaitli
        self.current_number = starting_number
        self.target_number = target_number
        # Nostāda pašreizējo spēlētāju kā cilvēku (lietotāju)
        self.current_player = Player.USER
        # Inicializē gājienu vēstures sarakstu kā tukšu
        self.moves_history = []

# definē funkciju "is_divisible", kas atgriež "True" vai "False"
    def is_divisible(self, number):
        return self.current_number % number == 0
    
# definē make_move metodi, kas pārbauda vai spēlētājs var veikt gājienu ar doto skaitli.
#  Ja dotais skaitlis dalās bez atlikuma ar pašreizējo skaitli, tad metode reģistrē spēlētāja
#  gājienu vēsturē, samazina pašreizējo skaitli, un nomaina pašreizējo spēlētāju uz otro.    
    def make_move(self, number):
        # Pārbauda, vai pašreizējais skaitlis dalās ar norādīto skaitli
        if self.is_divisible(number):
            # Ja dalās, pievieno gājienu vēsturei un atjauno pašreizējo skaitli
            self.moves_history.append((self.current_player, number))
            self.current_number //= number
            # Maina pašreizējo spēlētāju
            self.switch_player()
        else:
            # Ja nevar veikt gājienu, izdot ValueError ar kļūdas paziņojumu
            raise ValueError("Invalid move")

#funkcija pārslēdz spēlētāju
    def switch_player(self):
        # Pārbauda, vai pašreizējais spēlētājs ir lietotājs
        if self.current_player == Player.USER:
            # Ja pašreizējais spēlētājs ir lietotājs, nomaina to uz datoru
            self.current_player = Player.COMPUTER
        else:
            # Pretējā gadījumā nomaina pašreizējo spēlētāju uz lietotāju
            self.current_player = Player.USER

#pārbauda, vai spēle ir beigusies, salīdzinot pašreizējo skaitli ar mērķa skaitli un atgriežot "True", ja tie sakrīt, citādi atgriežot "False".
    def is_game_over(self):
        return self.current_number == self.target_number

    # normalizē atgriezto vērtību, lai tā būtu intervālā no -1 līdz 1.
    # Šāda normalizācija var palīdzēt algoritmam labāk saprast relatīvo
    # novērtējumu starp dažādiem spēles stāvokļiem.
    def evaluate_heuristic(self):
        return (self.current_number - self.target_number) / max(abs(self.target_number), abs(self.current_number))



    def minimax(self, depth, maximizing_player):
        if depth == 0 or self.is_game_over():# Pārbauda, vai ir sasniegts maksimālais pārbaudes dziļums vai spēle ir beigusies
            return self.evaluate_heuristic() # Ja ir, tad atgriež heiristiko vērtību pašreizējām pozīcijām
        # Ja algoritms pašlaik meklē lielāko iespējamo vērtību (maksimizē)
        if maximizing_player:       
            max_eval = float('-inf') # Sāk ar negatīvu bezgalību kā sākotnējo maksimālo vērtību           
            for number in [2, 3, 4, 5]:# Izmēģina visas iespējamas darbības (dalīšana ar 2, 3, 4, 5)
                if self.is_divisible(number):# Ja ir iespējams - dalīt ar šo skaitli
                    self.current_number //= number# Atjaunina pašreizējo skaitli, dalot to ar "number" un saglabājot veselo daļu
                    eval = self.minimax(depth - 1, False)# Rekursīvi izsauc minimax algoritmu nākamajā līmenī, ņemot vērā pretinieka labāko gājienu
                    self.current_number *= number# Atjauno pašreizējo skaitli, reizinot to ar "number" un atceļ iepriekšējo dalīšanas darbību
                    max_eval = max(max_eval, eval)# Atjaunina maksimālo vērtību, ja nepieciešams
            return max_eval# Atgriež maksimālo vērtību
        # Ja algoritms pašlaik meklē mazāko iespējamo vērtību (minimizē)
        else:
            min_eval = float('inf')# Sāk ar pozitīvu bezgalību kā sākotnējo minimālo vērtību
            for number in [2, 3, 4, 5]:# Izmēģina visas iespējamas darbības (dalīšana ar 2, 3, 4, 5)
                if self.is_divisible(number):# Ja ir iespējams - dalīt ar šo skaitli
                    self.current_number //= number# Atjaunina pašreizējo skaitli, dalot to ar "number" un saglabājot veselo daļu
                    eval = self.minimax(depth - 1, True)# Rekursīvi izsauc minimax algoritmu nākamajā līmenī, ņemot vērā pretinieka labāko gājienu
                    self.current_number *= number# Atjauno pašreizējo skaitli, reizinot to ar "number" un atceļ iepriekšējo dalīšanas darbību
                    min_eval = min(min_eval, eval)# Atjaunina minimālo vērtību, ja nepieciešams
            return min_eval# Atgriež minimālo vērtību

# Definē spēles grafiskās lietotāja saskarnes klasi
class GameGUI:


# Konstruktors GameGUI klasei, kas inicializē saskarni
    def __init__(self, game):
        
        self.game = game# Saglabā spēles objektu
        self.window = tk.Tk()# Izveido jaunu Tkinter logu
        self.window.title("Divpersonu spēle")# Iestata loga virsrakstu
        center_window(self.window,500,600)# Centrē logu un iestata tā izmērus
        self.window.lift()# Paceļ logu virs citiem logiem
        self.create_widgets()# Izveido saskarnes elementus
        self.choose_starting_player()# Izvēlas sākuma spēlētāju
        self.window.mainloop()# Sāk Tkinter galveno cilpu

# Metode, kas izveido grafiskās lietotāja saskarnes komponentes
# lambda funkcija izsauc self.on_user_move(x) funkciju, kad poga tiek nospiesta.
    def create_widgets(self):

        
        self.label = tk.Label(self.window, text=f"Pašreizējais skaitlis: {self.game.current_number}",font=("Arial", 15,))
        self.label.pack()

        self.buttons_frame = tk.Frame(self.window)
        self.buttons_frame.pack()

        self.button2 = tk.Button(self.window, text="Dalīt ar 2",font=("Arial", 15,), command=lambda: self.on_user_move(2))
        self.button2.pack()

        self.button3 = tk.Button(self.window, text="Dalīt ar 3",font=("Arial", 15), command=lambda: self.on_user_move(3))
        self.button3.pack()

        self.button4 = tk.Button(self.window, text="Dalīt ar 4",font=("Arial", 15), command=lambda: self.on_user_move(4))
        self.button4.pack()

        self.button5 = tk.Button(self.window, text="Dalīt ar 5",font=("Arial", 15), command=lambda: self.on_user_move(5))
        self.button5.pack()

        self.reset_button = tk.Button(self.window, text="Restartēt spēli",font=("Arial", 15), command=self.reset_game)
        self.reset_button.pack()

        self.history_label = tk.Label(self.window, text="Gājienu vēsture:")
        self.history_label.pack()

        self.history_text = tk.Text(self.window, width=30, height=20)
        self.history_text.pack()


# Metode, kas atjaunina pogu stāvokli un krāsu atkarībā no to spējas dalīt pašreizējo skaitli        
    def update_buttons(self):
        # Atjauno pogu stāvokli un krāsu atkarībā no to izmantojamības
        for button, number in [(self.button2, 2), (self.button3, 3), (self.button4, 4), (self.button5, 5)]:
            if self.game.is_divisible(number):# Pārbauda, vai pašreizējais skaitlis ir dalāms ar šo skaitli
                # Ja dalāms, uzstāda pogas fonu zaļu un atļauj tās lietošanu
                button.config(bg="green", state=tk.NORMAL)
            else:
                # Ja nav dalāms, uzstāda pogas fonu sarkanu un neļauj tās lietošanu
                button.config(bg="red", state=tk.DISABLED)

# Metode, kas ļauj lietotājam izvēlēties, kurš sāks spēli
    def choose_starting_player(self):

        self.update_buttons()
        # Izveido jaunu dialoglodziņu sākotnējā spēlētāja izvēlei
        choose_player_window = tk.Toplevel(self.window)
        choose_player_window.title("Izvēlies, kurš sāk spēli")
        choose_player_window.update_idletasks()
        choose_player_window.geometry(center_window(choose_player_window,500,600))
        choose_player_window.lift()

        # Izveido pogu ar tekstu "cilvēks" un piesaista tai funkciju, kas atbilst Player.USER
        cilveks_button = tk.Button(choose_player_window, text="cilvēks",font=("Arial", 20), command=lambda: self.set_starting_player(Player.USER, choose_player_window))
        cilveks_button.pack(pady=10)

        # Izveido pogu ar tekstu "dators" un piesaista tai funkciju, kas atbilst Player.COMPUTER
        dators_button = tk.Button(choose_player_window, text="dators",font=("Arial", 20), command=lambda: self.set_starting_player(Player.COMPUTER, choose_player_window))
        dators_button.pack(pady=10)
       
        update_geometry(choose_player_window)

# Metode, kas iestata sākotnējo spēlētāju un ļauj datoram veikt gājienu, ja nepieciešams
    def set_starting_player(self, player, window):
        # Iestata sākotnējo spēlētāju
        self.game.current_player = player

        # Ja sākotnējais spēlētājs ir dators, dators veic pirmo gājienu
        if player == Player.COMPUTER:
            self.computer_move()
        # Aizver dialoglodziņu, kurā tika izvēlēts sākotnējais spēlētājs
        window.destroy()
        
# Metode, kas tiek izsaukta, kad lietotājs veic gājienu
    def on_user_move(self, number):
        # Mēģina veikt lietotāja gājienu
        try:
            # Veic lietotāja gājienu spēlē
            self.game.make_move(number)
            # Atjaunina tekstu ar pašreizējo skaitli
            self.label.config(text=f"Pašreizējais skaitlis: {self.game.current_number}")
            # Atjaunina gājienu vēstures teksta lauku
            self.update_history()

            # Pārbauda, vai spēle ir beigusies
            if self.game.is_game_over():
                # Parāda paziņojumu, ka lietotājs uzvarēja
                messagebox.showinfo("Spēle beigusies", "Jūs uzvarējāt!")
                self.update_history()
                self.reset_game()
            else:
                # Ja spēle nav beigusies, dators veic savu gājienu
                self.computer_move()


        # Ja notiek kļūda (piemēram, neiespējams gājiens), parāda kļūdas paziņojumu
        except ValueError:
            messagebox.showerror("Kļūda", "Nederīgs gājiens")

        self.update_history() 
        self.update_buttons()

# Metode, kas veic datora gājienu, izmantojot minimax algoritmu
    def computer_move(self):
        # Inicializē labāko gājienu kā None un labāko novērtējumu kā negatīvu bezgalību
        best_move = None
        best_eval = float('-inf')
        
        # Izmanto ciklu, lai pārbaudītu katru skaitli no 2 līdz 5
        for number in [2, 3, 4, 5]:
            # Pārbauda, vai pašreizējais skaitlis ir dalāms ar šo skaitli
            if self.game.is_divisible(number):
                # Ja tā, veicam gājienu, dalot pašreizējo skaitli ar izvēlēto skaitli
                self.game.current_number //= number
                # Izsauc minimax algoritmu, lai novērtētu šo gājienu
                eval = self.game.minimax(20, False)  # var mainīt pārmeklēšanas dziļumu pēc nepieciešamības
                # Atjaunojam pašreizējo skaitli, atceļot gājienu
                self.game.current_number *= number 

                # Pārbauda, vai šī gājiena novērtējums ir labāks nekā iepriekšējais labākais
                if eval > best_eval:
                    # Ja tā, atjauninām labāko novērtējumu un labāko gājienu
                    best_eval = eval
                    best_move = number

        # Pārbauda, vai labākais gājiens tika atrasts
        if best_move is not None:
            # Ja tā, veic labāko gājienu un atjaunina ekrāna tekstu un pogas
            self.game.make_move(best_move)
            self.label.config(text=f"Pašreizējais skaitlis: {self.game.current_number}")
            self.update_history()
            self.update_buttons()
            # Pārbauda, vai spēle ir beigusies
            if self.game.is_game_over():
               # Ja tā, informē lietotāju par datora uzvaru
                messagebox.showinfo("Spēle beigusies", "Dators uzvarēja!")
                
                self.reset_game()
        else:
            # Ja labākais gājiens nav atrasts, informē lietotāju par kļūdu
            messagebox.showerror("Kļūda", "Dators nevarēja veikt gājienu")

        # Atjaunina vēsturi un pogu stāvokli
        self.update_history()
        self.update_buttons()

# Metode, kas atjaunina gājienu vēsturi grafiskajā lietotāja saskarnē
    def update_history(self):
        # Dzēš iepriekšējo vēsturi no teksta lauka
        self.history_text.delete(1.0, tk.END)
        # Izmanto ciklu, lai pārbaudītu spēles gājienu vēsturi
        for player, move in self.game.moves_history:
            # Nosaka spēlētāja nosaukumu atkarībā no spēlētāja uzdevuma (lietotājs vai dators)
            player_name = "Lietotājs" if player == Player.USER else "Dators"
            # Pievieno tekstu teksta laukā ar spēlētāja nosaukumu un veiktā gājiena informāciju
            self.history_text.insert(tk.END, f"{player_name} dalīja ar {move}\n")

# Metode, kas reseto spēli un sāk jaunu spēli
    def reset_game(self):
        # Atjaunina gājienu vēstures teksta lauku
        self.update_history()
        # Izveido jaunu spēles objektu, lai sāktu no sākuma
        self.game = Game()
        # Izvēlas, kurš spēlētājs sāk spēli (lietotājs vai dators)
        self.choose_starting_player()
        # Atjaunina tekstu ar pašreizējo skaitli
        self.label.config(text=f"Pašreizējais skaitlis: {self.game.current_number}")
        # Atjaunina pogu stāvokli atbilstoši spēles stāvoklim
        self.update_buttons()

if __name__ == "__main__": #Šī rindiņa pārbauda, vai šis skripts tiek izpildīts kā galvenais skripts (nevis importēts kā modulis)
    game = Game() # Izveido jaunu spēles objektu
    gui = GameGUI(game) # Izveido jaunu spēles grafiskās lietotāja saskarnes objektu, padodot spēles objektu kā parametru