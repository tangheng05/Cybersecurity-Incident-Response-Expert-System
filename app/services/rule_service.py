from typing import List, Optional
from app.models import Rule, AttackType
from extensions import db


class RuleService:
    @staticmethod
    def get_all(active_only: bool = False) -> List[Rule]:
        query = Rule.query
        if active_only:
            query = query.filter_by(is_active=True)
        return list(query.order_by(Rule.priority.desc(), Rule.severity_score.desc()).all())

    @staticmethod
    def get_by_id(rule_id: int) -> Optional[Rule]:
        return Rule.query.get(rule_id)

    @staticmethod
    def get_by_attack_type(attack_type_id: int, active_only: bool = True) -> List[Rule]:
        query = Rule.query.filter_by(attack_type_id=attack_type_id)
        if active_only:
            query = query.filter_by(is_active=True)
        return list(query.order_by(Rule.priority.desc(), Rule.severity_score.desc()).all())

    @staticmethod
    def create(data: dict) -> Rule:
        # Validate conditions and actions are not empty
        if not data.get("conditions") or not isinstance(data["conditions"], dict) or len(data["conditions"]) == 0:
            raise ValueError("Conditions cannot be empty. At least one condition is required.")
        
        if not data.get("actions") or not isinstance(data["actions"], list) or len(data["actions"]) == 0:
            raise ValueError("Actions cannot be empty. At least one action is required.")
        
        # Convert match_threshold from percentage (1-100) to decimal (0.01-1.0)
        match_threshold = data.get("match_threshold", 70) / 100.0
        
        rule = Rule(
            name=data["name"],
            attack_type_id=data["attack_type_id"],
            conditions=data["conditions"],
            actions=data["actions"],
            priority=data.get("priority", "medium"),
            severity_score=data.get("severity_score", 5),
            match_threshold=match_threshold,
            is_active=data.get("is_active", True),
        )
        db.session.add(rule)
        db.session.commit()
        return rule

    @staticmethod
    def update(rule: Rule, data: dict) -> Rule:
        # Validate conditions and actions are not empty
        if not data.get("conditions") or not isinstance(data["conditions"], dict) or len(data["conditions"]) == 0:
            raise ValueError("Conditions cannot be empty. At least one condition is required.")
        
        if not data.get("actions") or not isinstance(data["actions"], list) or len(data["actions"]) == 0:
            raise ValueError("Actions cannot be empty. At least one action is required.")
        
        # Convert match_threshold from percentage (1-100) to decimal (0.01-1.0)
        match_threshold = data.get("match_threshold", 70) / 100.0
        
        rule.name = data["name"]
        rule.attack_type_id = data["attack_type_id"]
        rule.conditions = data["conditions"]
        rule.actions = data["actions"]
        rule.priority = data.get("priority", "medium")
        rule.severity_score = data.get("severity_score", 5)
        rule.match_threshold = match_threshold
        rule.is_active = data.get("is_active", True)
        db.session.commit()
        return rule

    @staticmethod
    def delete(rule: Rule) -> None:
        db.session.delete(rule)
        db.session.commit()

    @staticmethod
    def toggle_active(rule: Rule) -> Rule:
        rule.is_active = not rule.is_active
        db.session.commit()
        return rule
