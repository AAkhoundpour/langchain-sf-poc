import os
import json
from simple_salesforce import Salesforce
from dotenv import load_dotenv

load_dotenv()


def get_salesforce_client():
    username = (os.getenv("SF_USERNAME") or "").strip()
    password = (os.getenv("SF_PASSWORD") or "").strip()
    security_token = (os.getenv("SF_SECURITY_TOKEN") or "").strip()
    domain = (os.getenv("SF_DOMAIN") or "test").strip()

    if not username or not password:
        raise ValueError("Missing SF_USERNAME or SF_PASSWORD in environment variables.")

    auth_kwargs = {
        "username": username,
        "password": password,
        "domain": domain,
    }

    if security_token:
        auth_kwargs["security_token"] = security_token

    return Salesforce(**auth_kwargs)


def run_readonly_soql(query: str) -> str:
    sf = get_salesforce_client()

    lowered = query.lower().strip()

    blocked_words = ["insert", "update", "delete", "undelete", "upsert", "merge"]

    if not lowered.startswith("select"):
        return json.dumps(
            {"success": False, "message": "Only SELECT queries are allowed."}
        )

    if any(word in lowered for word in blocked_words):
        return json.dumps(
            {"success": False, "message": "Only read-only SOQL is allowed."}
        )

    if " limit " not in lowered:
        query += " LIMIT 20"

    result = sf.query(query)

    return json.dumps(
        {
            "success": True,
            "totalSize": result.get("totalSize"),
            "records": result.get("records", []),
        },
        default=str,
        indent=2,
    )
