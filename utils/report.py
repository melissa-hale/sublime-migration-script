
REPORT = {
    "migrated_items": [],
    "skipped_items": [],
    "errors": []
}

def add_migrated(item_name, item_type):
    """Log a successfully migrated item."""
    REPORT["migrated_items"].append({"name": item_name, "type": item_type})

def add_skipped(item_name, reason):
    """Log a skipped item with a reason."""
    REPORT["skipped_items"].append({"name": item_name, "reason": reason})

def add_error(item_name, error_message):
    """Log an error that occurred during migration."""
    REPORT["errors"].append({"name": item_name, "error": error_message})

def print_report():
    """Prints the final migration report in a structured format."""
    print("\n=== Migration Report ===")

    print("\n✅ Migrated Items:")
    for item in REPORT["migrated_items"]:
        print(f"  - {item['type']}: {item['name']}")

    print("\n⚠️ Skipped Items:")
    for item in REPORT["skipped_items"]:
        print(f"  - {item['name']} (Reason: {item['reason']})")

    print("\n❌ Errors:")
    for error in REPORT["errors"]:
        print(f"  - {error['name']} (Error: {error['error']})")

    print("\n=======================")
