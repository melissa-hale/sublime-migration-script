from config.settings import ENDPOINTS
from config.templates import STRING_LIST_TEMPLATE, USER_GROUP_LIST_TEMPLATE

EXCLUDED_AUTHORS = {"Sublime Security", "System"}

def export_string_lists(source_client):
    string_list_data = source_client.get(ENDPOINTS["getStringLists"])

    # Filter out lists created by "Sublime Security" or "System"
    filtered_string_list_data = [
        lst for lst in string_list_data if lst.get("created_by_user_name") not in EXCLUDED_AUTHORS
    ]

    for string_list in filtered_string_list_data:
        list_id = string_list["id"]
        string_list_entries = source_client.get(ENDPOINTS["getListEntries"] + f"/{list_id}")
        string_list["entries"] = string_list_entries.get("entries", []) 

    return filtered_string_list_data

def import_string_lists(dest_client, string_list_data):
    for string_list in string_list_data:
        string_list_payload = STRING_LIST_TEMPLATE.copy()
        string_list_payload.update({
            "name": string_list.get("name", "Migrated String List"),
            "description": string_list.get("description", "No description found during migration"),
            "entries": string_list.get("entries", []),
        })
        dest_client.post(ENDPOINTS["createList"], string_list_payload)
        print(f"Imported string list: {string_list_payload['name']}")
        return

def export_user_group_lists(source_client):
    user_group_list_data = source_client.get(ENDPOINTS["getUserGroupLists"])

    # Filter out lists created by "Sublime Security" or "System"
    filtered_user_group_list_data = [
        lst for lst in user_group_list_data if lst.get("created_by_user_name") not in EXCLUDED_AUTHORS
    ]

    return filtered_user_group_list_data

def import_user_group_lists(dest_client, user_group_list_data):
    user_group_data = dest_client.get(ENDPOINTS["getUserGroups"])

    user_group_mapping = {
        group["name"]: group["id"] for group in user_group_data
    }

    for user_group_list in user_group_list_data:
        provider_group_name = user_group_list["provider_group_name"]
        
        if provider_group_name in user_group_mapping:
            user_group_list["provider_group_id"] = user_group_mapping[provider_group_name]
        else:
            print(f"Warning: No matching provider_group_id found for {provider_group_name}")
            continue

        user_group_list_payload = USER_GROUP_LIST_TEMPLATE.copy()
        user_group_list_payload.update({
            "name": user_group_list.get("name", "Migrated User Group List"),
            "description": user_group_list.get("description", "No description found during migration"),
            "provider_group_id": user_group_list.get("provider_group_id"),
        })
        dest_client.post(ENDPOINTS["createList"], user_group_list_payload)
        print(f"Imported user group list: {user_group_list_payload['name']}")

    return