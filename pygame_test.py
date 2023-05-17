import pygame
import numpy as np
import time

# Initialize the mixer and set the sample rate
pygame.mixer.init(44100, -16, 1, 4096)

# Define the mapping between keys and notes
key_notes = {
    pygame.K_a: 440,   # A4
    pygame.K_s: 494,   # B4
    pygame.K_d: 523,   # C5
    pygame.K_f: 587,   # D5
    pygame.K_g: 659,   # E5
    pygame.K_h: 698,   # F5
    pygame.K_j: 784    # G5
}

# Generate a square wave sample for a given frequency
def generate_sample(frequency):
    sample_rate = pygame.mixer.get_init()[0]
    duration = 1  # Adjust this to control the note duration
    num_samples = int(duration * sample_rate)
    sample = np.zeros((num_samples,))
    t = np.linspace(0, duration, num_samples, False)
    sample += 0.5 * np.cos(2 * np.pi * frequency * t)
    sample = sample * 32767
    return sample.astype(np.int16)

# Initialize pygame
pygame.init()

# Set the window title
pygame.display.set_caption('Synthesizer')

# Create a Pygame screen (required for capturing keyboard events)
screen = pygame.display.set_mode((400, 300))

# Track the pressed keys and their corresponding notes
pressed_keys = {}

# Start the main loop
running = True
while running:
    # Check for keyboard events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            # Check if the pressed key is mapped to a note
            if event.key in key_notes:
                # Add the pressed key to the dictionary if it's not already there
                if event.key not in pressed_keys:
                    frequency = key_notes[event.key]
                    sample = generate_sample(frequency)
                    pressed_keys[event.key] = pygame.mixer.Sound(sample)
                    pressed_keys[event.key].play(loops=-1)  # Play continuously

        elif event.type == pygame.KEYUP:
            # Check if the released key is mapped to a note and stop playing it
            if event.key in pressed_keys:
                pressed_keys[event.key].stop()
                del pressed_keys[event.key]

        elif event.type == pygame.QUIT:
            running = False

    # Add a delay to reduce the CPU usage of the while loop
    time.sleep(0.01)

# Stop playing any remaining notes and quit pygame
for sound in pressed_keys.values():
    sound.stop()
pygame.quit()