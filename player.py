import serial
import pygame
import numpy as np
import time

# First element of list = Left Hand
# Second element of list = Right Hand
DATA_AMOUNT = 2

# Mapping defined as follows:
# [ID = 0] Left Hand (3 octave): C2 C3 C4 (C2: 0-119, C3: 120-239, C4: 240-359)
# [ID = 1] Right Hand (3 octave): C3 C4 C5 (C3: 0-119, C4: 120-239, C5: 240-359)
# -1 = Out of range / No sound input from user
global mainlist
mainlist = []
for i in range(0, DATA_AMOUNT):
    mainlist.append(-1)

global playing_notes
playing_notes = {}

global tempL_note
tempL_note = -1

global tempR_note
tempR_note = -1

# Initialize the mixer and set the sample rate
pygame.mixer.init(44100, -16, 1, 4096)

# Define the mapping between keys and notes
key_notes = {
    "C2": 65,   # 1
    "C#2": 69,  # 2
    "D2": 73,   # 3
    "D#2": 78,  # 4
    "E2": 82,   # 5
    "F2": 87,   # 6
    "F#2": 93,  # 7
    "G2": 98,   # 8
    "G#2": 104, # 9
    "A2": 110,  # 10
    "A#2": 117, # ...
    "B2": 123,

    "C3": 131,
    "C#3": 139,
    "D3": 147,
    "D#3": 156,
    "E3": 165,
    "F3": 175,
    "F#3": 185,
    "G3": 196,
    "G#3": 208,
    "A3": 220,
    "A#3": 233,
    "B3": 247,

    "C4": 261,
    "C#4": 277,
    "D4": 294,
    "D#4": 311,
    "E4": 330,
    "F4": 349,
    "F#4": 370,
    "G4": 392,
    "G#4": 415,
    "A4": 440,
    "A#4": 466,
    "B4": 494,

    "C5": 523,
    "C#5": 554,
    "D5": 587,
    "D#5": 622,
    "E5": 659,
    "F5": 698,
    "F#5": 740,
    "G5": 784,
    "G#5": 831,
    "A5": 880,
    "A#5": 932,
    "B5": 988,

    "C6": 1047
}

# [FUNCTION] Generate a square wave sample for a given frequency
def generate_sample(frequency):
    sample_rate = pygame.mixer.get_init()[0]
    duration = 1  # Adjust this to control the note duration
    num_samples = int(duration * sample_rate)
    sample = np.zeros((num_samples,))
    t = np.linspace(0, duration, num_samples, False)
    sample += 0.5 * np.cos(2 * np.pi * frequency * t)
    sample = sample * 32767
    return sample.astype(np.int16)

# [FUNCTION] Refresh data from Arduino to Python script
def updateData(connIn):
    global mainlist
    try:
        tempdata = connIn.readline().decode('utf-8').split()
        if not tempdata:
            pass
        else:
            for i in range(0, DATA_AMOUNT):
                mainlist[i] = tempdata[i]
    except Exception as e:
        print(f"Error: {e}")

# [FUNCTION] Based on ultrasonic sensor data input, find note name requested
def keyFinder(ID, value):
    if value >= 0:
        note = ""
        
        octave = int(value / 12)
        offset = 4 + ID
        note_pos = value % 12

        if note_pos == 0:
            note = "C" + str(octave + offset)
        elif note_pos == 1:
            note = "C#" + str(octave + offset)
        elif note_pos == 2:
            note = "D" + str(octave + offset)
        elif note_pos == 3:
            note = "D#" + str(octave + offset)
        elif note_pos == 4:
            note = "E" + str(octave + offset)
        elif note_pos == 5:
            note = "F" + str(octave + offset)
        elif note_pos == 6:
            note = "F#" + str(octave + offset)
        elif note_pos == 7:
            note += "G" + str(octave + offset)
        elif note_pos == 8:
            note = "G#" + str(octave + offset)
        elif note_pos == 9:
            note = "A" + str(octave + offset)
        elif note_pos == 10:
            note = "A#" + str(octave + offset)
        elif note_pos == 11:
            note = "B" + str(octave + offset)
        else:
            note = "None"
        print(f"Octave: {octave} | Offset: {offset} | Notepos: {note_pos} | Note: {note}")
        return note
    else:
        return "None"

def main():
    global tempL_note
    global tempR_note
    global playing_notes
    
    # Initialize serial data from device
    arduinoMega = serial.Serial(port='COM4', baudrate=115200, timeout=.1)

    # Initialize pygame
    pygame.init()

    # Set the window title
    pygame.display.set_caption('Synthesizer')

    # Create a Pygame screen (required for capturing keyboard events)
    screen = pygame.display.set_mode((300, 300))

    # Start the main loop
    running = True
    while running:
        updateData(arduinoMega) # Update data from Arduino
        print(f"Mainlist: {mainlist} | Pressed Keys: {playing_notes}")

        noteL = int(mainlist[0])
        noteR = int(mainlist[1])


        if noteL != tempL_note:
            temp_name = keyFinder(0, int(tempL_note))
            if temp_name in playing_notes:
                playing_notes[temp_name].stop()
                del playing_notes[temp_name]
            tempL_note = noteL
            if noteL >= 0:
                print(f"[!NOTE CHANGE!] Left Note: {keyFinder(0, int(mainlist[0]))}")
                note_name = keyFinder(0, int(mainlist[0]))
                frequency = key_notes[note_name]
                sample = generate_sample(frequency)
                playing_notes[note_name] = pygame.mixer.Sound(sample)
                playing_notes[note_name].play(loops=-1)  # Play continuously

        if noteR != tempR_note:
            temp_name = keyFinder(1, int(tempR_note))
            if temp_name in playing_notes:
                playing_notes[temp_name].stop()
                del playing_notes[temp_name]
            tempR_note = noteR
            if noteR >= 0:
                print(f"[!NOTE CHANGE!] Right Note: {keyFinder(1, int(mainlist[1]))}")
                note_name = keyFinder(1, int(mainlist[1]))
                frequency = key_notes[note_name]
                sample = generate_sample(frequency)
                playing_notes[note_name] = pygame.mixer.Sound(sample)
                playing_notes[note_name].play(loops=-1)  # Play continuously

        # Check for keyboard events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Add a delay to reduce the CPU usage of the while loop
        time.sleep(0.01)

    # Stop playing any remaining notes and quit pygame
    for sound in playing_notes.values():
        sound.stop()
    pygame.quit()
    
if __name__ == '__main__': 
    main() 