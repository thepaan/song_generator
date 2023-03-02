# file writing requires admin privilege
import numpy as np
from pydub import AudioSegment
from pydub.generators import Sine
from pydub.playback import play



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

def generate_sine_wave(_frequency):
    sine_wave = Sine(_frequency, sample_rate=samplerate, bit_depth=bitdepth)
    return sine_wave

def generate_note(_note):
    note_duration = ms_per_beat * _note[2]
    # frequency multiplier, db reduction
    harmonics = [[2, 3], [3.025, 5]]
    note_audio = generate_sine_wave(frequency_table[_note[0]][_note[1]]).to_audio_segment(duration=note_duration)
    for harmonic in harmonics:
        harmonic_audio = generate_sine_wave(frequency_table[_note[0]][_note[1]] * harmonic[0]).to_audio_segment(duration=note_duration) - harmonic[1]
        note_audio = note_audio.overlay(harmonic_audio, position=0)
    # fades fix clicking sound during playback
    note_audio = note_audio.fade_in(10).fade_out(50)
    return note_audio



# Populate frequency table with notes from C0 to B8
for pitch in scale:
    for octave in range(9):
        if pitch not in frequency_table:
            frequency_table[pitch] = {octave: calculate_frequency(pitch, octave)}    
        else:
            frequency_table[pitch][octave] = calculate_frequency(pitch, octave)



# Test Song
# lines on treble staff (bottom up): Every Good Boy Deserves Football
#       E4 G4 B4 D5 F5
# spaces on staff (bottom up, starting on space below lowest line): D – FACE – G
#       D4 F4 A4 C5 E5 G5
#
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
    this_note = generate_note(note)
    if "song" in globals():
        song = song + this_note
    else:
        song = this_note

song.export("example.wav", format="wav")
