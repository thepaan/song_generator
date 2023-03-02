# file writing requires admin privilege
import numpy as np
from pydub import AudioSegment
from pydub.generators import Sine



A4_tuning = 440
samplerate = 44100
bitdepth = 16
tempo = 60
ms_per_beat = 1000 / (tempo / 60)
amplitude = np.iinfo(np.int16).max
scale = ["C", "Cs", "D", "Ef", "E", "F", "Fs", "G", "Gs", "A", "Bf", "B"]
frequency_table = {}
music_sheet = []



def calculate_frequency(_pitch, _octave):
    semitone_offset = (scale.index(_pitch) - 9) + (_octave - 4) * 12
    note_frequency = A4_tuning * pow(2, (semitone_offset / 12))
    return note_frequency



for pitch in scale:
    for octave in range(9):
        if pitch not in frequency_table:
            frequency_table[pitch] = {octave: calculate_frequency(pitch, octave)}    
        else:
            frequency_table[pitch][octave] = calculate_frequency(pitch, octave)


# note pitch, note octave, note value
music_sheet = [["E", 4, 0.25],
               ["D", 4, 0.25],
               ["C", 4, 0.25],
               ["D", 4, 0.25],
               ["E", 4, 0.25],
               ["E", 4, 0.25],
               ["E", 4, 0.5],
               ["D", 4, 0.25],
               ["D", 4, 0.25],
               ["D", 4, 0.5],
               ["E", 4, 0.25],
               ["G", 4, 0.25],
               ["G", 4, 0.5]]



for note in music_sheet:
    this_sine_wave = Sine(frequency_table[note[0]][note[1]], sample_rate=samplerate, bit_depth=bitdepth)
    this_sine_segment = this_sine_wave.to_audio_segment(duration=ms_per_beat * note[2])
    if "song" in globals():
        song = song + this_sine_segment
    else:
        song = this_sine_segment

song.export("example.wav", format="wav")
