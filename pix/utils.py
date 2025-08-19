# seed_db.py
from database import SessionLocal, engine
from debt import models

# Create all tables if they don't exist
models.Base.metadata.create_all(bind=engine)

# Get a new database session
db = SessionLocal()

print("Seeding database with initial data...")

try:
    # --- Sample Data ---
    people_to_add = [
        models.Person(name="João Silva"),
        models.Person(name="Maria Oliveira"),
        models.Person(name="Carlos Pereira"),
        models.Person(name="Ana Costa"),
    ]

    # Add people to the session
    db.add_all(people_to_add)
    db.commit()

    # --- Sample Debts ---
    # Refresh the objects to get their new IDs
    for person in people_to_add:
        db.refresh(person)

    debts_to_add = [
        models.Debt(item="Hambúrguer Artesanal", price=45.50, owner_id=people_to_add[0].id),
        models.Debt(item="Rodízio de Pizza", price=79.90, owner_id=people_to_add[0].id),
        models.Debt(item="Ingresso do Cinema", price=32.00, owner_id=people_to_add[1].id),
        models.Debt(item="Café e Pão de Queijo", price=15.75, owner_id=people_to_add[2].id),
        models.Debt(item="Corrida de Uber", price=25.00, owner_id=people_to_add[3].id),
        models.Debt(item="Açaí Completo", price=28.00, owner_id=people_to_add[3].id),
        models.Debt(item="Conta de Luz (dividida)", price=55.00, owner_id=people_to_add[3].id),
    ]

    # Add debts to the session
    db.add_all(debts_to_add)
    db.commit()

    print("✅ Database seeding complete!")

except Exception as e:
    print(f"An error occurred: {e}")
    db.rollback()

finally:
    db.close()
