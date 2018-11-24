import music21
from collections import defaultdict

import copy
import subprocess
from pathlib import Path

C_COLLECT_CLASSES=('Metadata',
                   'Clef',
                   'TimeSignature',
                   'Instrument',
                   'KeySignature')

def load_score(music_file_path: Path):
    '''Load a musicxml score file
    Keyword arguments:
    music_file_path -- the path to the file
    '''
    return music21.converter.parse(str(music_file_path))

def generate_window(score, window_size):
    '''Generate a window from the score'''
    # Create a container for all of the window scores
    window_scores = defaultdict(music21.stream.Score)
    part_names = [part.partName for part in score.parts]

    print(score.metadata)
    # Get the number of measures
    num_measures = score.measureOffsetMap().popitem()[-1][-1].measureNumber
    for measure_number in range(0, num_measures-window_size, window_size):
        window_score = (
                score.measures(measure_number, 
                               measure_number + window_size,
                               collect=C_COLLECT_CLASSES))
        window_score.metadata = copy.deepcopy(score.metadata)
        window_score.metadata.title = (
                  window_score.metadata.title 
                + ' (' + ', '.join(part_names) + ')'
                + ': Measures '
                + str(measure_number)
                + '-'
                + str(measure_number + window_size))
        window_scores[(measure_number, measure_number + window_size)] = (
                window_score)

    return window_scores

def extract_parts(score, part_names):
    if part_names:
        return [part for part in score.parts if part.partName in part_names]
    else:
        return score

def save_score(score, filepath, format='musicxml', save_metadata=True):
    metadata = score.metadata
    if not save_metadata:
        score.metadata=None
    saved =  Path(score.write(format, str(filepath)))
    score.metadata = metadata
    return saved

def export(score, filepath, save_metadata=True):
    '''
    metadata = score.metadata
    if not save_metadata:
        score.metadata=None
    '''
    print(score.metadata)
    tmp_filepath = filepath.with_name(
            filepath.stem + '_tmp').with_suffix('.xml')
    score.write('musicxml', str(tmp_filepath))
    #score.metadata = metadata
    print(filepath)
    subprocess.run(['musescore', 
                    '-o', str(filepath),
                    str(tmp_filepath)])
    #tmp_filepath.unlink()
    return filepath
