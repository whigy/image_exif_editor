import os
import json
import logging
import yaml
from PIL import Image
import piexif
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)

def shift_original_time(exif_dict, time_delta):
    # Get the original datetime from the EXIF data
    original_time_str = exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal].decode('utf-8')
    original_time = datetime.strptime(original_time_str, "%Y:%m:%d %H:%M:%S")
    
    # Adjust the datetime by the timezone offset (hours)
    adjusted_time = original_time + time_delta
    adjusted_time_str = adjusted_time.strftime("%Y:%m:%d %H:%M:%S")
    logging.debug(f"{original_time} --> {adjusted_time}")

    # Update the EXIF DateTimeOriginal field
    exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = adjusted_time_str.encode('utf-8')
    return exif_dict


def set_timezone_offset(exif_dict, timezone_offset):
    exif_dict['0th'][piexif.ImageIFD.TimeZoneOffset] = timezone_offset
    return exif_dict


def update_image_meta(image_path, output_path=None, time_delta=None, timezone_offset=None):
    # Load the image and its EXIF data
    img = Image.open(image_path)
    exif_dict = piexif.load(img.info['exif'])

    # Shift original time by 'time_delta'
    if time_delta is not None:
        exif_dict = shift_original_time(exif_dict, time_delta)

    if timezone_offset is not None:
        exif_dict = set_timezone_offset(exif_dict, timezone_offset)

    exif_bytes = piexif.dump(exif_dict)

    new_image_path = output_path if output_path is not None else image_path
    img.save(new_image_path, "jpeg", exif=exif_bytes)
    logging.debug(f"Image saved at: {new_image_path}")


def main():
    config_path = "config.yaml"
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    input_folder = config["images"]["input_folder"]
    logging.info(f"...Input folder `{input_folder}`")

    output_folder = config["images"].get("output_folder")
    if output_folder is None:
        logging.info(f"...Images will be overwritten with new meta data")
    else:
        logging.info(f"...Images will be saved to folder `{output_folder}`")

    time_delta_cfg = config["adjust"].get("shift_time")
    if time_delta_cfg is not None:
        try:
            time_delta = timedelta(**time_delta_cfg)
            logging.info(f"...Time will be shifted by `{time_delta}`")
        except Exception as e:
            logging.error(f"Invalid time to shift. Config: {json.dumps(time_delta_cfg, indent=2)}; \nError: {e}")
            return
    else:
        time_delta = None
        logging.info("...Received no 'shift_time' instruction, will not shift time for the images")

    timezone_offset = config["adjust"].get("timezone_offset")
    if timezone_offset is None:
        logging.info("...Received no 'timezone_offset' instruction, will not set timezone offset for the images")
    else:
        logging.info(f"...Will set all images' timezone to: GMT {timezone_offset}")

    # TODO: Add a break point for confirmation to continue

    for i, filename in enumerate(os.listdir(input_folder)):
        if filename.endswith('.JPG'):
            # Create the full file path
            image_path = os.path.join(input_folder, filename)
            if output_folder is not None:
                output_path = os.path.join(output_folder, filename)
            update_image_meta(image_path, output_path, time_delta, timezone_offset)

    logging.info(f"Done! {i} images modified!")

if __name__ == "__main__":
    main()
