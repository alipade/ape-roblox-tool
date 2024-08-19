import tkinter as tk
from tkinter import ttk
from tkinter import Menu
from PIL import Image, ImageTk
import json
import pyperclip
import datetime
import math
import string
import random
import threading
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

ASSETS_PATH = "assets/"
IMAGES_PATH = ASSETS_PATH + "images/"
JSON_FILE_PATH = "accounts.json"

class ApeRobloxToolApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ape Roblox Tool")
        self.geometry("800x400")
        self.resizable(False, False)
        self.iconbitmap(IMAGES_PATH + "Ape.ico")

        self.create_widgets()
        self.load_data()
        self.create_context_menu()

    def create_widgets(self):
        style = ttk.Style()
        style.configure("TFrame", background="lightgray")
        style.configure("TButton", padding=6, relief="flat")
        style.configure("TLabel", background="lightgray", padding=6)
        
        self.data_frame = ttk.Frame(self, width=600, height=390)
        self.data_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.control_frame = ttk.Frame(self, width=185, height=390)
        self.control_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        self.ape_image_tk = self.load_image(IMAGES_PATH + "Ape.png", (100, 100))
        self.ape_icon_label = tk.Label(self.control_frame, image=self.ape_image_tk)
        self.ape_icon_label.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        self.username_label = ttk.Label(self.control_frame, text="Base Username:")
        self.username_label.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")

        self.username_textbox = ttk.Entry(self.control_frame)
        self.username_textbox.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        
        self.password_label = ttk.Label(self.control_frame, text="Password:")
        self.password_label.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="w")

        self.password_textbox = ttk.Entry(self.control_frame, show="*")
        self.password_textbox.grid(row=4, column=0, padx=10, pady=5, sticky="ew")
        
        self.start_button = ttk.Button(self.control_frame, text="Start", command=self.start_action)
        self.start_button.grid(row=5, column=0, padx=10, pady=10, sticky="ew")
        
        self.stop_button = ttk.Button(self.control_frame, text="Stop", command=self.stop_action)
        self.stop_button.grid(row=5, column=1, padx=10, pady=10, sticky="ew")

        self.control_frame.columnconfigure(0, weight=1)
        self.control_frame.columnconfigure(1, weight=1)

        self.tree = ttk.Treeview(self.data_frame, columns=("Username", "Description", "Creation Date"), show="headings")
        self.tree.heading("Username", text="Username")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Creation Date", text="Creation Date")

        self.tree.pack(fill="both", expand=True)

        self.tree.bind("<Button-3>", self.show_context_menu)

    def load_image(self, path, size):
        image_pil = Image.open(path).resize(size)
        return ImageTk.PhotoImage(image_pil)

    def load_data(self):
        try:
            with open(JSON_FILE_PATH, 'r') as file:
                data = json.load(file)
                for item in data:
                    username = item.get("Username", "")
                    description = item.get("Description", "")
                    creation_date = item.get("Creation Date", "")
                    self.tree.insert("", "end", values=(username, description, creation_date))
        except FileNotFoundError:
            print(f"File {JSON_FILE_PATH} not found.")
        except json.JSONDecodeError:
            print("Error decoding JSON file.")

    def start_action(self):
        threading.Thread(target=self.run_driver).start()
    
    def run_driver(self):
        print("Start button clicked")
        new_username = self.username_textbox.get() + ''.join(random.choices(string.ascii_uppercase, k=5))
        new_password = self.password_textbox.get()

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--window-size=500,500")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        
        self.driver.get("https://www.roblox.com/")

        months_element = self.driver.find_element(By.XPATH, '/html/body/div[3]/div/section/div/div[2]/div[1]/div[2]/div[1]/div/div/div/div[1]/div/div[1]/div[1]/select')
        days_element = self.driver.find_element(By.XPATH, '/html/body/div[3]/div/section/div/div[2]/div[1]/div[2]/div[1]/div/div/div/div[1]/div/div[1]/div[2]/select')
        years_element = self.driver.find_element(By.XPATH, '/html/body/div[3]/div/section/div/div[2]/div[1]/div[2]/div[1]/div/div/div/div[1]/div/div[1]/div[3]/select')
        login_username_field = self.driver.find_element(By.XPATH, "/html/body/div[3]/div/section/div/div[2]/div[1]/div[2]/div[1]/div/div/div/div[2]/input")
        login_password_field = self.driver.find_element(By.XPATH, "/html/body/div[3]/div/section/div/div[2]/div[1]/div[2]/div[1]/div/div/div/div[3]/input")
        female_button = self.driver.find_element(By.XPATH, '/html/body/div[3]/div/section/div/div[2]/div[1]/div[2]/div[1]/div/div/div/div[4]/div/div/button[1]')
        male_button = self.driver.find_element(By.XPATH, '/html/body/div[3]/div/section/div/div[2]/div[1]/div[2]/div[1]/div/div/div/div[4]/div/div/button[2]')
        signup_button = self.driver.find_element(By.XPATH, '/html/body/div[3]/div/section/div/div[2]/div[1]/div[2]/div[1]/div/div/div/button')

        Select(months_element).select_by_index(random.randrange(1, len(Select(months_element).options)))
        Select(days_element).select_by_index(random.randrange(1, len(Select(days_element).options)))
        Select(years_element).select_by_index(random.randrange(13, len(Select(years_element).options)))

        login_username_field.send_keys(new_username)
        login_password_field.send_keys(new_password)

        random_gender = random.choice(["Female", "Male"])
        if random_gender == 'Female':
            female_button.click()
            pass
        elif random_gender == 'Male':
            male_button.click()
            pass

        while True:
            if signup_button.is_enabled():
                signup_button.click()
                break

        try:
            WebDriverWait(self.driver, math.inf).until(EC.url_to_be('https://www.roblox.com/home?nu=true'))

            creation_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            new_account = {
                "Username": new_username,
                "Password": new_password,
                "Description": "N/A",
                "Creation Date": creation_date
            }
                
            try:
                with open(JSON_FILE_PATH, 'r') as file:
                    data = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                data = []

            data.append(new_account)

            with open(JSON_FILE_PATH, 'w') as file:
                json.dump(data, file, indent=4)

            self.tree.insert("", "end", values=(new_username, "N/A", creation_date))

            self.driver.quit()
            
        except:
            self.driver.quit()

    def stop_action(self):
        print("Stop button clicked")
        self.driver.quit()

    def create_context_menu(self):
        self.context_menu = Menu(self, tearoff=0)
        self.context_menu.add_command(label="Copy Username", command=self.copy_username)
        self.context_menu.add_command(label="Copy Password", command=self.copy_password)
        self.context_menu.add_command(label="Copy Combo", command=self.copy_combo)
        self.context_menu.add_command(label="Copy Description", command=self.copy_description)
        self.context_menu.add_command(label="Copy Creation Date", command=self.copy_creation_date)

    def show_context_menu(self, event):
        selected_item = self.tree.identify_row(event.y)
        if selected_item:
            self.tree.selection_set(selected_item)
            self.context_menu.post(event.x_root, event.y_root)

    def copy_username(self):
        selected_item = self.tree.selection()[0]
        username = self.tree.item(selected_item, "values")[0]
        pyperclip.copy(username)
        print(f"Copied Username: {username}")

    def copy_password(self):
        selected_item = self.tree.selection()[0]
        username = self.tree.item(selected_item, "values")[0]
        password = self.get_data_from_username(username, "Password")
        pyperclip.copy(password)
        print(f"Copied Password for {username}: {password}")

    def copy_combo(self):
        selected_item = self.tree.selection()[0]
        username = self.tree.item(selected_item, "values")[0]
        combo = self.get_data_from_username(username, "Combo")
        pyperclip.copy(combo)
        print(f"Copied Combo for {username}: {combo}")

    def copy_description(self):
        selected_item = self.tree.selection()[0]
        description = self.tree.item(selected_item, "values")[1]
        pyperclip.copy(description)
        print(f"Copied Description: {description}")

    def copy_creation_date(self):
        selected_item = self.tree.selection()[0]
        creation_date = self.tree.item(selected_item, "values")[2]
        pyperclip.copy(creation_date)
        print(f"Copied Creation Date: {creation_date}")

    def get_data_from_username(self, username, value_type):
        with open(JSON_FILE_PATH, 'r') as file:
            data = json.load(file)
            for item in data:
                if item.get("Username", "") == username:
                    if value_type == "Password":
                        return item.get("Password", "")
                    elif value_type == "Combo":
                        return item.get("Username", "") + ":" + item.get("Password", "")
                    elif value_type == "Description":
                        return item.get("Description", "")
                    elif value_type == "Creation Date":
                        return item.get("Creation Date", "")
        return ""
    

if __name__ == "__main__":
    app = ApeRobloxToolApp()
    app.mainloop()
