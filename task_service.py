# task_service.py
from sqlalchemy import text
from config import engine

def create_task(task_data):
    with engine.begin() as conn: 
        bank_id = task_data["bankId"]
        amount = task_data["amount"]
        task_type = task_data["type"]

        if task_type == "WITHDRAW":
            conn.execute(
                text("UPDATE Bank SET balance = balance - :amount WHERE id = :bank_id"),
                {"amount": amount, "bank_id": bank_id}
            )
        elif task_type == "DEPOSIT":
            conn.execute(
                text("UPDATE Bank SET balance = balance + :amount WHERE id = :bank_id"),
                {"amount": amount, "bank_id": bank_id}
            )

        conn.execute(text("""
            INSERT INTO Task (id, bankId, amount, type, status, updatedAt)
            VALUES (:id, :bankId, :amount, :type, :status, NOW())
        """), task_data)
