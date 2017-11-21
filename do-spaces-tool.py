#!/usr/bin/env python3
import argparse
import os.path
import boto3.session
from botocore.client import Config


REGION = os.environ.get('region', 'ams3')
ACCESS_KEY_ID = os.environ['ACCESS_KEY_ID']
SECRET_ACCESS_KEY = os.environ['SECRET_ACCESS_KEY']


def cmd_upload(args):
    file_path = os.path.abspath(args.file)
    bucket, key = args.location.split('/', 1)
    assert bucket
    assert key

    session = boto3.session.Session()
    client = session.client(
        's3', region_name=REGION,
        endpoint_url='https://{}.digitaloceanspaces.com'.format(REGION),
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=SECRET_ACCESS_KEY,
    )
    resp = client.list_buckets()
    if bucket not in [x['Name'] for x in resp['Buckets']]:
        print('Creating bucket \'{}\''.format(bucket))
        client.create_bucket(Bucket=bucket)

    print('Uploading file {}...'.format(file_path))
    client.upload_file(file_path, bucket, key, ExtraArgs={
        'ServerSideEncryption': 'AES256',
    })


def cmd_download(args):
    bucket, key = args.location.split('/', 1)

    session = boto3.session.Session()
    client = session.client(
        's3', region_name=REGION,
        endpoint_url='https://{}.digitaloceanspaces.com'.format(REGION),
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=SECRET_ACCESS_KEY,
    )
    print('Downloading file {}...'.format(args.destination))
    client.download_file(bucket, key, args.destination)


cl_parser = argparse.ArgumentParser()
sub_cl_parsers = cl_parser.add_subparsers()

upload_cl_parser = sub_cl_parsers.add_parser('upload')
upload_cl_parser.add_argument('file')
upload_cl_parser.add_argument('location')
upload_cl_parser.set_defaults(func=cmd_upload)

download_cl_parser = sub_cl_parsers.add_parser('download')
download_cl_parser.add_argument('location')
download_cl_parser.add_argument('destination')
download_cl_parser.set_defaults(func=cmd_download)

args = cl_parser.parse_args()
args.func(args)
