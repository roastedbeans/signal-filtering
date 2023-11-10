#Name: Vincent D. Abella
#ID: 18101371
#Date Modified: May 5, 2023
################################################################
#Title: ABELLA_NotchNoiseFiltering
################################################################
#Description:
#The code is developed to input an audio file, filter the noise,
#and output the filtered audio file.
################################################################
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import tkinter as tk
from tkinter import filedialog, messagebox

class AudioFilterGUI:
    def __init__(self, master):
        self.master = master
        self.data = None
        self.sr = None
        self.filteredData = None
        self.startFreq = tk.DoubleVar(value=500.0)
        self.endFreq = tk.DoubleVar(value=12000.0)

        # Create button to load audio file
        self.loadButton = tk.Button(master, text="Load Audio", command=self.loadAudio)
        self.loadButton.pack(padx=20, pady=5)

        # Create button to plot original signal
        self.plotButton = tk.Button(master, text="Plot Signal", command=self.plot)
        self.plotButton.pack(padx=20, pady=5)

        # Create button to filter audio file
        self.filterButton = tk.Button(master, text="Filter Audio", command=self.filterAudio)
        self.filterButton.pack(padx=20, pady=5)

        # Create button to export filtered audio file
        self.exportButton = tk.Button(master, text="Export Audio", command=self.exportAudio)
        self.exportButton.pack(padx=20, pady=5)

        # Create entry for start frequency of noise band
        tk.Label(master, text="Start Frequency (Hz)").pack()
        self.entryFreqStart = tk.Entry(master, textvariable=self.startFreq)
        self.entryFreqStart.pack(padx=30, pady=10)

        # Create entry for end frequency of noise band
        tk.Label(master, text="End Frequency (Hz)").pack()
        self.entryFreqEnd = tk.Entry(master, textvariable=self.endFreq)
        self.entryFreqEnd.pack(padx=30, pady=10)

    def loadAudio(self):
        # Open file dialog to select audio file
        filename = filedialog.askopenfilename(initialdir="./", title="Select Audio File", filetypes=[("Audio Files", "*.wav *.mp3")])

        # Load audio file
        self.data, self.sr = sf.read(filename)

    def plot(self):
        if self.data is not None:
            # Plot original signal
            plt.figure(figsize=(8,3))
            plt.plot(self.data)
            plt.title('Original Signal')
            plt.xlabel('Sample')
            plt.ylabel('Amplitude')

            # Perform FFT
            FFTData = np.fft.rfft(self.data)

            # Compute PSD
            PSDData = np.abs(FFTData)**2 / len(self.data)

            # Plot PSD
            plt.figure(figsize=(8,3))
            plt.plot(np.fft.rfftfreq(len(self.data), d=1/self.sr), PSDData)
            plt.title('Power Spectral Density')
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('Power')
            plt.show()
        else:
            tk.messagebox.showerror("Error", "No audio file selected.")

    def filterAudio(self):
        if self.data is not None:
            # Perform FFT
            FFTData = np.fft.rfft(self.data)

            # Compute PSD
            PSDData = np.abs(FFTData)**2 / len(self.data)

            # Set noise frequency band
            noiseStart = self.startFreq.get() # start of noise frequency band in Hz
            noiseEnd = self.endFreq.get() # end of noise frequency band in Hz

            # Find indices of noise frequencies
            freqs = np.fft.rfftfreq(len(self.data), d=1/self.sr)
            noiseIndices = np.where((freqs >= noiseStart) & (freqs <= noiseEnd))[0]

            # Apply notch filter to noise frequencies
            notchFilter = np.ones(len(PSDData))
            notchFilter[noiseIndices] = 0
            filteredPSDData = PSDData * notchFilter

            # Apply inverse FFT to get filtered signal
            self.filteredData = np.fft.irfft(FFTData * notchFilter)

            # Plot PSD before and after filtering
            plt.figure(figsize=(8,3))
            plt.plot(freqs, PSDData, label='Before Filtering')
            plt.plot(freqs, filteredPSDData, label='After Filtering')
            plt.title('Power Spectral Density')
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('Power')
            plt.legend()

             # Plot filtered signal
            plt.figure(figsize=(8,3))
            plt.plot(self.data, label='Original Data')
            plt.plot(self.filteredData, label='Filtered Data')
            plt.title('Filtered Signal')
            plt.xlabel('Sample')
            plt.ylabel('Amplitude')
            plt.legend()
            plt.show()
        else:
            tk.messagebox.showerror("Error", "No audio file selected.")

    def exportAudio(self):
        if self.filteredData is not None:
            # Open file dialog
            filename = filedialog.asksaveasfilename(initialdir="./", title="Save Filtered Audio", defaultextension=".wav", filetypes=[("WAV Files", "*.wav")])

            # Export filtered audio file
            sf.write(filename, self.filteredData, self.sr)
        else:
            tk.messagebox.showerror("Error", "No filtered audio data available.")

# Create main window
root = tk.Tk()
root.title("Audio Filter")

# Create AudioFilterGUI instance
gui = AudioFilterGUI(root)

# Run main loop
root.mainloop()