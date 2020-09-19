# FILE : wave_editor.py
# EXERCISE 6: intro2cs1 2019
# DESCRIPTION: Wave Editor Program

import os
import wave_helper
import copy
import math


class Sound:
    """
    Holds constants for the entire program.
    """
    MAX_VOLUME = 32767
    MIN_VOLUME = -32768
    DEFAULT_SAMPLE_RATE = 2000
    VOL_INCREASE = 1.2
    VOL_DECREASE = 5 / 6
    SPEED_UP = 1
    SPEED_DOWN = 0
    # input validity purpose constants
    NAVIGATE = "navigate"
    MANIPULATE = "manipulate"
    COMPOSE = "compose"
    SAVE_FILE = "save_file"


def main_menu():
    """
    Prints the main menu and navigates between chosen operations.
    Terminates when the given input is 3.
    :return: None
    """
    print("Welcome to Wave Editor!")
    terminate = False
    while not terminate:
        print("Main Menu")
        print("--------------------")
        print("What can I do for you ? Insert a number :")
        print("1 - Edit existing audio")
        print("2 - Compose a new melody")
        print("3 - Exit")
        choice = user_input("", Sound.NAVIGATE, menu_length=3)
        if choice == '1':
            manipulation()
        elif choice == '2':
            composition()
        else:  # Exit program
            terminate = True
            print("we started with a simple hello but ended with a "
                  "complicated goodbye :( ")


def manipulation(internal_data=None):
    """
    Prints edit menu and handles user choice of audio manipulation.
    Returns back to main menu when input is 7.
    :return: None
    """
    if internal_data is None:
        audio = list(user_input("Enter your filename to edit : ",
                                Sound.MANIPULATE))
    else:
        audio = list(internal_data)

    audio_data = copy.deepcopy(audio[1])

    print("Loaded file successfully")
    choice = 0  # user's choice in edit menu

    # Edit menu
    while choice != 7:  # 7 = Move to exit menu

        print("Which change would like me to do?")
        msg = "1. Reverse \n2. Speed up \n3. Slow down \n4. Volume up\n" \
              "5. Volume down \n6. Low pass filter \n7. Exit Menu\n"
        choice = int(user_input(msg, Sound.NAVIGATE, menu_length=7))

        if choice == 1:
            audio[1] = reverse_audio(audio_data)
            print("The audio has been reversed")
        elif choice == 2:
            audio[1] = speed_change(audio_data, Sound.SPEED_UP)
            print("The audio speed is faster now")
        elif choice == 3:
            audio[1] = speed_change(audio_data, Sound.SPEED_DOWN)
            print("The audio speed has slowed down")
        elif choice == 4:
            audio[1] = change_volume(audio_data, Sound.VOL_INCREASE)
            print("Volume increased")
        elif choice == 5:
            audio[1] = change_volume(audio_data, Sound.VOL_DECREASE)
            print("Volume decreased")
        elif choice == 6:
            audio[1] = low_pass_filter(audio_data)
            print("Low pass filter applied")
        else:  # 7 = Exit Menu
            save_audio(audio)  # saves changes and return to main menu
        audio_data = audio[1]  # commit to changes before moving to next iter'


def save_audio(audio):
    """
    Saves the audio to a file and returns to main menu
    :param audio: 2D list which holds (frame rate, audio data)
    :return: None
    """
    output_filename = user_input("Enter a file name to save your changes : ",
                                 Sound.SAVE_FILE)
    saved = wave_helper.save_wave(audio[0], audio[1], output_filename)
    if saved == 0:
        print("All changes saved \n")
    else:
        print("Error : your changes could not be saved")


def composition():
    """
    Composes a melody by instructions.
    :return: None
    """
    raw_instructions = user_input\
        ("Provide instructions file name: ", Sound.COMPOSE)
    audio = compose_melody(raw_instructions)
    manipulation(audio)  # Redirecting to edit menu


def compose_melody(raw_instructions):
    """
    Composes a melody by the instructions specified.
    :param raw_instructions: list[(length,frequency)]
    :return: melody - 2D list
    """
    # arrange the instructions:
    # each instruction will be a tuple of (note,duration)
    instructions = list()
    for i in range(0, len(raw_instructions), 2):
        instructions.append((raw_instructions[i], int(raw_instructions[i+1])))

    audio_data = list()
    audio = (Sound.DEFAULT_SAMPLE_RATE, audio_data)

    for note in range(len(instructions)):
        duration = instructions[note][1] * (Sound.DEFAULT_SAMPLE_RATE / 16)
        if instructions[note][0] == "Q":  # Q - quiet
            audio_data.extend([[0, 0]] * int(duration))
        else:
            freq = frequency(instructions[note][0])
            samples_per_cycle = Sound.DEFAULT_SAMPLE_RATE / freq
            for i in range(int(duration)):
                theta = i / samples_per_cycle
                sample_value = \
                    int((Sound.MAX_VOLUME * math.sin(math.pi * 2 * theta)))
                audio_data.append([sample_value] * 2)

    return audio


def user_input(msg, purpose, menu_length=0):
    """
    Returns a valid input by the purpose specified
    :param msg: Prompt for user
    :param purpose:
    'navigate' - choice between range on numbers in a menu
    'manipulate' - wav file name
    'compose' - instruction file name
    'save_file' - output file name
    :param menu_length: Optional. the length of the menu printed to the user.
    Use only if checking for navigation.
    :return: a valid input by user
    'navigate' -  user's choice (integer)
    'manipulate' - audio file (list of (frame_rate, audio_data))
    'compose' - list of instructions (letters and integers combined)
    'save' - filename (string)
    """

    if purpose == Sound.NAVIGATE:
        valid_input = [str(opt) for opt in range(1, menu_length + 1)]
        while True:  # keeps iterates while input is invalid
            choice = input(msg)
            if choice in valid_input:
                return choice
            msg = "Your choice can only be numbers between the menu range. " \
                  "Try again :"

    elif purpose == Sound.MANIPULATE:  # Invoked from manipulation()
        while True:
            audio = wave_helper.load_wave(input(msg))
            if type(audio) == tuple:  # valid input
                return audio
            msg = "Error : Audio file does not exist. Try again : "

    elif purpose == Sound.COMPOSE:  # Invoked from composition():
        while True:
            instructions = input(msg)
            if os.path.isfile(instructions):  # File exists
                inst_file = open(instructions, 'r')
                instructions = [line.strip().split(" ") for line in inst_file]
                instructions = sum(instructions, [])  # flatten the list to 1D
                return instructions
            msg = "Error : Instructions file does not exist. Try again : "

    # Invoked from save_audio()
    return input(msg)


def frequency(note):
    """
    This function will return the corresponding
    frequency of the note's wave.
    :param note: The note (A-G) - Str
    :return: Frequency of the note (int)
    """
    if note == "A":
        return 440
    if note == "B":
        return 494
    if note == "C":
        return 523
    if note == "D":
        return 587
    if note == "E":
        return 659
    if note == "F":
        return 698
    if note == "G":
        return 784


def change_volume(audio, multiplier):
    """
    Multiplies the audio's volume by the multiplier specified.
    :param audio: The audio to edit - 2D list
    :param multiplier: The value to multiply by.
    use Sound.VOLUME_INCREASE or Sound.VOLUME_DECREASE
    :return: The manipulated audio - 2D list
    """
    audio_cpy = copy.deepcopy(audio)

    for i in range(0, len(audio_cpy)):
        for j in range(2):
            changed_value = int(audio_cpy[i][j] * multiplier)
            if changed_value > Sound.MAX_VOLUME:
                audio_cpy[i][j] = Sound.MAX_VOLUME
            elif changed_value < Sound.MIN_VOLUME:
                audio_cpy[i][j] = Sound.MIN_VOLUME
            else:
                audio_cpy[i][j] = changed_value
    return audio_cpy


def speed_change(audio, specifier):
    """
    Multiplies the audio speed by the multiplier specified.
    :param audio: The audio to edit - 2D list
    :param specifier: Sound.SPEED_UP or Sound.SPEED_DOWN
    :return: The manipulated audio - 2D list
    """
    audio_cpy = copy.deepcopy(audio)

    if len(audio_cpy) == 1:
        return audio_cpy

    if specifier == Sound.SPEED_UP:
        return audio_cpy[::2]

    if specifier == Sound.SPEED_DOWN:
        for i in range(len(audio)-1):
            left_avg = (audio[i][0] + audio[i+1][0]) // 2
            right_avg = (audio[i][1] + audio[i+1][1]) // 2
            audio_cpy.insert(2 * i + 1, [left_avg, right_avg])

    return audio_cpy


def reverse_audio(audio):
    """
    Reverses the audio end-to-start
    :param audio: The audio to reverse
    :return: the reversed audio - 2D list
    """
    audio_cpy = copy.deepcopy(audio)
    list.reverse(audio_cpy)
    return audio_cpy


def low_pass_filter(audio):
    """
    Filters the audio by a low-pass filter.
    :param audio: The audio to filter.
    :return: Filtered audio - list[list[]]
    """
    audio_cpy = copy.deepcopy(audio)
    filtered_audio = list()

    # assign first value
    left = (audio_cpy[0][0] + audio_cpy[1][0]) / 2
    right = (audio_cpy[0][1] + audio_cpy[1][1]) / 2
    filtered_audio.append([int(left), int(right)])

    # run from second value to the one before last
    for i in range(1, len(audio_cpy)-1):
        left = (audio_cpy[i-1][0] + audio_cpy[i][0] + audio_cpy[i+1][0]) / 3
        right = (audio_cpy[i-1][1] + audio_cpy[i][1] + audio_cpy[i+1][1]) / 3
        filtered_audio.append([int(left), int(right)])

    # assign last value
    left = (audio_cpy[-1][0] + audio_cpy[-2][0]) / 2
    right = (audio_cpy[-1][1] + audio_cpy[-2][1]) / 2
    filtered_audio.append([int(left), int(right)])

    return filtered_audio


if __name__ == "__main__":
    main_menu()
