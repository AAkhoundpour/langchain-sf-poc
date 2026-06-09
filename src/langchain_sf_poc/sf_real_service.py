import os
import json
from simple_salesforce import Salesforce, SalesforceLogin
from dotenv import load_dotenv

load_dotenv()


def get_salesforce_client():
    username = (os.getenv("SF_USERNAME") or "").strip()
    password = (os.getenv("SF_PASSWORD") or "").strip()
    security_token = (os.getenv("SF_SECURITY_TOKEN") or "").strip()
    consumer_key = (os.getenv("SF_CONSUMER_KEY") or "").strip()
    consumer_secret = (os.getenv("SF_CONSUMER_SECRET") or "").strip()
    domain = (os.getenv("SF_DOMAIN") or "test").strip()

    if not username or not password:
        raise ValueError("Missing SF_USERNAME or SF_PASSWORD in environment variables.")

    if bool(consumer_key) != bool(consumer_secret):
        raise ValueError(
            "Both SF_CONSUMER_KEY and SF_CONSUMER_SECRET must be set together."
        )

    if consumer_key and consumer_secret:
        login_kwargs = {
            "username": username,
            "password": password,
            "domain": domain,
            "consumer_key": consumer_key,
            "consumer_secret": consumer_secret,
        }
        if security_token:
            login_kwargs["security_token"] = security_token

        session_id, instance = SalesforceLogin(**login_kwargs)
        return Salesforce(instance=instance, session_id=session_id)

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
