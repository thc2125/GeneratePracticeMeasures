import anki_generator
import musescore_interface
import musicxml_interface

import argparse
from pathlib import Path

#C_WINDOW_SIZES = [2, 3, 5, 8]
C_WINDOW_SIZES = [8]

C_EXPORT_FORMATS = ['svg', 'mp3']
C_INPUT_FORMAT = 'xml'
C_INPUT_INTERFACE = {'xml': musicxml_interface}

def main(score_filepath,
         part_names=None,
         window_sizes=C_WINDOW_SIZES,
         export_formats=C_EXPORT_FORMATS):
    generate_practice_measures(score_filepath, window_sizes, part_names)

def generate_practice_measures(score_filepath,
                               window_sizes=C_WINDOW_SIZES,
                               part_names=None,
                               input_interface=C_INPUT_INTERFACE[C_INPUT_FORMAT],
                               export_formats=C_EXPORT_FORMATS,
                               export=musescore_interface.export):
    score = input_interface.load_score(score_filepath)
    parts = input_interface.extract_parts(score, part_names)
    generated_files = []
    for window_size in window_sizes:
        window_scores = input_interface.generate_window(parts, window_size)
        for (measures,
             window_score) in window_scores.items():
            window_score_filepath = (
                    score_filepath.with_name(
                          score_filepath.stem + '-'
                        + ('_'.join(part_names) + '-' if part_names else '') 
                        + ('m' + '_'.join([str(measure) 
                                           for measure in measures])
                          )
                    ).with_suffix('.xml')
            )
            generated_file = {}
            generated_file['score'] = window_score
            generated_file['score_filepath'] = input_interface.save_score(
                    window_score, 
                    window_score_filepath)
            
            '''
            input_interface.save_score(
                    window_score,
                    window_score_filepath.with_suffix(
                        '.' +
                        export_format),
                    export_format)
            generated_file['score_audio_filepath'] = export(window_score_filepath, 'mp3')

            generated_file['score_notation_filepath'] = export(
                    window_score_filepath.with_name(
                        window_score_filepath.stem + '-1'),
                    'svg')
            '''

            generated_file['score_audio_filepath'] = (
                    input_interface.export(
                        window_score,
                        window_score_filepath.with_suffix('.mp3'),
                        #'lily.mp3', 
                        save_metadata=False))

            generated_file['score_audio_filepath'] = (
                    input_interface.save_score(
                        window_score,
                        window_score_filepath.with_name(
                            window_score_filepath.stem),
                        'lily.svg',
                        save_metadata=False))


            '''
            generated_file['score_notation_filepath'] = (
                    input_interface.export(
                        window_score,
                        window_score_filepath.with_name(
                            window_score_filepath.stem +'-1').with_suffix(
                                '.svg'),
                        #'lily.svg',
                        save_metadata=False))
            '''
            generated_files.append(generated_file)

    anki_generator.write_anki_notes(
            score_filepath.with_suffix('.tsv'),generated_files)

    for generated_file in generated_files:
        print(generated_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
            'score_file', 
            type=Path,
            help="The score_file to split into practice measures.")
    args = parser.parse_args()
    main_args = {"score_filepath": args.score_file}
    main(**main_args)
