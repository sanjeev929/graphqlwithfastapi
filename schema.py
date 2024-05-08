from ariadne import QueryType, gql,make_executable_schema
from motor.motor_asyncio import AsyncIOMotorClient

MONGODB_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGODB_URL)
db = client["graphql"]
users_collection = db["test"]

type_defs = gql("""
        type Query{
                users(name: String):[User]!
        }
        type User{
            _id: ID!
            name: String!
            email: String!
            age: Int            
        }       
""")
query = QueryType()

@query.field("users")
async def resolve_users(_,info,name=None):
    try:
        if name:
            user_data = await users_collection.find_one({"name":name})
            return [user_data]
        else:
            cursor = users_collection.find({})
            user_data = await cursor.to_list(length=None)
            for user in user_data:
                user["_id"] = str(user["_id"])
            return user_data
    except Exception as e:
        return None   

schema =make_executable_schema(type_defs,query)         