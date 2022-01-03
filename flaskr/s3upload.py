import os
import boto3

conn = boto3.client('s3')

UPLOAD_FOLDER ='/home/ubuntu/Project1/flaskr/media/processed_photos' 
BUCKET_NAME = 'processed-images-tuj57093'

def upload_file(username, filename):
    ''' 
    uploads file to a key in bucket that follows key='<username>/<filename>', 
    '''
    filename = username + '/' + filename
    fullpath = os.path.join(UPLOAD_FOLDER, filename)
    fullkey = username + '/' + filename
    conn.upload_file(fullpath, BUCKET_NAME, fullkey)
   

