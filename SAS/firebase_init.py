import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("C:\Users\Eastpoint Computer\Desktop\FYP_B_end-main\FYP_B_end-main\config\serviceAccountKey.json")
firebase_admin.initialize_app(cred)
