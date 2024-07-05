import argparse
import zipfile
import os
import glob

parser = argparse.ArgumentParser()
parser.add_argument("--input", help="input")
parser.add_argument("--output", help="output")
parser.add_argument("--codido", help="running on codido")
############################################
# TODO: add extra args here
############################################

args = parser.parse_args()

input_folder_path = os.path.join(os.sep, 'app', 'inputs')
output_folder_path = os.path.join(os.sep, 'app', 'outputs')
os.makedirs(input_folder_path, exist_ok=True)
os.makedirs(output_folder_path, exist_ok=True)

if args.codido == 'True':
    import boto3
    s3 = boto3.client('s3')

    # downloads codido input file into the folder specified by input_folder_path
    input_file_path = os.path.join(input_folder_path, args.input.split('_SPLIT_')[-1])
    s3.download_file(os.environ['S3_BUCKET'], args.input, input_file_path)
else:
    input_file_path = glob.glob(os.path.join(input_folder_path, '*'))[0]

############################################
# TODO: the input is now accessible via input_file_path
############################################

############################################
# TODO: outputs should be saved to output_folder_path like follows:
with open(os.path.join(output_folder_path, 'TODO.txt'), 'w') as f:
    f.write('Hello World')
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
    s3.upload_file(zip_name, os.environ['S3_BUCKET'], args.output)