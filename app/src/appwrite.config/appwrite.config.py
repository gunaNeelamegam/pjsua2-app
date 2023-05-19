from appwrite.client import Client
from appwrite.services.users import Users

client = Client()

'''
Needs to go into .env file 

'''

DATA_BASE="646728422216731449db"
MSG_COLLECTION="646728b1674904949d2e"


(
    client.set_endpoint("https://cloud.appwrite.io/v1")  # Your API Endpoint
    .set_project("6467258dd958cabe5afc")  # Your project ID
    .set_key(
        "e757628dc7db8a156c9debdc516f15e200888358f2024ca3d7bda324f3a5d58a1c5a65b94647775cc3c340b48d2855135a776a44c617123e4b486359376aa399faba1ff0dc1f221f562c88098d612e9eb31b844f8df25177aa6e2b330dd46f448d3d631146064dbe2d4e822b5a0237fdfd79eb2745321d41e640b85dc1f0acfe"
    )
)

from appwrite.id import ID
from appwrite.services.users import Users

## REGISTER 

users = Users(client)

user = users.create(
    user_id=ID.unique(), email="gunag5127@gmail.com", phone="+918608811046", password="password"
)


##SIGN IN





### SIGNOUT



### GET ALL USERS



### GET ALL COLLECTIONS




### GET ALL DOCUMENTS




### QUERY DOCUMENTS




### DELETE USER




### DELETE DDCUMENTS






