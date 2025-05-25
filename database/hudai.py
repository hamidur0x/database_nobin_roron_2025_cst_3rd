import time
import os
import sys

# Timestamps to display (in seconds)
# Format: (timestamp_from_start, value_to_display, typing_delay_per_char)
timed_displays = [
    (4.93, "Is jawani me humne ye kya kar diya", 0.12),  # Increased delay for a slower typing speed
    (9.28, "Ishq me tere khud ko fana kar diya.", 0.12),  # Increased delay
    (14.37, "Mai to tujh me hi hu, tu na mujhme rha", 0.12), # Increased delay
    (19.50, "Meri mosikiyon me tu Zinda rha..", 0.12), # Increased delay
]

# Function to clear the screen (cross-platform)
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to display text with a typing effect
def type_effect(text, custom_delay=0.05):
    sys.stdout.write("\t\t\t") # Centering effect
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(custom_delay)
    print() # Move to the next line after the phrase is typed

# Start the timer
start_time = time.time()

# Initial clear to start with a clean screen
clear_screen()
print("\n\n") # Add some initial newlines for spacing

# Display the timestamps in sync with typing effect, stacking
for entry in timed_displays:
    timestamp_trigger = entry[0]
    value_to_show = entry[1]
    delay = entry[2]

    # Wait until the specified timestamp is reached
    while time.time() - start_time < timestamp_trigger:
        time.sleep(0.01) # Small sleep to avoid busy-waiting

    # Display the value with typing effect
    type_effect(value_to_show, delay)