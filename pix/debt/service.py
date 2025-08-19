from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List

from . import models

def search_people_by_name(
    db: Session,
    q: Optional[str] = None,
    field_name: str = "name",
    limit: int = 100
) -> List[str | int]:
    """
    Searches for people by name using a case-insensitive partial match (ILIKE),
    or returns all people if no query is provided.
    Results are always ordered alphabetically by name.
    """
    allowed_fields = ["id", "name"]
    if field_name not in allowed_fields:
        raise ValueError(f"Invalid field selected. Allowed fields are: {allowed_fields}")

    selected_column = getattr(models.Person, field_name)
    query = db.query(selected_column)

    if q:
        search_pattern = f"%{q}%"
        query = query.filter(models.Person.name.ilike(search_pattern))

    results = query.order_by(models.Person.name).limit(limit).all()
    results = [row[0] for row in results]

    return results

def get_top_debtors(db: Session, limit: int = 5) -> List:
    """
    Performs the database query to find the top debtors.
    """
    return (
        db.query(
            models.Person.name,
            func.sum(models.Debt.price).label("total_debt")
        )
        .join(models.Debt, models.Person.id == models.Debt.owner_id)
        .group_by(models.Person.id)
        .order_by(func.sum(models.Debt.price).desc())
        .limit(limit)
        .all()
    )