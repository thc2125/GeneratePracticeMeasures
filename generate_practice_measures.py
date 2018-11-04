import argparse
import musescore_interface

from pathlib import Path

C_WINDOW_SIZES = [2, 3, 5, 8]
C_EXPORT_FORMATS = ['svg', 'mp3']

def main(musescore_filepath, parts, window_sizes=C_WINDOWS, export_formats=C_EXPORT_FORMATS):
    generate_windows(musescore_filepath, window_sizes, parts, export_formats)

def generate_windows(musescore_filepath,
                     window_sizes=C_WINDOWS,
                     parts=None,
                     export_formats=C_EXPORT_FORMATS):
    score = musescore_interface.load_score(musescore_filepath)
    generated_scores = []
    for window_size in window_sizes
        window_scores = musescore_interface.generate_window(
                score,
                window_size)
        for (measures,
             window_score) in window_scores.items():
            window_score_filepath = musescore_filepath.with_name(
                musescore_filepath.stem + '-' + '_'.join(measures))
            musescore_interface.write_score(
                    window_score,
                    window_score_filepath)
            for export_format in export_formats:
                musescore_interface.export(window_score_file, export_format)
            generated_files.append(window_score_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
            'musescore_file', 
            type=Path,
            help="The musescore_file to split into practice measures.")
    args = parser.parse_args()
    main_args = {"musescore_filepath": musescore_file}
    main(**main_args)
