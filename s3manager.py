from boto3.session import Session
import os
import re

ACCESS_KEY = os.environ['AWS_ACCESS_KEY_ID']
SECRET_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
S3_BUCKET = os.environ['S3_BUCKET_NAME']

session = Session(aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
s3 = session.resource('s3')
bucket = s3.Bucket(S3_BUCKET)

keywords = re.compile(r"KERNELS_TO_LOAD\s*=\s*\((.*)\)", flags=re.DOTALL)
config = dict(kernel=None, kernel_list=[])


def get_meta_kernel(kernel):

    get_kernel(kernel)
    with open(kernel, 'r') as f:
        contents = f.read()

    match = keywords.search(contents)
    if match is not None:

        kernel_list = [s.strip().replace("'", '') for s in match.group(1).split(',')]
        kernels_to_add = [k for k in kernel_list if k not in config['kernel_list']]
        kernels_to_remove = [k for k in config['kernel_list'] if k not in kernel_list]

        if config['kernel'] is not None:
            os.remove(config['kernel'])

        for k in kernels_to_remove:
            os.remove(k)

        for k in kernels_to_add:
            get_kernel(k)

        config['kernel'] = kernel
        config['kernel_list'] = kernel_list


def remove_meta_kernel(kernel):

    with open(kernel, 'r') as f:
        contents = f.read()

    match = keywords.search(contents)
    if match is not None:
        kernel_list = [s.strip().replace("'", '') for s in match.group(1).split(',')]
        for k in kernel_list:
            os.remove(k)

    os.remove(kernel)


def get_kernel(kernel):
    bucket.download_file(kernel, "./" + kernel)
