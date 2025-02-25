from utils.api_client import APIClient
from modules import feeds, rules, automations, exclusions, actions, lists
from utils.report import print_report

# Create API clients only once
source_client = APIClient(instance="source")
dest_client = APIClient(instance="destination")

def migrate():
    print("Starting migration...")

    # print("Migrating feeds...")
    # feeds_data = feeds.export_feeds(source_client)
    # feeds.import_feeds(dest_client, feeds_data)

    #### WORKING ####
    # print("Migrating actions...")
    # actions_data = actions.export_actions(source_client)
    # actions.import_actions(dest_client, actions_data)
    #### WORKING ####

    #### WORKING ####
    # print("Migrating string lists...")
    # string_lists_data = lists.export_string_lists(source_client)
    # lists.import_string_lists(dest_client, string_lists_data)
    #### WORKING ####
    
    #### WORKING ####
    # print("Migrating User Group lists...")
    # user_group_lists_data = lists.export_user_group_lists(source_client)
    # lists.import_user_group_lists(dest_client, user_group_lists_data)
    #### WORKING ####

    #### WORKING ####
    # print("Migrating rules...")
    # rules_data = rules.export_rules(source_client)
    # rules.import_rules(dest_client, rules_data)
    #### WORKING ####

    print("Migrating exclusions...")
    exclusions_data = exclusions.export_exclusions(source_client)
    exclusions.import_exclusions(dest_client, exclusions_data)

    print("Migration complete!")

if __name__ == "__main__":
    migrate()
    print_report()
