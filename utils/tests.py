from utils.pdf_utils import upload_file

file_path = '/Volumes/WORK/works/Mathias/webbackend/'
imgs = [
  'dental-care.png',
  'dossier.png',
  'utilisateur.png',
  'verifie.png'
]

bucket_name = 'aligneursfrancais'
aws_s3_path = 'logos/email/'

for img in imgs:
  res = upload_file(file_path + img, bucket_name, aws_s3_path + img)
  print('==== res: ', res)