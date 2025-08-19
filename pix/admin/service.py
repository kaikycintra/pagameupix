from sqlalchemy.orm import Session

from . import schemas
from . import models

def create_person(db: Session, person: schemas.PersonCreate) -> models.Person:
    """Creates a new Person record in the database."""
    db_person = models.Person(name=person.name)
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

def create_debt_for_person(db: Session, debt: schemas.DebtCreate, person_id: int) -> models.Debt:
    """Creates a new Debt record for a specific person."""
    db_debt = models.Debt(**debt.model_dump(), owner_id=person_id)
    db.add(db_debt)
    db.commit()
    db.refresh(db_debt)
    return db_debt

def delete_person_by_id(db: Session, person_id: int) -> models.Person | None:
    """Finds and deletes a person by their ID."""
    db_person = db.query(models.Person).filter(models.Person.id == person_id).first()
    if db_person:
        db.delete(db_person)
        db.commit()
    return db_person

def delete_debt_by_id(db: Session, debt_id: int) -> models.Debt | None:
    """Finds and deletes a debt by its ID."""
    db_debt = db.query(models.Debt).filter(models.Debt.id == debt_id).first()
    if db_debt:
        db.delete(db_debt)
        db.commit()
    return db_debt