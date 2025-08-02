from sqlalchemy import text
from config import engine, logger

def get_accounts():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT id, name, accountHolder, accountNo 
                FROM Bank
                ORDER BY name
            """))
            accounts = result.fetchall()
            logger.info(f"Retrieved {len(accounts)} accounts")
            return accounts
    except Exception as e:
        logger.error(f"Error retrieving accounts: {str(e)}")
        raise

def get_banks(date_range):
    try:
        with engine.connect() as conn:
            start_date, end_date = date_range
            result = conn.execute(text("""
               SELECT 
                    IFNULL(SUM(a.amount), 0) AS total,
                    b.name,
                    b.accountNo
                FROM 
                    Task AS a 
                RIGHT JOIN 
                    Bank AS b 
                ON 
                    a.bankId = b.id 
                AND 
                    a.updatedAt BETWEEN :start_date AND :end_date
                GROUP BY 
                    b.id;
            """), {"start_date": start_date, "end_date": end_date})
            accounts = result.fetchall()
            logger.info(f"Retrieved {len(accounts)} accounts")
            return accounts
    except Exception as e:
        logger.error(f"Error retrieving accounts: {str(e)}")
        raise

def get_transactions(bank_id, date_range=None):
    try:
        with engine.connect() as conn:
            BATCH_SIZE = 1000
            all_transactions = []
            offset = 0
            
            # Base query
            query = """
                SELECT  a.amount, a.type, a.status, a.updatedAt, a.reason,b.code
                FROM 
                    Task as a 
                RIGHT JOIN 
	                Branch as b
                ON 
	                a.branchId = b.id
                WHERE bankId = :bank_id and a.isDelete = false
            """
            
            # Add date filter if provided
            params = {"bank_id": bank_id}
            if date_range:
                start_date, end_date = date_range
                query += " AND a.updatedAt BETWEEN :start_date AND :end_date"
                params["start_date"] = start_date
                params["end_date"] = end_date
                
            query += " ORDER BY a.updatedAt DESC LIMIT :limit OFFSET :offset"
            
            while True:
                params["limit"] = BATCH_SIZE
                params["offset"] = offset
                
                result = conn.execute(text(query), params)
                
                batch = result.fetchall()
                if not batch:
                    break
                    
                all_transactions.extend(batch)
                offset += BATCH_SIZE
                
                if len(batch) < BATCH_SIZE:
                    break
            
            logger.info(f"Retrieved {len(all_transactions)} transactions for bank_id {bank_id}")
            return all_transactions
    except Exception as e:
        logger.error(f"Error retrieving transactions for bank_id {bank_id}: {str(e)}")
        raise

def get_branches(date_range):
    try:
        with engine.connect() as conn:
            start_date, end_date = date_range
            result = conn.execute(text("""
               SELECT 
                    SUM(CASE WHEN type = 'deposit' THEN amount WHEN type = 'withdraw' THEN -amount ELSE 0 END) AS total,
                    b.code 
                FROM 
                    Task AS a 
                RIGHT JOIN 
                    Branch AS b 
                ON 
                    a.branchId = b.id 
                AND a.updatedAt BETWEEN :start_date AND :end_date
                GROUP BY 
                b.id;
            """), {"start_date": start_date, "end_date": end_date})
            branches = result.fetchall()
            logger.info(f"Retrieved {len(branches)} branches for date range {date_range}")
            return branches
    except Exception as e:
        logger.error(f"Error retrieving branches: {str(e)}")
        raise
def get_total(date_range):
    try:
        with engine.connect() as conn:
            start_date, end_date = date_range
            
            # Query for pending total
            pending_result = conn.execute(text("""
                SELECT COALESCE(SUM(amount), 0) as pending_total
                FROM Task
                WHERE status IN ('PENDING', 'ADMIN_PENDING')
                OR (status IN ('PENDING', 'ADMIN_PENDING') AND updatedAt BETWEEN :start_date AND :end_date)
                
            """), {"start_date": start_date, "end_date": end_date})
            pending_total = pending_result.scalar() or 0
            
            # Query for complete total (with type adjustment)
            complete_result = conn.execute(text("""
                SELECT COALESCE(SUM(
                    CASE WHEN type = 'deposit' THEN amount 
                         WHEN type = 'withdraw' THEN -amount 
                         ELSE 0 
                    END), 0) as complete_total
                FROM Task
                WHERE status = 'COMPLETE'
                AND updatedAt BETWEEN :start_date AND :end_date
            """), {"start_date": start_date, "end_date": end_date})
            complete_total = complete_result.scalar() or 0
            
            # Query for grand total
            grand_result = conn.execute(text("""
                SELECT COALESCE(SUM(amount), 0) as grand_total
                FROM Task
                WHERE status IN ('PENDING', 'COMPLETE')
                AND updatedAt BETWEEN :start_date AND :end_date
            """), {"start_date": start_date, "end_date": end_date})
            grand_total = grand_result.scalar() or 0
            
            return {
                "pending_total": pending_total,
                "complete_total": complete_total, 
                "grand_total": grand_total
            }
    except Exception as e:
        logger.error(f"Error retrieving task totals: {str(e)}")
        raise

def get_transactions2(bank_id, date_range=None):
    try:
        with engine.connect() as conn:
            BATCH_SIZE = 1000
            all_transactions = []
            offset = 0
            
            # Base query
            query = """
                SELECT t.amount, t.type, t.name, t.status, t.updatedAt, t.reason, b.code,c.bankAccountName
                FROM Task AS t
                LEFT JOIN Branch AS b ON t.branchId = b.id
                LEFT JOIN WithdrawBank AS c ON t.id = c.taskId
                WHERE t.bankId =  :bank_id
            """
        
            
            # Add date filter if provided
            params = {"bank_id": bank_id}
            if date_range:
                start_date, end_date = date_range
                query += " AND (t.updatedAt BETWEEN :start_date AND :end_date or t.status IN ('PENDING', 'ADMIN_PENDING')  )"
                params["start_date"] = start_date
                params["end_date"] = end_date
                
            query += " ORDER BY t.updatedAt DESC LIMIT :limit OFFSET :offset"
            
            while True:
                params["limit"] = BATCH_SIZE
                params["offset"] = offset
                
                result = conn.execute(text(query), params)
                
                batch = result.fetchall()
                if not batch:
                    break
                    
                all_transactions.extend(batch)
                offset += BATCH_SIZE
                
                if len(batch) < BATCH_SIZE:
                    break
            
            logger.info(f"Retrieved {len(all_transactions)} transactions for bank_id {bank_id}")
            return all_transactions
    except Exception as e:
        logger.error(f"Error retrieving transactions for bank_id {bank_id}: {str(e)}")
        raise

def create_task(task_data):
    from sqlalchemy import text

    with engine.begin() as conn:  # 开启事务
        bank_id = task_data["bankId"]
        amount = task_data["amount"]
        task_type = task_data["type"]

        if task_type == "WITHDRAW":
            # ✅ 允许负数，直接扣款
            conn.execute(
                text("UPDATE Bank SET balance = balance - :amount WHERE id = :bank_id"),
                {"amount": amount, "bank_id": bank_id}
            )
        elif task_type == "DEPOSIT":
            # 加钱
            conn.execute(
                text("UPDATE Bank SET balance = balance + :amount WHERE id = :bank_id"),
                {"amount": amount, "bank_id": bank_id}
            )

        # 插入任务记录
        conn.execute(text("""
            INSERT INTO Task (id, bankId, amount, type, status, updatedAt)
            VALUES (:id, :bankId, :amount, :type, :status, NOW())
        """), task_data)