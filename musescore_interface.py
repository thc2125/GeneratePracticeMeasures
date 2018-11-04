import xmltodict

import copy
import logging

from collections import defaultdict
from pathlib import Path
from typing import List
from zipfile import ZipFile


C_MUSESCORE_SUFFIX = '.mscx'

C_MUSESCORE_FORCELISTS = ['Part', 
                          'Staff', 
                          'linkedTo', 
                          'Measure', 
                          'Chord', 
                          'Note', 
                          'Rest']

def load_score(music_file_path: Path, 
               compressed: bool= True,
               musescore_suffix: str = C_MUSESCORE_SUFFIX,
               force_list=C_MUSESCORE_FORCELISTS):
    ''' Load a muse score file and return as a 
    python dict
    Keyword arguments:
    music_file_path -- the path to the file
    compressed      -- whether the file is compressed
    '''
    
    music_xml = ''
    if compressed:
        with ZipFile(music_file_path) as music_file_zip:
            musescore_filename = music_file_path.with_suffix(
                    musescore_suffix).name
            with music_file_zip.open(musescore_filename) as musescore_file:
                music_xml = musescore_file.read()
    else:
        with open(music_file_path) as music_file:
            music_xml = music_file.read()

    return xmltodict.parse(music_xml, force_list=force_list)

def write_score(score, score_write_filepath: Path, compressed: bool = False):
    '''Write a score to a filepath. Note that 

    Keyword arguments:
    score                -- a json object representing a musescore score
    score_write_filepath -- the filepath to which to write the score
    '''
    score_xml = xmltodict.unparse(score)
    if not compressed:
        with open(score_write_filepath.with_suffix(C_MUSESCORE_SUFFIX),
                  'w') as score_write_file:
            score_write_file.write(score_xml)

def generate_window(score, window_size, parts=None):
    if parts:
        new_score = extract_parts(score, parts)
    else:
        new_score = copy.deepcopy(score)

    staffs = new_score['museScore']['Score']['Staff']

    # Get the length of the longest staff
    num_measures = max([len(staff['Measure']) for staff in staffs])
    window_scores = {}
    for start_index in range(0, num_measures, window_size):
        end_index = start_index + window_size
        window_score = copy.deepcopy(new_score)
        window_staffs = window_score['museScore']['Score']['Staff']
        for staff, window_staff in zip(staffs, window_staffs):
            if len(staff['Measure']) >= end_index:
                window_staff['Measure'] = staff['Measure'][start_index:end_index]
        window_scores[(start_index, end_index)] = window_score
    return window_scores

def extract_parts(score, part_names: List[str]):
    '''Return a new score from the given score with only the specified part 
    names and associated staffs included.

    Keyword arguments:
    score -- a JSON dict representing a musescore score
    part_names -- a list of part
    '''
    new_score = copy_score_template(score)

    parts = score['museScore']['Score']['Part']
    new_parts = new_score['museScore']['Score']['Part']

    staff_ids = {}
    new_staff_counter = 1
    for part in parts:
        logging.info(part['trackName'])
        if part['trackName'] in part_names:
            new_parts.append(copy.deepcopy(part))
            logging.info("new part: " + str(new_parts[-1]))
            for staff_idx, staff in enumerate(part['Staff']):
                logging.info("staff id: " + str(staff['@id']))
                staff_ids[staff['@id']] = new_staff_counter
                new_staff_counter += 1


    # Remap staff ids and linked staffs
    for part in new_parts:
        for staff in part['Staff']:
            staff['@id'] = staff_ids[staff['@id']]
            for linked_idx, linked in enumerate(staff['linkedTo']):
               staff['linkedTo'][linked_idx] = staff_ids[linked]

    staffs = score['museScore']['Score']['Staff']
    new_staffs = new_score['museScore']['Score']['Staff']

    for staff in staffs:
        if staff["@id"] in staff_ids:
            new_staffs.append(copy.deepcopy(staff))
            new_staffs[-1]['@id'] = staff_ids[new_staffs[-1]['@id']]

    return new_score

def copy_score_template(score):
    '''Copy the score without parts or staffs
    Keyword arguments:
    score -- a json object representing the score
    '''
    new_score = copy.deepcopy(score)
    new_score['museScore']['Score']['Part'].clear()
    new_score['museScore']['Score']['Staff'].clear()

    return new_score

def copy_score(score):
    '''Copy the score 
    Keyword arguments:
    score -- a json object representing the score
    '''
    new_score = copy.deepcopy(score)
    return new_score
