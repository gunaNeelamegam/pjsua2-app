from appwrite.id import ID
from appwrite.services.users import Users
from appwrite.client import Client
from appwrite.services.storage import Storage
from appwrite.services.functions import Functions
from appwrite.services.databases import Databases
from appwrite.services.storage import Storage
from appwrite.services.functions import Functions
from appwrite.services.account import Account
from appwrite.exception import AppwriteException
from typing import Any, Union


class AppwriteUtility:
    """
    Needs to go into .env file
    """

    API_KEY = "e757628dc7db8a156c9debdc516f15e200888358f2024ca3d7bda324f3a5d58a1c5a65b94647775cc3c340b48d2855135a776a44c617123e4b486359376aa399faba1ff0dc1f221f562c88098d612e9eb31b844f8df25177aa6e2b330dd46f448d3d631146064dbe2d4e822b5a0237fdfd79eb2745321d41e640b85dc1f0acfe"
    DATA_BASE = "646728422216731449db"
    MSG_COLLECTION = "646728b1674904949d2e"
    PROJECT_ID = "6467258dd958cabe5afc"
    APPWRITE_ENDPOINT = "https://cloud.appwrite.io/v1"

    def __init__(self, endpoint=None, project_id=None):
        self.client = Client()
        self.client.set_endpoint(self.APPWRITE_ENDPOINT)
        self.client.set_project(self.PROJECT_ID)
        self.client.set_key(self.API_KEY)
        self.account: Account = Account(self.client)
        self.users = Users(self.client)
        self.database = Databases(self.client)
        self.storage = Storage(self.client)
        self.functions = Functions(self.client)

    def register(
        self, email: str, password: str, phone_number: int = None, name: str = None
    ):
        try:
            if email and phone_number:
                response = self.users.create(
                    ID.unique(),
                    email,
                    phone=phone_number
                    if phone_number and "+" in phone_number
                    else None,
                    password=password,
                    name=name if name else None,
                )
                return response
            else:
                raise AppwriteException(
                    message="Please Provide User Name and Password !"
                )
        except AppwriteException as e:
            print("Failed to register user:", str(e.message))
            return None

    def login(self, email, password):
        try:
            if email and password:
                response = self.users.createEmailSession(email, password)
                return response
            else:
                raise AppwriteException(message="Please Provide Email and Password !")

        except AppwriteException as e:
            print("Failed to login user:", str(e))
            return None

    def logout(self, session_id):
        try:
            if session_id:
                response = self.users.delete_session(session_id)
                return response
            else:
                raise AppwriteException("Please provide Session id for logout !")
        except AppwriteException as e:
            print("Failed to logout user:", str(e))
            return None

    def get_current_user(self):
        try:
            response = self.account.get()
            return response
        except AppwriteException as e:
            print("Failed to get current user:", str(e))
            return None

    def create_document(self, collection_id, data):
        try:
            result = self.database.create_document(collection_id, data)
            return result["$id"] if "$id" in result else None
        except AppwriteException as e:
            print("Failed to create Document :: ", e.message)
            return None

    def get_document(self, collection_id, document_id):
        try:
            result = self.database.get_document(collection_id, document_id)
            return result
        except AppwriteException as e:
            print("Failed to Get Document :: ", e.message)
            return None

    def update_document(self, collection_id, document_id, data):
        try:
            result = self.database.update_document(collection_id, document_id, data)
            return result
        except AppwriteException as e:
            print("Failed to Update Document :: ", e.message)
            return None

    def delete_document(self, collection_id, document_id):
        try:
            result = self.database.delete_document(collection_id, document_id)
            return result
        except AppwriteException as e:
            print("Failed to Delete Document :", e.args)
            return None

    def upload_file(self, file_path, file_name):
        try:
            result = self.storage.create_file(open(file_path, "rb"), ["*"], file_name)
            return result["$id"] if "$id" in result else None
        except AppwriteException as e:
            print("Failed to Upload File :: ", e.message)
            return None

    def get_file(self, file_id):
        try:
            result = self.storage.get_file(file_id)
            return result
        except AppwriteException as e:
            print("Failed to get File :: ", e.message)
            return None

    def delete_file(self, file_id) -> Union[Any, None]:
        try:
            result = self.storage.delete_file(file_id)
            return result
        except AppwriteException as e:
            print("Failed to Delete File :: ", e.message)
            return None

    def call_function(self, function_id, data):
        result = self.functions.create_execution(function_id, data)
        execution_id = result["$id"] if "$id" in result else None

        if execution_id:
            execution_result = self.functions.get_execution(execution_id)
            return {
                "action": "call_function",
                "execution_id": execution_id,
                "execution_result": execution_result,
            }

        return {
            "action": "call_function",
            "execution_id": None,
            "execution_result": None,
        }


if __name__ == "__main__":
    appwrite = AppwriteUtility()
    # response = appwrite.register("gunag77730@gmail.com", "11111111")
    response = appwrite.register("", "")
    print(response)
    # response=appwrite.login("gunag77730@gmail.com", "11111111")
    # print(response)
