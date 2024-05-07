from ariadne import ObjectType, QueryType, gql, make_executable_schema

type_defs = gql("""
    type Query {
        hello: String!
        hey: String!        
    }
""")

query = QueryType()

@query.field("hello")
def resolve_hello(_, info):
    return "Hello, World!"

@query.field("hey")
def resolve_hey(_, info):
    return "Good morning"

schema = make_executable_schema(type_defs, query)
