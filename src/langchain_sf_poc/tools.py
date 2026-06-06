from langchain_core.tools import tool

from langchain_sf_poc.sf_mcp_service import (
    search_accounts,
    get_account_by_id,
    get_open_cases_for_account,
    create_case,
)


@tool
def search_salesforce_accounts(search_term: str) -> str:
    """
    Search Salesforce accounts by name or industry.
    Use this when the user wants to find accounts.
    """
    return search_accounts(search_term)


@tool
def get_salesforce_account(account_id: str) -> str:
    """
    Get details for a Salesforce account by account id.
    Use this when the user provides an account id.
    """
    return get_account_by_id(account_id)


@tool
def get_salesforce_open_cases(account_id: str) -> str:
    """
    Get open cases for a Salesforce account.
    Use this when the user asks about cases for an account.
    """
    return get_open_cases_for_account(account_id)


@tool
def create_salesforce_case(
    account_id: str, subject: str, priority: str = "Medium"
) -> str:
    """
    Create a Salesforce case for an account.
    Use this when the user asks to create a case.
    """
    return create_case(
        account_id=account_id,
        subject=subject,
        priority=priority,
    )


tools = [
    search_salesforce_accounts,
    get_salesforce_account,
    get_salesforce_open_cases,
    create_salesforce_case,
]
