""" 
import pyrebase

class UserController:

    config = {
    "apiKey": "AIzaSyBeI3TmqeOUihbuL9om1bUGA7MjBlHTEzg",
    "authDomain": "ecomp-observatorio.firebaseapp.com",
    "databaseURL": "https://ecomp-observatorio-default-rtdb.firebaseio.com",
    "storageBucket": "ecomp-observatorio.appspot.com",
    "serviceAccount": "controllers/key-admin.json"
    }

    def __init__(self):
        try:
            firebase = pyrebase.initialize_app(config=self.config)
            self.auth = firebase.auth()
        except Exception as e:
            raise Exception(f"Error initializing Firebase: {e}")

    def login(self, username:str, password:str):
        try:
            user = self.auth.sign_in_with_email_and_password(username, password)
            return {"Sucesso!": f"idToken={user['idToken']}"}
        except Exception as e:
            return {"msg": f"E-mail ou senha inválidos!\n{e}"}
 """
import pyrebase
from fastapi import HTTPException
from passlib.context import CryptContext
import firebase_admin
from firebase_admin import credentials, firestore, auth as admin_auth

# Import Firebase initialization from key_admin.py
from controllers.keyAdmin import initialize_firebase

class UserController:
    # Firebase configuration for Pyrebase
    config = {
        "apiKey": "AIzaSyBeI3TmqeOUihbuL9om1bUGA7MjBlHTEzg",
        "authDomain": "ecomp-observatorio.firebaseapp.com",
        "databaseURL": "https://ecomp-observatorio-default-rtdb.firebaseio.com",
        "storageBucket": "ecomp-observatorio.appspot.com",
    }

    def __init__(self):
        try:
            # Initialize Pyrebase for user authentication
            firebase = pyrebase.initialize_app(config=self.config)
            self.auth = firebase.auth()

            # Initialize Firebase Admin SDK (called once)
            initialize_firebase()

            # Initialize Firestore database client
            self.db = firestore.client()

            # Password hashing
            self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        except Exception as e:
            raise Exception(f"Erro inicializando Firebase: {e}")


    def register(self, username: str, email: str, password: str, is_admin: bool = False):
        try:
            # Register user with Firebase Authentication
            user = self.auth.create_user_with_email_and_password(email, password)

            # Store additional user info like username in Firestore
            self.db.collection('users').document(user['localId']).set({
                'username': username,
                'email': email,
                'is_admin': is_admin
            })

            # Assign custom claims for user roles (admin vs. regular user)
            admin_auth.set_custom_user_claims(user['localId'], {"admin": is_admin})

            user_id = user['localId']
            user_ref = self.db.collection('users').document(user_id)
            user_data = user_ref.get().to_dict()

            return {"msg": "Usuário registrado com sucesso", "user_id": user_ref.id, email: user_data['email'], "is_admin": user_data['is_admin'], "username": user_data['username']}
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Erro no registro: {e}")

    def login(self, email: str, password: str):
        try:
            user = self.auth.sign_in_with_email_and_password(email, password)

            # Get the user's token to check for custom claims (e.g., admin)
            decoded_token = admin_auth.verify_id_token(user['idToken'])
            is_admin = decoded_token.get('admin', False)

            user_ref = self.db.collection('users').document(user['localId'])
            user_data = user_ref.get().to_dict()

            return {"msg": "Logado com sucesso", "idToken": user['idToken'], "is_admin": user_data['is_admin'], "userId": user['localId'], "username": user_data['username'], "email": email}
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Email ou senha inválidos: {e}")

    def forgot_password(self, email: str):
        try:
            self.auth.send_password_reset_email(email)
            return {"msg": "Email de recuperação de senha enviado"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Erro ao enviar email: {e}")

    def get_user_info(self, user_id: str):
        try:
            user_record = admin_auth.get_user(user_id)
            # Get username from Firestore
            user_ref = self.db.collection('users').document(user_id)
            user_data = user_ref.get().to_dict()

            if not user_data:
                raise HTTPException(status_code=404, detail="Dados do usuário não encontrados")

            return {
                "user_id": user_record.uid,
                "email": user_record.email,
                "username": user_data.get('username'),  # Get username from Firestore
                "is_admin": user_data.get('is_admin'),
                "creation_timestamp": user_record.user_metadata.creation_timestamp,
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error retrieving user info: {e}")

    def list_users(self):
        try:
            users = []
            page = admin_auth.list_users()
            for user_record in page.users:
                # Get username and is_admin from Firestore
                user_ref = self.db.collection('users').document(user_record.uid)
                user_data = user_ref.get().to_dict()

                if not user_data:
                    # You can choose to handle this case differently
                    continue  # Skip users without data in Firestore

                users.append({
                    "user_id": user_record.uid,
                    "email": user_record.email,
                    "username": user_data.get('username', 'N/A'),  # Get username or default to 'N/A'
                    "is_admin": user_data.get('is_admin', False),  # Get is_admin or default to False
                    "creation_timestamp": user_record.user_metadata.creation_timestamp,
                })
            total_users = len(users)
            return {"total de usuários": total_users, "usuários": users}
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Erro ao listar usuários: {e}")
        
    def update_user(self, user_id: str, username: str = None, is_admin: bool = None):
        try:
            # Prepare data to update
            """ update_data = {}

            if email:
                update_data['email'] = email
            if password:
                update_data['password'] = password

            # Update Firebase Authentication user if email or password is provided
            if update_data:
                admin_auth.update_user(
                    user_id,
                    email=update_data.get('email'),
                    password=update_data.get('password')
                ) """

            # Update Firestore with additional user info
            firestore_update_data = {}
            if username:
                firestore_update_data['username'] = username
            if is_admin is not None:
                firestore_update_data['is_admin'] = is_admin

            if firestore_update_data:
                user_ref = self.db.collection('users').document(user_id)
                user_ref.update(firestore_update_data)
            user_data = user_ref.get().to_dict()

            return {"msg": "Usuário atualizado com sucesso", "username": user_data['username'], "email": user_data['email'], "userId": user_id, "is_admin": user_data['is_admin']}
        
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Erro ao atualizar usuário: {e}")
        
    def delete_user(self, user_id: str):
        try:
            user_ref = self.db.collection('users').document(user_id)
            user_data = user_ref.get().to_dict()
            # Delete the user by their user_id (uid)
            self.db.collection('users').document(user_id).delete()

            return {"msg": "Usuário deletado com sucesso", "username": user_data['username'], "email": user_data['email'], "is_admin": user_data['is_admin'], "userId": user_id, }
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Erro ao deletar usuário: {e}")

    def set_admin_claim(self, email: str):
        try:
            # Find the user by email
            user = admin_auth.get_user_by_email(email)
            user_id = user.uid

            # Set the custom claim 'admin' to True
            admin_auth.set_custom_user_claims(user_id, {'admin': True})

            # Update the 'is_admin' field in Firestore for consistency
            user_ref = self.db.collection('users').document(user_id)
            user_ref.update({'is_admin': True})

            return {"msg": f"Permissão de administrador concedida com sucesso para o usuário {email}"}
        except admin_auth.UserNotFoundError:
            raise HTTPException(status_code=404, detail=f"Usuário com email {email} não encontrado.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ocorreu um erro: {e}")
