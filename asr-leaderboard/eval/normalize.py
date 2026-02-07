# Normalization Utilities

# Function to normalize text
import opencc

def normalize_chinese(text):
    converter = opencc.OpenCC('t2s')  # Traditional to Simplified
    return converter.convert(text)


# Processing function based on input format
def process_input(input_line):
    utt_id, text = input_line.strip().split('\t')
    normalized_text = normalize_chinese(text)
    return utt_id, normalized_text
