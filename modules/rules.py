from config.settings import ENDPOINTS
from config.templates import DETECTION_RULE_TEMPLATE
from utils.report import add_migrated, add_skipped, add_error

EXCLUDED_ACTION_TYPES = {
    "alert_smtp", 
    "alert_smtp_eml", 
    "hud", 
    "report"
    }

def is_non_imported_type(source_client, action_id):
    action_data = source_client.get(ENDPOINTS["actions"] + f"/{action_id}")
    if action_data["type"] in EXCLUDED_ACTION_TYPES:
        return True, action_data["name"]
    else:
         return False, action_data

def export_rules(source_client):
    rules_data = source_client.get(ENDPOINTS["getRules"])["rules"]

    ## filter out actions that aren't imported
    for rule in rules_data[:]:
        if "Sublime-Standard-Test-String" in rule["source"]:
            rules_data.remove(rule)
            continue

        if len(rule["actions"]) > 0:
            rule_name = rule["name"]
            filtered_actions = []

            for action in rule["actions"]:
                action_id = action["id"]
                non_imported_action, action_data = is_non_imported_type(source_client, action_id)

                if non_imported_action:
                    add_skipped(
                        f"Action to Rule: {non_imported_action[1]} -> {rule_name}",
                        f"Unsupported type, please manually assign action to rule"
                    )
                else:
                    action["config"] = action_data["config"]
                    action["type"] = action_data["type"]
                    filtered_actions.append(action)

            rule["actions"] = filtered_actions

    return rules_data


def import_rules(dest_client, rules_data):
    ## set up lookup objects for mapping actionIds
    dest_actions_data = dest_client.get(ENDPOINTS["actions"])

    dest_actions_lookup = {
        (action["name"], action["type"], str(action["config"])): action["id"]
        for action in dest_actions_data
    }

    warning_banner_lookup = {
        (action["name"], action["type"]): action["id"]
        for action in dest_actions_data if action["type"] == "warning_banner"
    }

    ## now iterate over the data, map the actionIds and build the payload
    for rule in rules_data:
        rule_payload = DETECTION_RULE_TEMPLATE.copy()

        mapped_action_ids = []
        for action in rule.get("actions", {}):
            action_name = action["name"]
            action_type = action["type"]
            action_config = str(action["config"])

            if action_type == "warning_banner":
                matching_action_id = warning_banner_lookup.get((action_name, action_type))
            else:
                matching_action_id = dest_actions_lookup.get((action_name, action_type, action_config))

            if matching_action_id:
                mapped_action_ids.append(matching_action_id)
            else:
                print(f"⚠️ Warning: No matching action found for {action_name} (type: {action_type}).")

        rule_payload.update({
            "name": rule.get("name", "Migrated Rule"),
            "description": rule.get("description", "No description found during migration"),
            "source": rule.get("source", ""),
            "active": rule.get("active", False),
            "action_ids": mapped_action_ids,
            "attack_types": rule.get("attack_types", []),
            "auto_review_auto_share": rule.get("auto_review_auto_share", None),
            "auto_review_classification": rule.get("auto_review_classification", None),
            "detection_methods": rule.get("detection_methods", []),
            "false_positives": rule.get("false_positives", []),
            "maturity": rule.get("maturity", None),
            "references": rule.get("references", []),
            "severity": rule.get("severity", None),
            "tactics_and_techniques": rule.get("tactics_and_techniques", []),
            "tags": rule.get("tags", []),
            "type": rule.get("type", "detection"),
            "user_provided_tags": rule.get("user_provided_tags", []),
            "authors": [
                {
                "name": rule.get("created_by_user_name", ""),
                }
            ],
            "triage_flagged_messages": rule.get("triage_flagged_messages", None),
            "triage_abuse_reports": rule.get("triage_abuse_reports", None)
        })
        
        try:
            dest_client.post(ENDPOINTS["createRule"], rule_payload)
            add_migrated(rule_payload.get("name", "Unnamed Rule"), "Rule (detection or automation)")
        except Exception as e:
            add_error(rule_payload.get("name", "Unnamed Rule"), str(e))

        print(f"Imported rule: {rule_payload['name']}")
