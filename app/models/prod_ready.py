from .db import SCHEMA,environment

args = {}

if environment == "production":
    args["schema"] = SCHEMA

class PROD:
    __table_args__ = args