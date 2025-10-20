import random
import time
import datetime
import pygame
import os
import pandas as pd

from mutagen.mp3 import MP3

datapath = 'data'
journalpath = 'journal'
soundmodelspath = 'soundmodels'

trunks = [0,1,2,3,4,5,6,7,8,9]

def get_mp3_duration(filepath):
    audio = MP3(filepath)
    return audio.info.length

def get_sound_durations(sound_model):
    sound_durations = {}

    for i, trunk in enumerate(trunks):
        filepath = os.path.join(soundmodelspath, sound_model, "{}.mp3".format(trunk))
        sound_duration = get_mp3_duration(filepath)
        sound_durations[i] = sound_duration

    return sound_durations

# Set working directory
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Create directories, if missing
if not os.path.exists(datapath):
    os.makedirs(datapath)
if not os.path.exists(journalpath):
    os.makedirs(journalpath)

def is_valid(seq):
    if len(seq) < 3:
        return True
    a, b, c = seq[-3], seq[-2], seq[-1]
    # Check for three same digits
    if a == b == c:
        return False
    # Check for increasing sequence
    if a + 1 == b and b + 1 == c:
        return False
    # Check for decreasing sequence
    if a - 1 == b and b - 1 == c:
        return False
    return True

def generate_numbers_list(n):
    allowed_digits = range(10)
    numbers_list = []
    i = 0
    while i < n:
        candidates = list(allowed_digits)
        random.shuffle(candidates)
        
        approved = False
        for candidate_digit in candidates:
            # enforce restrictions to allowed digit sequences
            if is_valid(numbers_list + [candidate_digit]):
                numbers_list.append(candidate_digit)
                i += 1
                approved = True
                break
        
        if not approved:
            if not numbers_list:
                raise ValueError("Cannot generate valid numbers_list from scratch.")
            numbers_list.pop()
            i -= 1
    return numbers_list


def play_audio(number, sound_model):
    pygame.mixer.init()
    path = os.path.join(soundmodelspath, str(sound_model), "{}.mp3".format(number))
    pygame.mixer.music.load(path)    
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

if __name__ == "__main__":


    # Predefine variables
    os.system('cls||clear')
    status = True
    mistakes_in_a_row = 0
    loop_nr = 0

    # Start the game
    print('Welcome to digit span!')
    print()

    # Ask for user's name
    name = input('Please enter your name ---> ')
    os.system('cls||clear')

    current_date = datetime.date.today().isoformat()

    mode_int_to_word = {"1": "BENCHMARK",
                        "2": "PRACTICE",
                        "3": "TEST"}

    while True:
        print('Palun vali sisu - Please choose mode:')
        print()
        print('1. Baastest - Benchmark')
        print('2. Harjutamine - Practice')
        print('3. Jätkutest - Test')
        print()
        print('* sisesta number - enter a number *')
        mode_input = input('---> ')
        if mode_input in mode_int_to_word.keys():
            break
        else:
            print("Palun kasuta lubatud valikuid - Please enter a valid option.")
            os.system('cls||clear')
    os.system('cls||clear')

    # how comfortable is the environment, 1 - not comfortable, 10 - very comfortable
    while True:
        print('NOT COMFORTABLE  1--2--3--4--5--6--7--8--9--10    VERY COMFORTABLE')
        print()
        print('* enter a number *')
        location = input('How comfortable is the environment right now? ---> ')
        if location in {'1', '2', '3', '4', '5', '6', '7', '8', '9', '10'}:
            break
        else:
            print("Please enter a valid option.")
            os.system('cls||clear')
    os.system('cls||clear')

    # tiredness level, 1 - not tired, 10 - tired
    while True:
        print('NOT TIRED  1--2--3--4--5--6--7--8--9--10    VERY TIRED')
        print()
        print('* enter a number *')
        tiredness = input('How tired are you right now? ---> ')
        if tiredness in {'1', '2', '3', '4', '5', '6', '7', '8', '9', '10'}:
            break
        else:
            print("Please enter a valid option.")
            os.system('cls||clear')
    os.system('cls||clear')

    # mental state, 1 - not focused, 10- focused
    while True:
        print('NOT FOCUSED  1--2--3--4--5--6--7--8--9--10    VERY FOCUSED')
        print()
        print('* enter a number *')
        mental_state = input('How focused are you right now? ---> ')
        if mental_state in {'1', '2', '3', '4', '5', '6', '7', '8', '9', '10'}:
            break
        else:
            print("Please enter a valid option.")
            os.system('cls||clear')
    os.system('cls||clear')

    # motivation level, 1 - not motivated, 10 - very motivated
    while True:
        print('NOT MOTIVATED  1--2--3--4--5--6--7--8--9--10    VERY MOTIVATED')
        print()
        print('* enter a number *')
        motivation = input('How motivated are you right now? ---> ')
        if motivation in {'1', '2', '3', '4', '5', '6', '7', '8', '9', '10'}:
            break
        else:
            print("Please enter a valid option.")
            os.system('cls||clear')
    os.system('cls||clear')

    # Initialize starting sequence length
    if mode_int_to_word[mode_input] == 'BENCHMARK':
        n = 3
    else:
        while True:
            print('Please enter starting point for digit span test.')
            print()
            print('Press ENTER for default 3 digits')
            n_input = input('...or enter a custom starting point for digit span test ---> ')
            if n_input.isdigit():
                n = int(n_input)
                break
            elif n_input == '':
                n = 3
                break
            else:
                print("Please enter a valid number.")
            os.system('cls||clear')
    os.system('cls||clear')    

    # Ask for sound model and ensure it is a valid option
    while True:
        print('Palun vali häälemudel - Please enter sound model number:')
        print()
        print('1. Kaarel (Estonian)')
        print('2. Pille (Estonian)')
        print('3. Bot (English)')
        print()
        print('* enter a number *')
        sound_model = input(' ---> ')
        if sound_model in {'1', '2', '3'}:
            sound_durations = get_sound_durations(sound_model)
            break
        else:
            print("Please enter a valid option.")
            os.system('cls||clear')
    os.system('cls||clear')

    # ask for wait time between numbers'
    wait_time = 1
    if mode_int_to_word[mode_input] == 'PRACTICE':
        wait_time = float(input('Please enter wait time between numbers in seconds ---> '))
    elif mode_int_to_word[mode_input] in ['TEST', 'BENCHMARK']:
        # world memory championships start saying a new digit at each new second.
        wait_time = 1
    os.system('cls||clear')

    # Ask about the method that was practiced or used for memorization.
    print('Please choose memory method that you used or practiced today.')
    print()
    print('Examples: 4, 7, 10 or 6')
    print()
    print('1. Repeating the audio')
    print('2. Visualizing the digits')
    print('3. Rhyming words with numbers to visualize images')
    print('4. Translating number shape to images')
    print('5. Phonetic number system to create images (1 digit at a time)')
    print('6. Phonetic number system to create images (2 digits at a time)')
    print('7. Method of Loci')
    print('8. Using absurd connections')
    print('9. Number chunking')
    print('10. Using personal connections')
    print('11. No method')
    print()
    print('* enter a number *')
    memory_method = input(' ---> ')

    os.system('cls||clear')

    # Display game rules
    print('Rules:')
    print()
    print('1. You will hear a series of numbers')
    print('2. After hearing the full sequence of numbers, recall the full sequence in the same order')
    print('3. If you repeat the numbers correctly, the series will get longer by one digit')
    print('4. If you make a mistake the first time, the digit length will stay the same. Additional mistakes will shorten the series by one digit')
    print()
    print('________________________')
    print('Press ENTER to start')
    input()
    os.system('cls||clear')

    # Check if log file exists
    if os.path.isfile(os.path.join(datapath, '{}_digit_span_log.csv'.format(name))):
        df = pd.read_csv(os.path.join(datapath,'{}_digit_span_log.csv'.format(name)))
        session_nr = df['session_nr'].iloc[-1] + 1
    else:
        df = pd.DataFrame(columns=['user_name', 'date', 'time', 'session_nr', 'loop_nr', 'presented_sequence', 'recalled_sequence', 'outcome', 'mistakes_in_a_row',
                                'recall_time_in_s', 'sound_model', 'digit_length', 'session_time', 'time_between_digits', 'memory_method', 'tiredness',
                                'physical_activity', 'mental_state', 'motivation', 'location', 'session_mode', 'feedback'])
        session_nr = 1
        
    # start whole game timer
    total_time_start = time.time()

    # Benchmark test params
    benchmark_test_loop_nr = 0

    # Game loop
    while status:
        loop_nr += 1
        current_loop_n = n
        benchmark_test_loop_nr += 1
        
        # Generate list of numbers
        numbers_list = generate_numbers_list(n)
        presented_sequence = ''.join(str(number) for number in numbers_list)
        
        # Play audio for all numbers in the list
        for number in numbers_list:
            os.system('cls||clear')
            play_audio(number, sound_model)
            sound_duration = sound_durations[number]
            adjusted_wait_time = max(0, wait_time - sound_duration)
            time.sleep(adjusted_wait_time)

        # os.system('cls||clear')

        # Measure time
        loop_input_start_time = time.time()
        
        # Ask user to repeat numbers
        print('Current number length is ' + str(current_loop_n) + ' numbers.')
        print()
        print('Please repeat the numbers in one line')
        print()
        recalled_sequence = str(input(' ---> '))
        recalled_sequence_digits_only = ''.join([ch for ch in recalled_sequence if ch.isdigit()])
        os.system('cls||clear')
        

        # Stop time measurement
        loop_input_end_time = time.time()
        time_taken_loop_input = loop_input_end_time - loop_input_start_time

        # Check if user repeated numbers correctly
        if recalled_sequence_digits_only == presented_sequence:
            outcome = 'correct'
            print('Correct!')
            n += 1
            mistakes_in_a_row = 0
        else:
            outcome = 'incorrect'
            print('Incorrect!')
            mistakes_in_a_row += 1
            if mistakes_in_a_row > 1:
                n -= 1
                n = max(1, n)
                mistakes_in_a_row = 0
                

        # calculate total session time in hours, minutes and seconds
        session_time = time.strftime("%H:%M:%S", time.gmtime(time.time() - total_time_start))
        
        # ask for a journal entry
        if mode_int_to_word[mode_input] != 'BENCHMARK':
            print('Press ENTER to continue or write a comment about memorizing the previous sequence!')
            print()
            trial_comment = input(' ---> ')
            os.system('cls||clear')
        else:
            trial_comment = ''
        
        # Compose data
        data = {'user_name': name, 'date': current_date, 'time': time.strftime("%H:%M:%S"), 'session_nr': session_nr, 'loop_nr': loop_nr, 'presented_sequence': presented_sequence,
                'recalled_sequence': recalled_sequence, 'outcome': outcome, 'mistakes_in_a_row': mistakes_in_a_row, 'recall_time_in_s': time_taken_loop_input, 'sound_model': sound_model,
                'digit_length': current_loop_n, 'session_time': session_time, 'time_between_digits': wait_time, 'memory_method': memory_method, 'tiredness': tiredness,
                'mental_state': mental_state, 'location': location, 'motivation': motivation, 'session_mode': mode_int_to_word[mode_input], 'trial_comment': trial_comment}

        # Add data to dataframe
        df = pd.concat([df, pd.DataFrame(data, index=[0])], ignore_index=True)
        
        # print elapsed time in hours, miutes and seconds
        print('__________________________')
        print(outcome + '!')
        print()
        print('Total time elapsed from start: ' + time.strftime("%H:%M:%S", time.gmtime(time.time() - total_time_start)))
        # print current loop number and length of series
        print()
        print('This was trial number ' + str(loop_nr))
        print('Next digit length: ' + str(n))
        print('__________________________')

        # Clear screen and wait for user input
        
        if mode_int_to_word[mode_input] == 'BENCHMARK':
            if benchmark_test_loop_nr == 14:
                os.system('cls||clear')
                df.to_csv(os.path.join(datapath, '{}_digit_span_log.csv'.format(name)), index=False)
                print('You have reached the end of benchmark test.')
                print()
                print('Press ENTER to continue')
                input()
                os.system('cls||clear')
                status = False
            else:
                print('Press ENTER to continue')
                input()
                os.system('cls||clear')

        # if not benchmark mode
        else:
            print('Press ENTER to continue')
            print()
            print('...or type "quit" to quit and save your results to a csv file')
            user_input = input(' ---> ')
            os.system('cls||clear')
            if user_input.lower() == 'quit':
                df.to_csv(os.path.join(datapath, '{}_digit_span_log.csv'.format(name)), index=False)
                print('''OPTIONAL.
                    Please summarize your experience in this testing session (across trials)!''')
                print()
                print('(press ENTER to skip)')
                print()
                journal_entry = input(' ---> ')
                # save journal_entry as a text file with session number, user name and date and time as object
                if journal_entry != '':
                    #generate datetime parameter yyyymmdd_hhmmss
                    journal_entry_datetime = time.strftime("%Y%m%d_%H%M%S")
                    filepath = os.path.join(journalpath, '{}_journal_{}.txt'.format(name, journal_entry_datetime)) 
                    with open(filepath, 'w') as f:
                        f.write(journal_entry)
                status = False
                print('Thank you for playing!')
                time_elapsed = time.strftime("%H:%M:%S", time.gmtime(time.time() - total_time_start))
                print('Total time elapsed: ' + time_elapsed)
