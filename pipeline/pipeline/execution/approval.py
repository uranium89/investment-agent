import json
import logging
import os
from datetime import datetime, timedelta
from typing import Any

from pipeline.config import settings

logger = logging.getLogger(__name__)

APPROVAL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "approvals")


class ApprovalError(Exception):
    pass


def _ensure_approval_dir():
    os.makedirs(APPROVAL_DIR, exist_ok=True)


def _approval_path(run_id: str) -> str:
    return os.path.join(APPROVAL_DIR, f"{run_id}.json")


def create_approval_request(proposed_trades: list[dict]) -> str:
    _ensure_approval_dir()
    run_id = datetime.now().strftime("trade_%Y%m%d_%H%M%S")
    request = {
        "run_id": run_id,
        "created_at": datetime.now().isoformat(),
        "expires_at": (datetime.now() + timedelta(minutes=settings.approval_timeout_minutes)).isoformat(),
        "status": "pending",
        "proposed_trades": proposed_trades,
    }
    with open(_approval_path(run_id), "w") as f:
        json.dump(request, f, indent=2, default=str)
    logger.info("Approval request created: %s (%d trades)", run_id, len(proposed_trades))
    return run_id


def check_approval(run_id: str) -> dict[str, Any]:
    path = _approval_path(run_id)
    if not os.path.exists(path):
        raise ApprovalError(f"Approval request not found: {run_id}")
    with open(path) as f:
        request = json.load(f)

    if request["status"] == "approved":
        return {"approved": True, "notes": request.get("approval_notes", "")}
    elif request["status"] == "rejected":
        return {"approved": False, "reason": request.get("rejection_reason", "No reason given")}
    elif request["status"] == "pending":
        expires = datetime.fromisoformat(request["expires_at"])
        if datetime.now() > expires:
            request["status"] = "expired"
            with open(path, "w") as f:
                json.dump(request, f, indent=2, default=str)
            return {"approved": False, "reason": "Approval timeout expired"}
        return {"approved": None, "reason": "Pending approval"}
    return {"approved": False, "reason": f"Unknown status: {request['status']}"}


def wait_for_approval(run_id: str) -> dict[str, Any]:
    if not settings.approval_required:
        logger.info("Approval not required, auto-approving")
        return {"approved": True}

    result = check_approval(run_id)
    if result["approved"] is None:
        msg = (
            f"⚠️  TRADES PENDING APPROVAL: {run_id}\n"
            f"   File: {_approval_path(run_id)}\n"
            f"   Edit the file and set \"status\": \"approved\" or \"rejected\"\n"
            f"   Timeout: {settings.approval_timeout_minutes} minutes"
        )
        logger.warning(msg)
        print("\n" + "=" * 60)
        print(msg)
        print("=" * 60 + "\n")
        while True:
            import time
            time.sleep(10)
            result = check_approval(run_id)
            if result["approved"] is not None:
                return result
    return result