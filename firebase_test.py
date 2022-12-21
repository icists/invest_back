import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
 
 
#Firebase database 인증 및 앱 초기화
cred = credentials.Certificate('ovl-investement-game-firebase-adminsdk-4cnm0-7981270c80')
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://ovl-investement-game-default-rtdb.asia-southeast1.firebasedatabase.app/'
})
 
dir = db.reference() #기본 위치 지정
dir.update({'test':'Hello World'})