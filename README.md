# Image EXIF meta data editor

A small script to adjust Image (currently JPG only) EXIF metadata tags from a single folder.
Supports to adjust:
- `0x882a` - TimeZoneOffset
- `0x9003` - DateTimeOriginal

Check more about EXIF Tags here: https://exiftool.org/TagNames/EXIF.html

## How to use:
- Install libraries
    ```
    pipenv install
    ```
    or
    ```
    pip install pillow piexif pyyaml
    ```
- Copy `config.yaml.template` to `config.yaml` file and fill it in according to the instructions. The file should contain:
    ```
    images:
    input_folder: <input folder>
    output_folder: <[Optional] output folder. Will overwrite the photos if not set>

    adjust:
    shift_time:  <[Optional] set how much time to shift. If None, then time will not be shifted>
        hours: 5
        minutes: 0
        seconds: 90
    timezone_offset: 8 # [Optional] The time zone offset of DateTimeOriginal from GMT in hoursIf None, then will not update time zone
    ```
- Run:
    ```
    python main.py
    ```
