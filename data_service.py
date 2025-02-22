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
                    task AS a 
                RIGHT JOIN 
                    bank AS b 
                ON 
                    a.bankId = b.id 
                AND 
                    a.createdAt BETWEEN :start_date AND :end_date
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
                SELECT  a.amount, a.type, a.status, a.createdAt, a.reason,b.code
                FROM 
                    Task as a 
                RIGHT JOIN 
	                branch as b
                ON 
	                a.branchId = b.id
                WHERE bankId = :bank_id
            """
            
            # Add date filter if provided
            params = {"bank_id": bank_id}
            if date_range:
                start_date, end_date = date_range
                query += " AND a.createdAt BETWEEN :start_date AND :end_date"
                params["start_date"] = start_date
                params["end_date"] = end_date
                
            query += " ORDER BY a.createdAt DESC LIMIT :limit OFFSET :offset"
            
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
                    IFNULL(SUM(a.amount), 0) AS total,
                    b.code 
                FROM 
                    task AS a 
                RIGHT JOIN 
                    branch AS b 
                ON 
                    a.branchId = b.id 
                AND a.createdAt BETWEEN :start_date AND :end_date
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
            result = conn.execute(text("""
                SELECT 
                    SUM(CASE WHEN status = 'PENDING' THEN amount ELSE 0 END) as pending_total,
                    SUM(CASE WHEN status = 'COMPLETE' THEN amount ELSE 0 END) as complete_total,
                    SUM(CASE WHEN status IN ('PENDING', 'COMPLETE') THEN amount ELSE 0 END) as grand_total
                FROM 
                    Task 
                WHERE 
                    status IN ('PENDING', 'COMPLETE')
                AND 
                    createdAt BETWEEN :start_date AND :end_date
            """), {"start_date": start_date, "end_date": end_date})
            
            # This will return a single row with the aggregated values
            totals = result.fetchone()
            
            # Return the single row of totals rather than all accounts
            return {
                "pending_total": totals[0] or 0,
                "complete_total": totals[1] or 0, 
                "grand_total": totals[2] or 0
            }
    except Exception as e:
        logger.error(f"Error retrieving task totals: {str(e)}")
        raise