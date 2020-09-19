from subprocess import PIPE, STDOUT, run
import sys
import os
import filecmp

TESTER_FILES_DIR = 'tester_files' + os.sep
TESTER_OUT_DIR = 'tester_files_out' + os.sep
TEST_LST = [
    ['2', 'fmmsd,md,msd,msd,msd,msd,m',
     TESTER_FILES_DIR + 'sample3.txt', '1', '7',
     TESTER_OUT_DIR + 'composition_reversed.wav', '3'],
    ['2',
     TESTER_FILES_DIR + 'sample3.txt', '7',
     TESTER_OUT_DIR + 'composition.wav', '3'],
    ['2',
     TESTER_FILES_DIR + 'sample2.txt', '1', '1', '7',
     TESTER_OUT_DIR + 'composition_reversed_twice.wav', '3'],
    ['2',
     TESTER_FILES_DIR + 'sample1.txt', '2', '7',
     TESTER_OUT_DIR + 'composition_speed_up.wav', '3'],
    ['2',
     TESTER_FILES_DIR + 'sample3.txt', '3', '7',
     TESTER_OUT_DIR + 'composition_slow_down.wav', '3'],
    ['2',
     TESTER_FILES_DIR + 'sample2.txt', '4', '7',
     TESTER_OUT_DIR + 'composition_volume_up.wav', '3'],
    ['2',
     TESTER_FILES_DIR + 'sample3.txt', '5', '7',
     TESTER_OUT_DIR + 'composition_volume_down.wav', '3'],
    ['2',
     TESTER_FILES_DIR + 'sample3.txt', '6', '7',
     TESTER_OUT_DIR + 'composition_low_pass_filter.wav', '3'],
    ['1', 'fmmsd,md,msd,msd,msd,msd,m',
     TESTER_FILES_DIR + 'sample3.wav', '1', '7',
     TESTER_OUT_DIR + 'wav_reversed.wav', '3'],
    ['1',
     TESTER_FILES_DIR + 'sample2.wav', '7',
     TESTER_OUT_DIR + 'wav.wav', '3'],
    ['1',
     TESTER_FILES_DIR + 'sample1.wav', '1', '1', '7',
     TESTER_OUT_DIR + 'wav_reversed_twice.wav', '3'],
    ['1',
     TESTER_FILES_DIR + 'sample3.wav', '2', '7',
     TESTER_OUT_DIR + 'wav_speed_up.wav', '3'],
    ['1',
     TESTER_FILES_DIR + 'sample3.wav', '3', '7',
     TESTER_OUT_DIR + 'wav_slow_down.wav', '3'],
    ['1',
     TESTER_FILES_DIR + 'sample2.wav', '4', '7',
     TESTER_OUT_DIR + 'wav_volume_up.wav', '3'],
    ['1',
     TESTER_FILES_DIR + 'sample3.wav', '5', '7',
     TESTER_OUT_DIR + 'wav_volume_down.wav', '3'],
    ['1',
     TESTER_FILES_DIR + 'sample3.wav', '6', '7',
     TESTER_OUT_DIR + 'wav_low_pass_filter.wav', '3'],
    ['1',
     TESTER_FILES_DIR + 'sample3.wav', '6', '1', '5', '4',
     '3', '3', '2', '1', '7',
     TESTER_OUT_DIR + 'weird_flex_but_ok.wav', '3'],
    ['2',
     TESTER_FILES_DIR + 'sample3.txt', '6', '1', '5', '4',
     '3', '3', '2', '1', '7',
     TESTER_OUT_DIR + 'weird_flex_but_ok.wav', '3']
]


def run_program(input_lst):
    input_str = '\n'.join(input_lst) + '\n'
    p = run([sys.executable, "wave_editor.py"],
            input=input_str, stdout=PIPE, stderr=STDOUT, timeout=20,
            encoding='utf-8')


def test_program():
    if not os.path.exists(TESTER_OUT_DIR):
        os.makedirs(TESTER_OUT_DIR)

    for test in TEST_LST:
        run_program(test)
        test_file = test[-2]
        tester_file = TESTER_FILES_DIR + test_file[len(TESTER_OUT_DIR):]
        assert filecmp.cmp(tester_file, test_file,
                           shallow=False), ("Expected: " + tester_file
                                            + "\nWith input:" + str(test))


def test_multiple_actions():
    # bonus

    test_input = (
            ['2',
             TESTER_FILES_DIR + 'sample3.txt', '5', '7',
             TESTER_OUT_DIR + 'composition_volume_down_chained.wav']
            + ['2', 'fmmsd,md,msd,msd,msd,msd,m',
               'fmmsd,md,msd,msd,msd,msd,m',
               TESTER_FILES_DIR + 'sample3.txt', '6', '7',
               TESTER_OUT_DIR + 'composition_low_pass_filter_chained.wav']
            + ['1', 'fmmsd,md,msd,msd,msd,msd,m',
               'fmmsd,md,msd,msd,msd,msd,m',
               TESTER_FILES_DIR + 'sample3.wav', '1', '7',
               TESTER_OUT_DIR + 'wav_reversed_chained.wav', '3']
    )

    run_program(test_input)

    comparison_list = [
        ['composition_volume_down.wav',
         'composition_volume_down_chained.wav'],
        ['composition_low_pass_filter.wav',
         'composition_low_pass_filter_chained.wav'],
        ['wav_reversed.wav',
         'wav_reversed_chained.wav']]

    for test in comparison_list:
        test_file = TESTER_OUT_DIR + test[1]
        tester_file = TESTER_FILES_DIR + test[0]
        assert filecmp.cmp(tester_file, test_file,
                           shallow=False), ("Expected: " + tester_file
                                            + "\nWith input:" + str(test))
