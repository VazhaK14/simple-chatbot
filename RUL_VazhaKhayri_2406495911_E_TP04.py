import pygame 
import os
from tkinter import *
from tkinter import messagebox
from random import *
from time import *

class ChatBot:
    def __init__(self, window): 
        self.window = window
        self.window.title('ChatBot Sederhana')
        self.window.geometry('450x400')
        
        #Buat Frame dalam window
        self.frame = Frame(self.window)
        self.window.rowconfigure(0, weight = 1)
        self.window.columnconfigure(0, weight = 1)
        self.frame.grid(row = 0, column = 0, sticky ='news') # news = north, east, west, south
        self.frame.rowconfigure(0, weight=1)  
        self.frame.columnconfigure(0, weight=1)
        
        #buat grid dalam frame
        self.grid = Frame(self.frame)
        self.grid.grid(row = 0, column = 3, sticky ='news')
        self.grid.rowconfigure(0, weight = 1)
        self.grid.columnconfigure(3, weight = 1)
        
        #Buat MenuBar
        self.menubar = Menu(self.window)
        self.window['menu'] = self.menubar
        
        self.label_menu1 = Menu(self.menubar, tearoff = 0)
        self.menubar.add_cascade(label = 'File', menu = self.label_menu1)
        self.label_menu1.add_command(label = 'Simpan Sesi', command=self.simpan_sesi)
        self.label_menu1.add_command(label = 'Reset Sesi', command=self.reset_sesi)
        self.label_menu1.add_separator()
        self.label_menu1.add_command(label = 'Keluar', command=self.keluar)
        
        self.label_menu2 = Menu(self.menubar, tearoff = 0)
        self.menubar.add_cascade(label='Tema', menu = self.label_menu2)
        self.label_menu2.add_command(label = 'Ubah Tema', command=self.ubah_tema)
        self.label_menu2.add_command(label = 'Default', command=self.kembalikan_tema)
        
        self.label_menu3 = Menu(self.menubar, tearoff = 0)
        self.menubar.add_cascade(label='Tentang', menu = self.label_menu3)
        self.label_menu3.add_command(label='Tentang Aplikasi', command=self.tentang_app)
        
        #Buat chatbox
        self.frame_chatbox = Frame(self.frame)
        self.frame_chatbox.grid(row=0, column=0, sticky='news', pady=8, padx=8)
        self.frame_chatbox.columnconfigure(0, weight=1) 
        self.frame_chatbox.rowconfigure(0, weight=1)
        
        self.sc = Scrollbar(self.frame_chatbox, orient=VERTICAL)
        self.msg = Listbox(self.frame_chatbox, yscrollcommand=self.sc.set)
        self.msg.insert(END, 'Chatbot: Halo! Ada yang bisa saya bantu?😊')
        self.sc.config(command=self.msg.yview)
        self.msg.grid(row=0, column=0, sticky='news')
        self.sc.grid(row=0, column=1, sticky='ns')
        
        #Buat button
        self.frame_button = Frame(self.frame)
        self.frame_button.grid(row=1, column=0, sticky='n', pady=20)
        
        self.button1 = Button(self.frame_button, text='Buat Lelucon', command=lambda: [self.msg.insert(END, f'User: Buat lelucon'), self.buat_lelucon()])
        self.button1.grid(row=0, column=0, padx=8)
        self.button2 = Button(self.frame_button, text='Tanya Jam', command=lambda: [self.msg.insert(END, f'User: Tanya jam'), self.tanya_jam()])
        self.button2.grid(row=0, column=1, padx=8)
        self.button3 = Button(self.frame_button, text='Soal Matematika', command=lambda: [self.msg.insert(END, f'User: Beri aku soal matematika'), self.soal_matematika()])
        self.button3.grid(row=0, column=2, padx=8)
        self.button4 = Button(self.frame_button, text='Music Button', command=self.xyz)
        self.button4.grid(row=0, column=3, padx=8)
        
        #Buat chat message
        self.frame_message = Frame(self.frame)
        self.frame_message.grid(row=2, column=0, sticky='news', pady=10, padx=15)
        self.frame_message.rowconfigure(0, weight=1)
        self.frame_message.columnconfigure(0, weight=1)
        
        self.message = Entry(self.frame_message, bg='white')
        self.message.grid(row=0, column=0, sticky='news')
        self.message.bind('<Return>', self.send_message)
        self.kirim_button = Button(self.frame_message, width=5, text='Kirim', command=self.send_message)
        self.kirim_button.grid(row=0, column=1, sticky='e', padx=(20,0))
        
    #untuk menampilkan pesan pada listbox
    def send_message(self, event=None):
        user_message = self.message.get()
        if user_message:
            try:
                self.msg.insert(END, f'User: {user_message}')
                self.message.delete(0, END) 
                if 'lelucon' in user_message.lower():
                    self.buat_lelucon()
                elif 'jam' in user_message.lower():
                    self.tanya_jam()
                elif 'matematika' in user_message.lower():  
                    self.soal_matematika()
                elif 'hai' in user_message.lower():
                    self.msg.insert(END, 'Chatbot: Hai! Ada yang bisa saya bantu?')
                elif 'apa kabar' in user_message.lower():
                    self.msg.insert(END, 'Chatbot: Kabar baik! Bagaimana kabarmu?')
                elif 'baik' in user_message.lower():
                    self.msg.insert(END, 'Chatbot: Senang mendengar itu! Ada yang bisa saya bantu?')
                elif 'siapa nama' in user_message.lower():
                    self.msg.insert(END, 'Chatbot: Halo nama saya adalah Chabot yang selalu siap membantu anda!')
                elif self.counting_math:
                    try:
                        answer = int(user_message)
                        if answer == result:
                            self.msg.insert(END, 'Chatbot: Jawaban Anda benar!')
                        else:
                            self.msg.insert(END, f'Chatbot: Salah, jawaban yang benar adalah {result}')
                        self.counting_math = False
                    except ValueError:
                        self.msg.insert(END, 'Chatbot: Masukkan angka yang valid sebagai jawaban.')
                else:
                    self.msg.insert(END, 'Chatbot: Maaf, Saya belum mengerti perintah anda')
            except AttributeError:
                self.msg.insert(END, 'Chatbot: Maaf, Saya belum mengerti perintah anda')
    
    # Fungsi untuk membuat lelucon
    def buat_lelucon(self):
        list_of_jokes = [
            'Kenapa buku pelajaran sedih? Karena dia punya banyak masalah! 📘',
            'Di dunia ini cuma ada dua tipe orang, yang suka tidur, dan yang salah jalan hidupnya 🚶',
            'Aku mencoba diet, tapi kue di meja bilang, "Hai, kita ngobrol dulu yuk"🎂💬',
            'Kalau hidupku film, genrenya pasti komedi absurd 😂',
            'Aku bikin kopi pahit, biar hatiku nggak merasa sendirian.☕'
        ]
        self.msg.insert(END, f'Chatbot: {list_of_jokes[randint(0, len(list_of_jokes)-1)]}')    
    
    #fungsi untuk menanyakan jam
    def tanya_jam(self):    
        self.msg.insert(END, f'Chatbot: Saat ini pukul {strftime('%H:%M:%S', localtime())}')
    
    #fungsi untuk membuat soal matematika
    def soal_matematika(self): 
        global left_num, right_num, result
        left_num = randint(0, 10)
        right_num = randint(0, 10)
        self.msg.insert(END, f'Chatbot: Berapa {left_num} + {right_num}?')
        result = left_num + right_num 
        
        self.counting_math = True
    
    #fungsi untuk menyimpan sesi percakapan
    def simpan_sesi(self): 
        if self.msg.get(0) == self.msg.get(END): 
            messagebox.showinfo('Info', 'Tidak ada sesi untuk disimpan')
        else:
            semua_pesan = self.msg.get(0, END)
            nama_file = f'chat_session_{strftime('%Y-%m-%d_%H-%M-%S', localtime())}.txt'
            
            with open(nama_file, 'w', encoding='utf-8') as file:
                for pesan in semua_pesan:
                    file.write(pesan + '\n')
            
            messagebox.showinfo('Sukses', f'Sesi percakapan berhasil disimpan sebagai \n{nama_file}')
    
    #fungsi untuk melakukan reset pada sesi percakapan
    def reset_sesi(self): 
        self.msg.delete(0, END)
        messagebox.showinfo('Reset', 'Sesi telah direset')
        self.msg.insert(END, 'Chatbot: Halo! Ada yang bisa saya bantu?😊')
    
    #fungsi untuk menutup tab chatbot
    def keluar(self):
        self.window.destroy()
    
    #fungsi untuk mengubah tema menjadi gelap
    def ubah_tema(self):
        dark_theme = 'black'
        font_color = 'white'
        
        color_bg = [
            self.window, 
            self.frame, 
            self.frame_chatbox, 
            self.frame_button, 
            self.message, 
            self.msg, 
            self.frame_message, 
            self.button1, 
            self.button2, 
            self.button3, 
            self.button4
        ]
        color_fg = [self.message, self.msg, self.button1, self.button2, self.button3, self.button4]
        
        for background in color_bg:
            background.config(bg=dark_theme)
            
        for font in color_fg:
            font.config(fg=font_color)
            
        self.kirim_button.config(bg='red', fg='black')
    
    #fungsi untuk mengembalikan tema awal
    def kembalikan_tema(self):
        white_theme = 'white'
        font_color = 'black'
        
        color_bg = [
            self.window, 
            self.frame, 
            self.frame_chatbox, 
            self.frame_button, 
            self.message, 
            self.msg, 
            self.frame_message, 
            self.kirim_button,
            self.button1, 
            self.button2, 
            self.button3, 
            self.button4
        ]
        color_fg = [self.message, self.msg, self.kirim_button, self.button1, self.button2, self.button3, self.button4]
        
        for background in color_bg:
            background.config(bg=white_theme)
            
        for font in color_fg:
            font.config(fg=font_color)
    
    #fungsi untuk menunjukkan tentang aplikasi
    def tentang_app(self):
        messagebox.showinfo('Tentang Aplikasi',
            'Aplikasi Chatbot ini dikembangkan oleh VAZHA-KHAYRI\
            \ndari FASILKOM UI di tahun 2024.\
            \nSemoga aplikasi ini dapat menjadi pembelajaran yang\
            bermanfaat, have a great day!'
        )
    
    #fungsi untuk play music 
    def xyz(self):
        music_path = 'music.mp3'
        #jika music path tidak ada, maka akan muncul show error
        if not os.path.exists(music_path):
            messagebox.showerror('Error', 'Rickroll MP3 file not found!')
            return
        
        try:
            pygame.mixer.init()
            # memutar lagu MP3
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play()
            
            rickroll_messages = [
                'Chatbot: You just got RICKROLLED!',
                'Chatbot: Never gonna give you up!🕺',
                'Chatbot: Never gonna let you down!🎶',
            ]
            
            for message in rickroll_messages:
                self.msg.insert(END, message)
            
            # Tombol stop music
            self.stop_music_button = Button(self.frame_button, text='Stop Music', command=self.stop_rickroll)
            self.stop_music_button.grid(row=1, column=0, padx=8, pady=8, stick='n')
        except Exception:
            messagebox.shererror('Playback Error', f'Could not play the music: {str(Exception)}')
            
    def stop_rickroll(self):
        pygame.mixer.music.stop()
        # Menghilangkan Stop Button
        if hasattr(self, 'stop_music_button'):
            self.stop_music_button.destroy()

#main program
if __name__ == '__main__':
    root = Tk()
    my_chatbot = ChatBot(root)
    root.mainloop()