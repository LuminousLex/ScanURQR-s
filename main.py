import tkinter
import customtkinter
from CTkListbox import *
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from QRDetecting import realtime_scanning, scanning, camera_scanning, reset_events, toggle_pause, set_stop, is_paused
import threading
import cv2

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Scan Your QR! ")
        self.iconbitmap('qr_logo.ico')
        
        # Увеличил высоту окна до 650, чтобы всё влезало
        self.geometry(f"{400}x{650}")
        self.resizable(False, False)
        
        # Настройка колонок: вторая колонка (где основной контент) растягивается
        self.grid_columnconfigure(1, weight=1)
        # Настройка строк: последняя строка (список) растягивается вниз
        self.grid_rowconfigure(6, weight=1)
        
        # Поле ввода
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Введите параметр для поиска: ")
        self.entry.grid(row=0, column=1, padx=(20, 20), pady=(20, 10), sticky="nsew")
        
        # Кнопка выбора файла
        self.select_file_button = customtkinter.CTkButton(self, text="Выбрать видео", command=self.select_video)
        self.select_file_button.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")
        
        # Фрейм настроек
        self.radiobutton_frame = customtkinter.CTkFrame(self)
        self.radiobutton_frame.grid(row=2, column=1, padx=(20, 20), sticky="nsew")
        self.radio_var = tkinter.IntVar(value=0)
        self.label_radio_group = customtkinter.CTkLabel(master=self.radiobutton_frame, text="Настройка: ")
        self.label_radio_group.grid(row=0, column=0, padx=20, pady=0, sticky="w")
        
        self.radio_button_1 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, text="Режим видео",
                                                           value=0)
        self.radio_button_1.grid(row=1, column=0, pady=5, padx=20, sticky="w")
        
        self.radio_button_2 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, text="Веб-камера",
                                                           value=1)
        self.radio_button_2.grid(row=2, column=0, pady=5, padx=20, sticky="w")
        
        self.switch_1 = customtkinter.CTkSwitch(master=self.radiobutton_frame, text="Предобработка видео")
        self.switch_1.grid(row=3, column=0, pady=5, padx=20, sticky="w")
        
        self.label_slider_group = customtkinter.CTkLabel(master=self.radiobutton_frame, text="Пропуск кадров: ")
        self.label_slider_group.grid(row=4, column=0, padx=20, pady=5, sticky="w")
        
        self.slider = customtkinter.CTkSlider(master=self.radiobutton_frame, from_=2, to=10, number_of_steps=8, command=self.update_label)
        self.slider.grid(row=5, column=0, padx=15, pady=5, sticky="w")
        self.slider.set(1)
        
        self.slider_value_label = customtkinter.CTkLabel(master=self.radiobutton_frame, text="Значение: 2")
        self.slider_value_label.grid(row=5, column=1, padx=0, pady=0, sticky="w")
        
        # Кнопка СТАРТ
        self.start_button = customtkinter.CTkButton(master=self, text="СТАРТ!!!", command=self.on_start_click,
                                                    fg_color="#28a745", hover_color="#218838")
        self.start_button.grid(row=3, column=1, columnspan=2, padx=(20, 20), pady=5, sticky="nsew")
        
        # Фрейм для кнопок Пауза и Продолжить (чтобы они были в одну линию)
        self.controls_frame = customtkinter.CTkFrame(self)
        self.controls_frame.grid(row=4, column=1, columnspan=2, padx=(20, 20), pady=5, sticky="nsew")
        
        self.pause_button = customtkinter.CTkButton(master=self.controls_frame, text="ПАУЗА", command=self.on_pause_click, 
                                                    fg_color="#ffc107", hover_color="#e0a800", state="disabled")
        self.pause_button.grid(row=0, column=0, padx=(0, 5), pady=0, sticky="nsew")
        
        self.resume_button = customtkinter.CTkButton(master=self.controls_frame, text="ПРОДОЛЖИТЬ", command=self.on_resume_click, 
                                                     fg_color="#17a2b8", hover_color="#138496", state="disabled")
        self.resume_button.grid(row=0, column=1, padx=(5, 0), pady=0, sticky="nsew")
        
        # Растягиваем колонки внутри фрейма управления
        self.controls_frame.grid_columnconfigure(0, weight=1)
        self.controls_frame.grid_columnconfigure(1, weight=1)
        
        # Лейбл с результатом
        self.selected_file_label = customtkinter.CTkLabel(self, text="QR-код: ", anchor="w")
        self.selected_file_label.grid(row=5, column=1, columnspan=2, padx=20, pady=(10, 5), sticky="nsew")
        
        # Список результатов (растягивается вниз благодаря grid_rowconfigure(6, weight=1))
        self.listbox = CTkListbox(master=self, command=self.show_value)
        self.listbox.grid(row=6, column=1, columnspan=2, padx=15, pady=(5, 20), sticky="nsew")
        
        self.processing = False
        self.thread = None
        self.is_paused = False
    
    def select_video(self):
        self.file_path = askopenfilename(title="Выберите видео файл", filetypes=[("Видео файлы", "*.mp4;*.avi;*.mov;*.mkv;*.flv")])
        if self.file_path:
            print(f"Выбранный видео файл: {self.file_path}")
        else:
            print("Видео файл не выбран")
    
    def update_label(self, value):
        self.slider_value_label.configure(text=f"Значение: {int(float(value))}")
        print(f"Текущее значение слайдера: {int(float(value))}")
    
    def show_value(self, value):
        print(f"Выбранная опция: {value}")
    
    def on_start_click(self):
        if self.processing:
            print("[WARNING] Обработка уже запущена!")
            return
        
        radio_value = self.radio_var.get()
        if radio_value == 0:
            if not hasattr(self, 'file_path') or not self.file_path:
                print("Ошибка: Видео файл не выбран!")
                return
        
        reset_events()
        
        self.processing = True
        self.is_paused = False
        self.start_button.configure(state="disabled")
        self.pause_button.configure(state="normal")
        self.resume_button.configure(state="disabled")
        
        self.thread = threading.Thread(target=self.run_processing, daemon=True)
        self.thread.start()
    
    def on_pause_click(self):
        print("[INFO] Пауза...")
        toggle_pause()
        self.is_paused = True
        self.pause_button.configure(state="disabled")
        self.resume_button.configure(state="normal")
    
    def on_resume_click(self):
        print("[INFO] Продолжение...")
        toggle_pause()
        self.is_paused = False
        self.resume_button.configure(state="disabled")
        self.pause_button.configure(state="normal")
    
    def run_processing(self):
        try:
            radio_value = self.radio_var.get()
            switch_value = self.switch_1.get()
            entry_value = self.entry.get()
            slider_value = int(self.slider.get())
            
            print(f"Параметр для поиска: {entry_value}")
            print(f"Пропуск кадров: {slider_value}")
            
            if switch_value:
                print("Предобработка видео: Включена")
            else:
                print("Предобработка видео: Отключена")
            
            spisok = set()
            
            if radio_value == 0:
                print("Выбранный режим: Режим видео")
                spisok = realtime_scanning(self.file_path, entry_value, slider_value, switch_value)
            else:
                print("Выбранный режим: Веб-камера")
                spisok = camera_scanning(entry_value, slider_value, switch_value)
            
            self.after(0, self.update_listbox, spisok, entry_value)
            
        except Exception as e:
            print(f"[ERROR] Ошибка обработки: {e}")
        
        finally:
            self.after(0, self.reset_buttons)
    
    def update_listbox(self, spisok, entry_value):
        self.listbox.delete(0, 'end')
        k = 0
        for name in spisok:
            self.listbox.insert(k, name)
            k += 1
        
        if entry_value in spisok:
            self.selected_file_label.configure(text=f'QR-код: "{entry_value}" Найден!!!')
        else:
            self.selected_file_label.configure(text=f'QR-код: "{entry_value}" Не найден!!!')
    
    def reset_buttons(self):
        self.processing = False
        self.is_paused = False
        self.start_button.configure(state="normal")
        self.pause_button.configure(state="disabled")
        self.resume_button.configure(state="disabled")
        print("[INFO] Кнопки сброшены. Можно запустить заново.")

if __name__ == "__main__":
    app = App()
    app.mainloop()