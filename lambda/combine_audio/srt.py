import re

def modify_srt_file(srt_file_path, seconds_to_add):
    with open(srt_file_path, 'r', encoding='utf-8') as file:
        srt_content = file.read()

    # Define a regular expression pattern to match time stamps in the format HH:MM:SS,SSS
    time_pattern = re.compile(r'(\d{2}:\d{2}:\d{2},\d{3})')

    # Function to add seconds to a time stamp and format it back to HH:MM:SS,SSS
    def add_seconds(match):
        timestamp = match.group(1)
        hours, minutes, seconds_milliseconds = timestamp.split(':')
        seconds, milliseconds = seconds_milliseconds.split(',')
        
        total_seconds = int(hours) * 3600 + int(minutes) * 60 + int(seconds) + seconds_to_add
        new_timestamp = "{:02d}:{:02d}:{:02d},{:03d}".format(
            total_seconds // 3600,
            (total_seconds % 3600) // 60,
            total_seconds % 60,
            int(milliseconds)
        )
        return new_timestamp

    # Use the regular expression to find and replace time stamps in the content
    modified_srt_content = time_pattern.sub(add_seconds, srt_content)

    # Write the modified content back to the file
    with open(srt_file_path, 'w', encoding='utf-8') as file:
        file.write(modified_srt_content)

# Example usage:
srt_file_path = 'caption-2.srt'
seconds_to_add = 10
modify_srt_file(srt_file_path, seconds_to_add)
