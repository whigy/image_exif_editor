# Image EXIF meta data editor

A small script to adjust Image EXIF metadata tags from a single folder.
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
- Fill in `config.yaml` file