import json
import os
from typing import Any

from email_audit_app.core.schemas.audit_schema import AuditResult
from email_audit_app.core.schemas.audit_schema import AuditStatus
from email_audit_app.core.schemas.audit_schema import RuleResult

RULES_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'rules.json')

class RuleEvaluator:
    def evaluate_condition(self,
                           condition: str,
                           email: dict[str, Any],
                           /) -> bool:
        try:
            return bool(eval(condition, {"__builtins__": {}, "any": any, "str":str, "email": email}, {"email": email}))

        except Exception:
            return False


class RuleEngine:
    def __init__(self,
                 rules_file: str = RULES_PATH,
                 /) -> None:
        self.rules = self._load_rules(rules_file)
        self.evaluator = RuleEvaluator()

    def _load_rules(self,
                    rules_file: str,
                    /) -> list[dict[str, Any]]:
        try:
            with open(rules_file) as f:
                return json.load(f)

        except FileNotFoundError:
            return self._get_default_rules()

    def _get_default_rules(self,
                           /) -> list[dict[str, Any]]:
        return [
            {
                "name": "Greeting Check",
                "description": "Check if email starts with a greeting",
                "condition": "[greeting for greeting in ['hello', 'hi', 'dear'] if email['body'].lower().strip().startswith(greeting)]",
                "score": 10,
                "justification_pass": "Greeting found.",
                "justification_fail": "No greeting found at the start of the email."
            },
            {
                "name": "Clear Subject",
                "description": "Check if subject line is present and not empty",
                "condition": "email['subject'] is not None and len(email['subject'].strip()) > 0",
                "score": 10,
                "justification_pass": "Subject line is present.",
                "justification_fail": "Subject line is missing or empty."
            }
        ]

    def evaluate(self,
                 email_content: dict[str, Any],
                 /) -> AuditResult:
        results = []
        total_score = 0
        possible_score = 0

        for rule in self.rules:
            passed = self.evaluator.evaluate_condition(rule["condition"], email_content)
            score = rule["score"] if passed else 0

            results.append(RuleResult(
                rule_name=rule["name"],
                passed=passed,
                score=score,
                justification=rule["justification_pass"] if passed else rule["justification_fail"]
            ))

            total_score += score
            possible_score += rule["score"]

        return AuditResult(
            status=AuditStatus.SUCCESS,
            overall_score=(total_score / possible_score * 10) if possible_score > 0 else 0,
            rule_results=results
        )
