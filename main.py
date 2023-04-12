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
        self.current_number = starting_number
        self.target_number = target_number
        self.current_player = Player.USER
        self.moves_history = []

# definē funkciju "is_divisible", kas atgriež "True" vai "False"
    def is_divisible(self, number):
        return self.current_number % number == 0
    
# definē make_move metodi, kas pārbauda vai spēlētājs var veikt gājienu ar doto skaitli.
#  Ja dotais skaitlis dalās bez atlikuma ar pašreizējo skaitli, tad metode reģistrē spēlētāja
#  gājienu vēsturē, samazina pašreizējo skaitli, un nomaina pašreizējo spēlētāju uz otro.    
    def make_move(self, number):
        if self.is_divisible(number):
            self.moves_history.append((self.current_player, number))
            self.current_number //= number
            self.switch_player()
        else:
            raise ValueError("Invalid move")

#funkcija pārslēdz spēlētāju
    def switch_player(self):
        if self.current_player == Player.USER:
            self.current_player = Player.COMPUTER
        else:
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
        for button, number in [(self.button2, 2), (self.button3, 3), (self.button4, 4), (self.button5, 5)]:
            if self.game.is_divisible(number):
                button.config(bg="green", state=tk.NORMAL)
            else:
                button.config(bg="red", state=tk.DISABLED)

# Metode, kas ļauj lietotājam izvēlēties, kurš sāks spēli
    def choose_starting_player(self):

        self.update_buttons()
        choose_player_window = tk.Toplevel(self.window)
        choose_player_window.title("Izvēlies, kurš sāk spēli")
        choose_player_window.update_idletasks()
        choose_player_window.geometry(center_window(choose_player_window,500,600))
        choose_player_window.lift()

        # Izveido pogu ar tekstu "cilvēks" un piesaista tai funkciju, kas atbilst Player.USER
        asd_button = tk.Button(choose_player_window, text="cilvēks",font=("Arial", 20), command=lambda: self.set_starting_player(Player.USER, choose_player_window))
        asd_button.pack(pady=10)

        # Izveido pogu ar tekstu "dators" un piesaista tai funkciju, kas atbilst Player.COMPUTER
        dfg_button = tk.Button(choose_player_window, text="dators",font=("Arial", 20), command=lambda: self.set_starting_player(Player.COMPUTER, choose_player_window))
        dfg_button.pack(pady=10)
       
        update_geometry(choose_player_window)

# Metode, kas iestata sākotnējo spēlētāju un ļauj datoram veikt gājienu, ja nepieciešams
    def set_starting_player(self, player, window):
        self.game.current_player = player

        if player == Player.COMPUTER:
            self.computer_move()
        window.destroy()
        
# Metode, kas tiek izsaukta, kad lietotājs veic gājienu
    def on_user_move(self, number):
        
        try:
            self.game.make_move(number)
            self.label.config(text=f"Pašreizējais skaitlis: {self.game.current_number}")
            self.update_history()

            if self.game.is_game_over():
                messagebox.showinfo("Spēle beigusies", "Jūs uzvarējāt!")
                self.update_history()
                self.reset_game()
            else:
                self.computer_move()



        except ValueError:
            messagebox.showerror("Kļūda", "Nederīgs gājiens")

        self.update_history() 
        self.update_buttons()

# Metode, kas veic datora gājienu, izmantojot minimax algoritmu
    def computer_move(self):
        best_move = None
        best_eval = float('-inf')
        
        for number in [2, 3, 4, 5]:
            if self.game.is_divisible(number):
                self.game.current_number //= number
                eval = self.game.minimax(20, False)  # var mainīt pārmeklēšanas dziļumu pēc nepieciešamības
                self.game.current_number *= number 

                if eval > best_eval:
                    best_eval = eval
                    best_move = number

        if best_move is not None:
            self.game.make_move(best_move)
            self.label.config(text=f"Pašreizējais skaitlis: {self.game.current_number}")
            self.update_history()

            if self.game.is_game_over():
               
                messagebox.showinfo("Spēle beigusies", "Dators uzvarēja!")
                
                self.reset_game()
        else:
            messagebox.showerror("Kļūda", "Dators nevarēja veikt gājienu")

        self.update_history()
        self.update_buttons()

# Metode, kas atjaunina gājienu vēsturi grafiskajā lietotāja saskarnē
    def update_history(self):
        self.history_text.delete(1.0, tk.END)  # Dzēš iepriekšējo vēsturi
        for player, move in self.game.moves_history:
            player_name = "Lietotājs" if player == Player.USER else "Dators"
            self.history_text.insert(tk.END, f"{player_name} dalīja ar {move}\n")

# Metode, kas reseto spēli un sāk jaunu spēli
    def reset_game(self):
        self.update_history()
        self.game = Game()
        self.choose_starting_player()
        self.label.config(text=f"Pašreizējais skaitlis: {self.game.current_number}")
        self.update_buttons()

if __name__ == "__main__": #Šī rindiņa pārbauda, vai šis skripts tiek izpildīts kā galvenais skripts (nevis importēts kā modulis)
    game = Game() # Izveido jaunu spēles objektu
    gui = GameGUI(game) # Izveido jaunu spēles grafiskās lietotāja saskarnes objektu, padodot spēles objektu kā parametru