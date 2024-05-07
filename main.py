from fastapi import FastAPI
from ariadne.asgi import GraphQL

from schema import schema

app = FastAPI()

app.mount("/graphql", GraphQL(schema, debug=True))
