import argparse
import zipfile
import os
import glob
import random
import string

parser = argparse.ArgumentParser()
parser.add_argument("--output", help="output")
parser.add_argument("--codido", help="running on codido")
############################################
# TODO: add extra args here
parser.add_argument("--length", type=int, help="length of password")
############################################

args = parser.parse_args()

output_folder_path = os.path.join(os.sep, 'app', 'outputs')
os.makedirs(output_folder_path, exist_ok=True)

############################################
############################################

# get filename and filepath first
pw_length = int(args.length) if args.length else 4


def generate_password(length):
    password_chars = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(string.digits),
        random.choice(string.punctuation)
    ]

    if length > 4:
        password_chars.extend(random.choices(string.ascii_letters + string.digits + string.punctuation, k = length-4))

    random.shuffle(password_chars)
    return ''.join(password_chars)


password = generate_password(pw_length)
print(password)

############################################
# TODO: outputs should be saved to output_folder_path like follows:
with open(os.path.join(output_folder_path, 'out.txt'), 'w') as f:
    f.write(password)
############################################

if args.codido == 'True':
    # create zip with all the saved outputs
    zip_name = output_folder_path + '.zip'
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
        for folder_name, subfolders, filenames in os.walk(output_folder_path):
            for filename in filenames:
                file_path = os.path.join(folder_name, filename)
                zip_ref.write(file_path, arcname=os.path.relpath(file_path, output_folder_path))

    # upload
    import boto3
    s3 = boto3.client('s3')
    s3.upload_file(zip_name, os.environ['S3_BUCKET'], args.output)
