"""
Central Supervisor Router Engine
Sovereign Multi-Agent AI Platform for Government of Pakistan
"""

import json
from typing import Dict, Any

class CentralSupervisorRouter:
    """
    Central Supervisor Router determining jurisdictional routing across
    34 Federal Ministries and 105 Provincial Departments.
    """
    def __init__(self):
        self.federal_domain_keys = ["defense", "foreign affairs", "currency", "telecom", "national highways", "drap", "fbr", "mof", "tax"]
        self.provincial_domain_keys = ["health", "education", "agriculture", "local government", "police", "pra", "srb", "kra", "bra"]

    def classify_and_route(self, query: str) -> Dict[str, Any]:
        if not query or not query.strip():
            raise ValueError("Query string cannot be empty.")

        q_lower = query.lower()
        is_fed = any(k in q_lower for k in self.federal_domain_keys)
        is_prov = any(k in q_lower for k in self.provincial_domain_keys)

        if is_fed and not is_prov:
            jurisdiction = "FEDERAL"
            province = None
            dept = self._detect_federal_dept(q_lower)
            conf = 0.95
            reason = "Query aligns with Federal Rules of Business 1973."
        elif is_prov:
            jurisdiction = "PROVINCIAL"
            province = self._detect_province(q_lower) or "Punjab"
            dept = self._detect_provincial_dept(q_lower)
            conf = 0.92
            reason = "Query pertains to Provincial jurisdiction under 18th Amendment."
        else:
            jurisdiction = "SHARED_JURISDICTION"
            province = "Multi-Region"
            dept = "Policy Handoff Agent"
            conf = 0.65
            reason = "Cross-cutting query requiring inter-agency coordination."

        next_action = "route_to_agent" if conf >= 0.70 else "ask_clarification"

        return {
            "query": query,
            "jurisdiction": jurisdiction,
            "province": province,
            "department": dept,
            "confidence": conf,
            "reason": reason,
            "next_action": next_action
        }

    def _detect_province(self, text: str) -> str:
        if "sindh" in text: return "Sindh"
        if "kpk" in text or "khyber" in text: return "KPK"
        if "balochistan" in text: return "Balochistan"
        if "punjab" in text: return "Punjab"
        return "Punjab"

    def _detect_federal_dept(self, text: str) -> str:
        if "tax" in text or "fbr" in text or "finance" in text:
            return "Ministry of Finance / FBR"
        return "Cabinet Division"

    def _detect_provincial_dept(self, text: str) -> str:
        if "health" in text:
            return "Department of Health"
        if "education" in text:
            return "Department of Education"
        return "Provincial Revenue Board"

if __name__ == "__main__":
    router = CentralSupervisorRouter()
    print("Central Supervisor Router Initialized.")
    sample_res = router.classify_and_route("What is the federal tax rate under FBR?")
    print(json.dumps(sample_res, indent=2))
