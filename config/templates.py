WEBHOOK_ACTION_TEMPLATE = {
  "active": False,
  "config": {},
  "wait_for_complete_rule_evaluation": True,
  "name": "",
  "type": "webhook"
}

SLACK_ALERT_ACTION_TEMPLATE = {
  "active": False,
  "config": {},
  "name": "",
  "type": "slack_incoming_webhook"
}

STRING_LIST_TEMPLATE = {
  "name": "",
  "description": "",
  "entries": [],
  "entry_type": "string"
}

USER_GROUP_LIST_TEMPLATE = {
  "name": "",
  "description": "",
  "entries": [],
  "entry_type": "user_group",
  "provider_group_id": ""
}

DETECTION_RULE_TEMPLATE = {
  "action_ids": [],
  "active": False,
  "attack_types": [],
  "auto_review_auto_share": True,
  "auto_review_classification": "spam",
  "description": "tg",
  "detection_methods": [],
  "false_positives": [],
  "maturity": "",
  "name": "",
  "references": [],
  "severity": "",
  "source": "",
  "tactics_and_techniques": [],
  "tags": [],
  "type": "",
  "user_provided_tags": [],
  "triage_abuse_reports": None,
  "triage_flagged_messages": None
}

EXCLUSION_TO_RULE_TEMPLATE = {
    
}

EXCLUSION_TEMPLATE = {
    
}