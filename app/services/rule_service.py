from typing import List, Optional
from app.models import Rule, AttackType
from extensions import db


class RuleService:
    @staticmethod
    def get_all(active_only: bool = False) -> List[Rule]:
        query = Rule.query
        if active_only:
            query = query.filter_by(is_active=True)
        return list(query.order_by(Rule.created_at.desc()).all())

    @staticmethod
    def get_by_id(rule_id: int) -> Optional[Rule]:
        return Rule.query.get(rule_id)

    @staticmethod
    def get_by_attack_type(attack_type_id: int, active_only: bool = True) -> List[Rule]:
        query = Rule.query.filter_by(attack_type_id=attack_type_id)
        if active_only:
            query = query.filter_by(is_active=True)
        return list(query.order_by(Rule.created_at.desc()).all())

    @staticmethod
    def create(data: dict) -> Rule:
        symbolic_conditions = data.get("symbolic_conditions", [])
        if not symbolic_conditions or len(symbolic_conditions) == 0:
            raise ValueError("Symbolic conditions cannot be empty.")
        
        rule = Rule(
            name=data["name"],
            attack_type_id=data["attack_type_id"],
            symbolic_conditions=symbolic_conditions,
            conclusion=data.get("conclusion"),
            cf=data.get("cf"),
            is_active=data.get("is_active", True),
        )
        db.session.add(rule)
        db.session.commit()
        return rule

    @staticmethod
    def update(rule: Rule, data: dict) -> Rule:
        symbolic_conditions = data.get("symbolic_conditions", [])
        if not symbolic_conditions or len(symbolic_conditions) == 0:
            raise ValueError("Symbolic conditions cannot be empty.")
        
        rule.name = data["name"]
        rule.attack_type_id = data["attack_type_id"]
        rule.symbolic_conditions = symbolic_conditions
        rule.conclusion = data.get("conclusion")
        rule.cf = data.get("cf")
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
