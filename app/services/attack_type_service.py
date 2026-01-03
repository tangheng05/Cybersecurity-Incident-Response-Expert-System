from typing import List, Optional
from app.models import AttackType
from extensions import db


class AttackTypeService:
    @staticmethod
    def get_all(active_only: bool = False) -> List[AttackType]:
        query = AttackType.query
        if active_only:
            query = query.filter_by(is_active=True)
        return list(query.order_by(AttackType.name).all())

    @staticmethod
    def get_by_id(attack_type_id: int) -> Optional[AttackType]:
        return AttackType.query.get(attack_type_id)

    @staticmethod
    def get_by_name(name: str) -> Optional[AttackType]:
        return AttackType.query.filter_by(name=name).first()

    @staticmethod
    def create(data: dict) -> AttackType:
        attack_type = AttackType(
            name=data["name"],
            description=data.get("description", ""),
            severity_level=data.get("severity_level", 5),
            is_active=data.get("is_active", True),
        )
        db.session.add(attack_type)
        db.session.commit()
        return attack_type
