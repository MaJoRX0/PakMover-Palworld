import utils
import tkinter
import customtkinter as ct
from tkinter.filedialog import askdirectory
import sys
import datetime
import json
import os
import ctypes
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
process_array = (ctypes.c_uint8 * 1)()
num_processes = kernel32.GetConsoleProcessList(process_array, 1)
if num_processes < 3: ctypes.WinDLL('user32').ShowWindow(kernel32.GetConsoleWindow(), 0)


original_write = sys.stdout.write



def save_settings():
    if not PalworldPathT.get() and not ChunksPathT.get():
        return
    settings = {
        "PalworldPath": PalworldPathT.get(),
        "ChunksPath": ChunksPathT.get(),
        "CheckBox": checkbox.get()
    }
    local_appdata_folder = os.getenv('LOCALAPPDATA')

    # Construct the full path to the PakUtil folder
    pakutil_folder = os.path.join(local_appdata_folder, "PakMover")

    # Ensure the PakUtil folder exists
    if not os.path.exists(pakutil_folder):
        os.makedirs(pakutil_folder)

    settings_file_path = os.path.join(pakutil_folder, "settings.json")
    with open(settings_file_path, "w") as f:
        json.dump(settings, f)

# Function to load settings from a JSON file
def load_settings():
    global PalworldPath, ChunksPath, CheckBoxV
    try:
        # Get the path to the AppData/Local folder
        local_appdata_folder = os.getenv('LOCALAPPDATA')

        # Construct the full path to the PakUtil folder
        pakutil_folder = os.path.join(local_appdata_folder, "PakMover")

        # Construct the full path to the settings file in the PakUtil folder
        settings_file_path = os.path.join(pakutil_folder, "settings.json")

        with open(settings_file_path, "r") as f:
            settings = json.load(f)
            PalworldPath = settings.get("PalworldPath", PalworldPath)
            PalworldPathT.delete(0, 1000)
            PalworldPathT.insert(0, PalworldPath)

            CheckBoxV = settings.get("CheckBox", CheckBoxV)
            if CheckBoxV == 1:
                checkbox.select()
            else:
                checkbox.deselect()
            ChunksPath = settings.get("ChunksPath", ChunksPath)
            ChunksPathT.delete(0, 1000)
            ChunksPathT.insert(0, ChunksPath)


    except FileNotFoundError:
        # Handle the case where the settings file doesn't exist
        pass

# Call load_settings at the beginning of your script to load settings when the app launches

def hooked_write(text):
    # Add your custom code here
    original_write(text)
    if text =="\n":
        return

    timestamp = datetime.datetime.now().strftime("[%H:%M]")
    text_1.insert("end", f"{timestamp} {text}\n")
    text_1.see("end")

def on_close():
    save_settings()
    app.destroy()
sys.stdout.write = hooked_write
ct.set_appearance_mode("dark")
ct.set_default_color_theme("dark-blue")

app = ct.CTk()
app.geometry("830x450")
app.title("PakMover")
app.protocol("WM_DELETE_WINDOW", on_close)

PalworldPath = r"C:/Program Files (x86)/Steam/steamapps/common/Palworld"
ChunksPath = r"C:/Modding/PalworldModdingKit/Pkg/Windows/Pal/Content/Paks"

CheckBoxV = 0

def updatecheckbox():
    global  CheckBoxV
    CheckBoxV = checkbox.get()
def BrowseButtons(button):
        global PalworldPath
        global ChunksPath

        filename = askdirectory()
        if button == "Chunks":
            ChunksPath = filename
            ChunksPathT.delete(0, 1000)
            ChunksPathT.insert(0, ChunksPath)
        elif button == "Palworld":
            PalworldPath = filename
            PalworldPathT.delete(0, 1000)
            PalworldPathT.insert(0, PalworldPath)

def StartMain():
    global ChunksPath
    global PalworldPath
    if ChunksPathT.get() != "":
        ChunksPath = ChunksPathT.get()
    if PalworldPathT.get() != "":
        PalworldPath = PalworldPathT.get()
    files = utils.read_and_extract_keywords_from_pak_files(ChunksPath)
    logicfolder = utils.find_logic_mods_folder(PalworldPath)
    utils.copy_and_rename_pak_files(files, logicfolder)
    if CheckBoxV == 1:
        utils.launch_program(rf"{PalworldPath}\palworld.exe")

frame_1 = ct.CTkFrame(master=app)
frame_1.pack(pady=20, padx=60, expand=True , fill="both")

label_2 = ct.CTkLabel(master=frame_1, justify=tkinter.LEFT, text="PakMover",font=ct.CTkFont("Arial",20,"bold"))
label_2.pack(pady=3)

label_1 = ct.CTkLabel(master=frame_1, justify=tkinter.LEFT, text="_"*100,font=ct.CTkFont("Arial",20,"bold"))
label_1.pack()


container_frame= ct.CTkFrame(master=frame_1)
container_frame.pack(pady=(10, 0), padx=10)
container_frame.rowconfigure(1, minsize=50)

label_2 = ct.CTkLabel(master=container_frame, text="Palworld Path: ",font=ct.CTkFont("Arial",14,"bold"))
label_2.grid(row=0, column=0, padx=(5, 0), pady=(5, 0))

PalworldPathT = ct.CTkEntry(width=500, master=container_frame, placeholder_text=PalworldPath)
PalworldPathT.grid(row=0, column=1, padx=(5, 0), pady=(5, 0))

FileChooserPal = ct.CTkButton(width=10, master=container_frame, text="Browse",  command=lambda: BrowseButtons("Palworld"))
FileChooserPal.grid(row=0, column=2, padx=(5,5), pady=(5, 0))

# Add space between rows


label_2 = ct.CTkLabel(master=container_frame, text="Chunks Path: ",font=ct.CTkFont("Arial",14,"bold"))
label_2.grid(row=1, column=0, padx=(5, 0), pady=(5, 0))

ChunksPathT = ct.CTkEntry(width=500, master=container_frame, placeholder_text=ChunksPath)
ChunksPathT.grid(row=1, column=1, padx=(5, 0), pady=(5, 0))

FileChooserChunk = ct.CTkButton(width=10, master=container_frame, text="Browse", command=lambda: BrowseButtons("Chunks"))
FileChooserChunk.grid(row=1, column=2, padx=(5,5), pady=(5, 0))


check_var = ct.StringVar(value="on")
checkbox = ct.CTkCheckBox(master=container_frame, text="Launch Game",font=ct.CTkFont("Arial",12,"bold"), variable=check_var,command=updatecheckbox)
checkbox.grid(row=2, column=0, padx=(5,0),pady=(0,5))

text_1 = ct.CTkTextbox(master=frame_1, width=600, height=150,font=ct.CTkFont("Arial",15))
text_1.pack(pady=(10,0), padx=10,expand=True, fill="both")

button_1 = ct.CTkButton(width=600,master=frame_1,text="Start", command=StartMain)
button_1.pack(pady=(10,0), padx=10, fill="both")
load_settings()
app.mainloop()











r"""
if __name__ == "__main__":
    # Path to the exe file

    directory_path = r"C:\Users\c9o\PycharmProjects\PakMover"
    files = utils.read_and_extract_keywords_from_pak_files(directory_path)

    destination_directory = r"E:\Games\Steam or any shop\Steam\steamapps\common\Palworld\Pal\Content\Paks\LogicMods"  # Adjust as needed
    utils.copy_and_rename_pak_files(files, destination_directory)

    gamepath = r"E:\Games\Steam or any shop\Steam\steamapps\common\Palworld"
    logicfolder = utils.find_logic_mods_folder(gamepath)

    utils.launch_program(rf"{gamepath}\palworld.exe")

"""