import csv

C_FIELDNAMES = ['prompt','citation','audio','notation','tags']
C_DELIMITER = '\t'

def write_anki_notes(csv_filepath,
                     generated_files,
                     fieldnames=C_FIELDNAMES,
                     delimiter=C_DELIMITER):
    with open(csv_filepath, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=C_FIELDNAMES, delimiter='\t')
        #writer.writeheader()
        for generated_file in generated_files:
            writer.writerow(create_anki_note(**generated_file))

    return csv_filepath

def create_anki_note(score, 
                     score_filepath, 
                     title = None,
                     score_audio_filepath = None,
                     score_notation_filepath = None):
    return {C_FIELDNAMES[0]: title if title else score.metadata.title,
            C_FIELDNAMES[1]: '',
            C_FIELDNAMES[2]: (
                create_audio_field(score_audio_filepath.name)
                if score_audio_filepath 
                else create_audio_field(
                    score_filepath.with_suffix('mp3').name)),
            C_FIELDNAMES[3]: (
                create_image_field(score_notation_filepath.name)
                if score_notation_filepath 
                else create_image_field(
                    score_filepath.with_suffix('.svg').name)),
            C_FIELDNAMES[4]: ''}

def create_audio_field(filepath):
    return '[sound: ' +  str(filepath) + ']'

def create_image_field(filepath):
    return '<img src="' + str(filepath) + '" />'
