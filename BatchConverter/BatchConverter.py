import os
import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as messagebox
from tkinter import ttk
from pydub import AudioSegment

def convert_to_wav(input_file, output_directory):
    # Load the audio file
    audio = AudioSegment.from_file(os.path.join(output_directory, input_file))
    
    # # # Set the output file path
    output_file = os.path.join(output_directory, os.path.splitext(os.path.basename(input_file))[0] + ".wav")
    
    # Export the audio file as WAV
    audio.export(output_file, format="WAV")
    
    return output_file

def convert_directory(input_directory):
    file_count = sum(len(files) for _, _, files in os.walk(input_directory))
    progress['maximum'] = file_count
    progress['value'] = 0
    
    # Recursively iterate over all files and subdirectories in the input directory
    for root, dirs, files in os.walk(input_directory):
        for file_name in files:
            input_file = os.path.join(root, file_name)
            input_file = input_file.replace('\\', '/')                  
            try:
                output_file = convert_to_wav(input_file, root)
                print(f"File converted to WAV: {output_file}")
                os.remove(input_file)
                progress['value'] += 1
                root_window.update_idletasks()
            except Exception as e:
                print(f"Conversion failed for {input_file}: {str(e)}")
                return
        

def browse_directory(entry):
    directory = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, directory)

def convert_audio():
    input_directory = input_entry.get()
    
    if not input_directory:
        messagebox.showerror("Error", "Please select input directory.")
        return
    
    if not os.path.isdir(input_directory):
        messagebox.showerror("Error", "Invalid input directory.")
        return
    
    convert_directory(input_directory)
    messagebox.showinfo("Success", "Conversion completed.")

# Create the main window
root_window = tk.Tk()
root_window.title("Audio Converter")

# Create directory selection frame
directory_frame = tk.Frame(root_window)
directory_frame.pack(pady=10)

input_label = tk.Label(directory_frame, text="Select input directory:")
input_label.grid(row=0, column=0)

input_entry = tk.Entry(directory_frame, width=50)
input_entry.grid(row=0, column=1)

input_button = tk.Button(directory_frame, text="Browse", command=lambda: browse_directory(input_entry))
input_button.grid(row=0, column=2)

# Create progress bar
progress_frame = tk.Frame(root_window)
progress_frame.pack(pady=10)

progress_label = tk.Label(progress_frame, text="Conversion Progress:")
progress_label.pack()

progress = ttk.Progressbar(progress_frame, orient="horizontal", length=300, mode="determinate")
progress.pack()

# Create convert button
convert_button = tk.Button(root_window, text="Convert", command=convert_audio)
convert_button.pack(pady=10)

root_window.mainloop()
