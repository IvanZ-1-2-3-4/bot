import pickle
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

creds = pickle.load(open('token.pickle', 'rb'))
service = build('drive', 'v3', credentials=creds)

file_metadata = {'name': '0.png', 'parents': ['1wFmPPHoTbaxcsVZlVq6wCv8Mmmb7x2DS']}
media = MediaFileUpload('images/training_set/0.png', mimetype='image/png')
file = service.files().create(body = file_metadata, media_body = media, fields = 'id').execute()
print('File ID: %s' % file.get('id'))