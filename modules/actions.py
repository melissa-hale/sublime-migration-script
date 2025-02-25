from config.settings import ENDPOINTS
from config.templates import WEBHOOK_ACTION_TEMPLATE, SLACK_ALERT_ACTION_TEMPLATE

EXCLUDED_TYPES = {
    "quarantine_message", 
    "auto_review", 
    "move_to_spam", 
    "delete_message", 
    "warning_banner"
    }

def export_actions(source_client):
    actions_data = source_client.get(ENDPOINTS["actions"])

    # Filter out lists created by "Sublime Security" or "System"
    filtered_actions_data = [
        lst for lst in actions_data if lst.get("type") not in EXCLUDED_TYPES
    ]
    print(filtered_actions_data)

    return filtered_actions_data

def import_actions(dest_client, actions_data):
    for action in actions_data:
        if action["type"] == 'slack_incoming_webhook':
            slack_action_payload = SLACK_ALERT_ACTION_TEMPLATE.copy()
            slack_action_payload.update({
                "name": action.get("name", "Migrated Slack Alert Action"),
                "active": action.get("active", False),
                "config": action.get("config", {}),
            })
            print(slack_action_payload)
            dest_client.post(ENDPOINTS["actions"], slack_action_payload)
            print(f"Imported slack action: {slack_action_payload['name']}")
        elif action["type"] == 'webhook':
            webhook_action_payload = WEBHOOK_ACTION_TEMPLATE.copy()
            webhook_action_payload.update({
                "name": action.get("name", "Migrated Slack Alert Action"),
                "active": action.get("active", False),
                "config": action.get("config", {}),
                "wait_for_complete_rule_evaluation": action.get("wait_for_complete_rule_evaluation", True)
            })
            
            # ensure we pass a custom_headers object in config
            if "custom_headers" not in webhook_action_payload["config"]:
                webhook_action_payload["config"]["custom_headers"] = []
                
            dest_client.post(ENDPOINTS["actions"], webhook_action_payload)
            print(f"Imported webhook action: {webhook_action_payload['name']}")
    return