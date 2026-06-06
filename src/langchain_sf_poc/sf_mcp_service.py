# src/langchain_sf_poc/sf_mcp_service.py

import json
from datetime import datetime, timezone
from typing import Any

# -------------------------------------------------------------------
# Mock Salesforce data
# -------------------------------------------------------------------

ACCOUNTS: list[dict[str, Any]] = [
    {
        "id": "A-1001",
        "name": "Inquisitive Education",
        "industry": "Education",
        "status": "Active",
        "annual_revenue": 1_200_000,
    },
    {
        "id": "A-1002",
        "name": "Sydney Learning Group",
        "industry": "Education",
        "status": "Active",
        "annual_revenue": 850_000,
    },
    {
        "id": "A-1003",
        "name": "Northside Finance",
        "industry": "Financial Services",
        "status": "Active",
        "annual_revenue": 3_500_000,
    },
    {
        "id": "A-1004",
        "name": "Cloud Retail Co",
        "industry": "Retail",
        "status": "Inactive",
        "annual_revenue": 670_000,
    },
]


CASES: list[dict[str, Any]] = [
    {
        "id": "C-5001",
        "account_id": "A-1001",
        "subject": "Login issue for teacher portal",
        "status": "New",
        "priority": "High",
    },
    {
        "id": "C-5002",
        "account_id": "A-1001",
        "subject": "Question about invoice",
        "status": "Closed",
        "priority": "Low",
    },
    {
        "id": "C-5003",
        "account_id": "A-1002",
        "subject": "Payment webhook failed",
        "status": "Working",
        "priority": "High",
    },
    {
        "id": "C-5004",
        "account_id": "A-1003",
        "subject": "API timeout from integration",
        "status": "New",
        "priority": "Medium",
    },
]


# -------------------------------------------------------------------
# Helper functions
# -------------------------------------------------------------------


def _to_json(data: Any) -> str:
    """
    Convert Python data to a pretty JSON string.

    LangChain tools can return strings safely, and JSON strings are easy
    for the model to read and reason about.
    """
    return json.dumps(data, indent=2, default=str)


def _find_account(account_id: str) -> dict[str, Any] | None:
    """
    Find one account by mock Salesforce account id.
    """
    for account in ACCOUNTS:
        if account["id"].lower() == account_id.lower():
            return account

    return None


def _next_case_id() -> str:
    """
    Generate the next mock Case id.
    """
    return f"C-{5000 + len(CASES) + 1}"


# -------------------------------------------------------------------
# Mock MCP-style service functions
# -------------------------------------------------------------------


def search_accounts(search_term: str) -> str:
    """
    Search mock Salesforce accounts by name, industry, status, or id.

    This simulates a Salesforce MCP tool/service function.
    """
    term = search_term.strip().lower()

    if not term:
        return _to_json(
            {
                "success": False,
                "message": "Search term is required.",
                "records": [],
            }
        )

    matched_accounts = []

    for account in ACCOUNTS:
        searchable_text = " ".join(
            [
                str(account.get("id", "")),
                str(account.get("name", "")),
                str(account.get("industry", "")),
                str(account.get("status", "")),
            ]
        ).lower()

        if term in searchable_text:
            matched_accounts.append(account)

    return _to_json(
        {
            "success": True,
            "search_term": search_term,
            "total_records": len(matched_accounts),
            "records": matched_accounts,
        }
    )


def get_account_by_id(account_id: str) -> str:
    """
    Get one mock Salesforce account by id.
    """
    account = _find_account(account_id)

    if account is None:
        return _to_json(
            {
                "success": False,
                "message": f"No account found for id {account_id}.",
                "record": None,
            }
        )

    return _to_json(
        {
            "success": True,
            "record": account,
        }
    )


def get_open_cases_for_account(account_id: str) -> str:
    """
    Get open cases for one mock Salesforce account.

    Closed cases are excluded.
    """
    account = _find_account(account_id)

    if account is None:
        return _to_json(
            {
                "success": False,
                "message": f"No account found for id {account_id}.",
                "records": [],
            }
        )

    open_cases = [
        case
        for case in CASES
        if case["account_id"].lower() == account_id.lower()
        and case["status"].lower() != "closed"
    ]

    return _to_json(
        {
            "success": True,
            "account": {
                "id": account["id"],
                "name": account["name"],
            },
            "total_records": len(open_cases),
            "records": open_cases,
        }
    )


def create_case(account_id: str, subject: str, priority: str = "Medium") -> str:
    """
    Create a mock Salesforce Case.

    This does not call real Salesforce. It only appends to the in-memory
    CASES list while the Python process is running.
    """
    account = _find_account(account_id)

    if account is None:
        return _to_json(
            {
                "success": False,
                "message": f"Cannot create case. No account found for id {account_id}.",
                "record": None,
            }
        )

    clean_subject = subject.strip()
    clean_priority = priority.strip().title() if priority else "Medium"

    if not clean_subject:
        return _to_json(
            {
                "success": False,
                "message": "Cannot create case. Subject is required.",
                "record": None,
            }
        )

    if clean_priority not in {"Low", "Medium", "High", "Critical"}:
        clean_priority = "Medium"

    new_case = {
        "id": _next_case_id(),
        "account_id": account["id"],
        "subject": clean_subject,
        "status": "New",
        "priority": clean_priority,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    CASES.append(new_case)

    return _to_json(
        {
            "success": True,
            "message": "Case created successfully.",
            "record": new_case,
        }
    )


def get_case_by_id(case_id: str) -> str:
    """
    Optional helper: get one mock Salesforce Case by id.
    """
    for case in CASES:
        if case["id"].lower() == case_id.lower():
            return _to_json(
                {
                    "success": True,
                    "record": case,
                }
            )

    return _to_json(
        {
            "success": False,
            "message": f"No case found for id {case_id}.",
            "record": None,
        }
    )


def health_check() -> str:
    """
    Optional helper to confirm the mock service is working.
    """
    return _to_json(
        {
            "success": True,
            "service": "mock_sf_mcp_service",
            "accounts_loaded": len(ACCOUNTS),
            "cases_loaded": len(CASES),
        }
    )
