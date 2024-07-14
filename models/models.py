from configuration.extensions import get_mongo_client

client = get_mongo_client()
mongo = client.get_database('User')

class User:
    @staticmethod
    def find_by_email(email):
        return mongo.db.users.find_one({"email": email})

    @staticmethod
    def find_by_username(username):
        return mongo.db.users.find_one({"username": username})

    @staticmethod
    def insert(user):
        return mongo.db.users.insert_one(user)
    
    @staticmethod
    def update_last_login(id, dt):
        return mongo.db.users.update_one({"_id": id}, {"$set": {"last_login": dt}})