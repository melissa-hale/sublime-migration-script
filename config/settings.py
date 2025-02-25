from dotenv import load_dotenv
import os

load_dotenv()

SOURCE_API_BASE_URL = os.getenv("SOURCE_API_BASE_URL")
DESTINATION_API_BASE_URL = os.getenv("DESTINATION_API_BASE_URL")

API_VERSION = "v1"
ENDPOINTS = {
    "feeds": f"/{API_VERSION}/feeds",
    "getRules": f"/{API_VERSION}/rules?in_feed=false&include_deleted=false",
    "rules": f"/{API_VERSION}/rules",
    "createRule": f"/{API_VERSION}/rules",
    "exclusions": f"/{API_VERSION}/config/exclusions",
    "actions": f"/{API_VERSION}/actions",
    "getStringLists": f"/{API_VERSION}/lists?list_types=string",
    "getListEntries": f"/{API_VERSION}/lists",
    "getUserGroupLists": f"/{API_VERSION}/lists?list_types=user_group",
    "getUserGroups": f"/{API_VERSION}/user-groups",
    "createList": f"/{API_VERSION}/lists",
}

SOURCE_API_KEY = os.getenv("SOURCE_API_KEY")
DESTINATION_API_KEY = os.getenv("DESTINATION_API_KEY")