import re
from config.settings import ENDPOINTS
from config.templates import EXCLUSION_TO_RULE_TEMPLATE
from utils.report import add_migrated, add_error


EXCLUSION_PATTERNS = {
    "recipient_email": re.compile(r"any\(recipients\.to, \.email\.email == '([^']+)'\)"),
    "sender_email": re.compile(r"sender\.email\.email == '([^']+)'"),
    "sender_domain": re.compile(r"sender\.email\.domain\.domain == '([^']+)'")
}

def extract_exclusion_type(exclusion_str):
    for exclusion_type, pattern in EXCLUSION_PATTERNS.items():
        match = pattern.search(exclusion_str)
        if match:
            return exclusion_type, match.group(1)
    return None, None

def fetch_all_rules(client, sublime_feed_id, limit=100):
    all_rules = []
    offset = 0

    while True:
        response = client.get(f"{ENDPOINTS["rules"]}?feed={sublime_feed_id}&limit={limit}&offset={offset}")

        all_rules.extend(response["rules"])
        count = response["count"]
        total = response["total"] 
        print(f"Fetched {count} rules (Offset: {offset}/{total})")

        if len(all_rules) >= total:
            break

        offset += limit

    return all_rules


def export_exclusions(source_client):
    """Fetches exclusions from source rules and maps them by rule name."""
    
    feeds = source_client.get(ENDPOINTS["feeds"])["feeds"]
    sublime_feed_id = next((feed["id"] for feed in feeds if feed["name"] == "Sublime Core Feed"), None)
    
    if not sublime_feed_id:
        print("Sublime Core Feed not found in source")
        return {}

    rules = fetch_all_rules(source_client, sublime_feed_id)

    exclusions_mapping = {}

    for rule in rules:
        rule_id = rule["id"]
        rule_name = rule["name"]

        rule_details = source_client.get(f"{ENDPOINTS['rules']}/{rule_id}")
        
        if len(rule_details["exclusions"]) > 0:
            exclusions_mapping[rule_name] = {}

            for exclusion in rule_details["exclusions"]:
                exclusion_type, exclusion_value = extract_exclusion_type(exclusion)

                if exclusion_type and exclusion_value:
                    exclusions_mapping[rule_name][exclusion_type] = exclusion_value

    #print(exclusions_mapping) ## {'Spam: Attendee List solicitation': {'recipient_email': 'penelope.seinfeld@gmail.com', 'sender_email': 'community@superdatascience.com', 'sender_domain': 'superdatascience.com'}}
    return exclusions_mapping


def import_exclusions(dest_client, exclusions_mapping):
    """Applies exclusions to matching rules in the destination."""

    feeds = dest_client.get(ENDPOINTS["feeds"])["feeds"]
    sublime_feed_id = next((feed["id"] for feed in feeds if feed["name"] == "Sublime Core Feed"), None)
    
    if not sublime_feed_id:
        print("Sublime Core Feed not found in destination")
        return

    rules = fetch_all_rules(dest_client, sublime_feed_id)
    
    rule_id_mapping = {rule["name"]: rule["id"] for rule in rules}  # Map rule names to IDs

    for rule_name, exclusions in exclusions_mapping.items():
        if rule_name not in rule_id_mapping:
            continue

        rule_id = rule_id_mapping[rule_name]

        for exclusion_type, exclusion_value in exclusions.items():
            exclusion_payload = {
                exclusion_type: exclusion_value
            }

            try:
                dest_client.post(f"{ENDPOINTS['rules']}/{rule_id}/add-exclusion", exclusion_payload)
                add_migrated(f"Exclusion {exclusion_type} -> {exclusion_value}", f"Rule: {rule_name}")
            except Exception as e:
                add_error(f"Exclusion {exclusion_type} -> {exclusion_value}", str(e))

    print("Exclusions migration complete!")
