
import os

def create_txt_files():
    # Read file
    with open('git/hillside-hermitage-talks/resources/all_recordings.txt', encoding = 'utf8') as mr:
        lines = mr.readlines()
    all_lines = []
    for i in lines:
        all_lines.append(i.replace('\n', '') + '.txt')
    for i in all_lines:
        with open('git/hillside-hermitage-talks/working/' + i, 'w') as wd:
            wd.write('In process...')
        print('Created: ' + i)

create_txt_files()