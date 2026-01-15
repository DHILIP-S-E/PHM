"""
Transaction Seed Script - Create sample Purchase Requests and Sales for existing shops
Run with: python -m scripts.seed_transactions
"""
import sys
import random
from datetime import datetime, timedelta, date

sys.path.insert(0, '.')

from app.db.database import SessionLocal
from app.db.models import (
    User, Warehouse, MedicalShop, Medicine, Batch, Customer,
    PurchaseRequest, PurchaseRequestItem, PurchaseRequestStatus,
    Invoice, InvoiceItem, InvoiceStatus, PaymentStatus,
    ShopStock, Employee, Attendance, SalaryRecord, AttendanceStatus,
    StockMovement, MovementType, StockAdjustment, Dispatch, DispatchItem,
    DispatchStatus, Return, CustomerFollowup
)

def seed_transactions():
    db = SessionLocal()
    
    try:
        print("🌱 Starting transaction seed...")
        
        # 1. Fetch Dependencies
        print("Fetching existing data...")
        admin = db.query(User).filter(User.email == "admin@pharmaec.com").first()
        medicines = db.query(Medicine).all()
        shops = db.query(MedicalShop).all()
        warehouses = db.query(Warehouse).all()
        customers = db.query(Customer).all()
        
        if not all([admin, medicines, shops, warehouses]):
            print("❌ Critical data (Users/Medicines/Shops/Warehouses) missing. Run seed_data.py first or manually add them.")
            return

        print(f"  Found {len(shops)} shops, {len(medicines)} medicines.")
        
        # 1.5 Create Customers if missing
        if not customers:
            print("  No customers found. Creating temporary customers for seeding...")
            customers = []
            for i in range(5):
                cust = Customer(
                    name=f"Walk-in Customer {i+1}",
                    phone=f"999999990{i}",
                    email=f"customer{i}@example.com",
                    customer_type="regular",
                    shop_id=shops[0].id
                )
                db.add(cust)
                customers.append(cust)
            db.flush()
            print(f"  Created {len(customers)} temporary customers.")

        # 2. Purchase Requests
        print("  Generating Purchase Requests...")
        pr_statuses = [
            PurchaseRequestStatus.PENDING, 
            PurchaseRequestStatus.APPROVED, 
            PurchaseRequestStatus.REJECTED,
            PurchaseRequestStatus.COMPLETED
        ]
        
        pr_count = 0
        for shop in shops:
            # Randomly pick a warehouse
            warehouse = random.choice(warehouses)
            
            # Create 3-5 PRs per shop
            for _ in range(random.randint(3, 5)):
                status = random.choice(pr_statuses)
                created_date = datetime.utcnow() - timedelta(days=random.randint(0, 30))
                
                pr_number = f"PR-{created_date.year}-{random.randint(1000, 99999)}"
                
                pr = PurchaseRequest(
                    request_number=pr_number,
                    shop_id=shop.id,
                    warehouse_id=warehouse.id,
                    urgency=random.choice(["normal", "high", "critical"]),
                    status=status,
                    requested_by=admin.id, # Using admin as requester for simplicity
                    notes=f"Auto-generated request for {shop.name}",
                    created_at=created_date,
                    updated_at=created_date
                )
                
                if status == PurchaseRequestStatus.APPROVED:
                    pr.approved_by = admin.id
                    pr.approval_notes = "Auto-approved by system seed"
                
                db.add(pr)
                db.flush()
                
                # Add 2-5 items per PR
                for _ in range(random.randint(2, 5)):
                    med = random.choice(medicines)
                    qty = random.randint(10, 100)
                    
                    item = PurchaseRequestItem(
                        purchase_request_id=pr.id,
                        medicine_id=med.id,
                        quantity_requested=qty,
                        quantity_approved=qty if status in [PurchaseRequestStatus.APPROVED, PurchaseRequestStatus.COMPLETED] else 0,
                        notes="Refill stock"
                    )
                    db.add(item)
                
                pr_count += 1
                
        print(f"  Created {pr_count} Purchase Requests.")

        # 3. Sales (Invoices)
        print("  Generating Sales (Invoices)...")
        invoice_count = 0
        
        for shop in shops:
            # Create 10-15 invoices per shop scattered over 45 days
            for _ in range(random.randint(10, 15)):
                customer = random.choice(customers)
                sale_date = datetime.utcnow() - timedelta(days=random.randint(0, 45))
                
                inv_number = f"INV-{shop.code}-{random.randint(10000, 99999)}"
                
                invoice = Invoice(
                    invoice_number=inv_number,
                    shop_id=shop.id,
                    customer_id=customer.id,
                    payment_method=random.choice(["cash", "card", "upi"]),
                    status=InvoiceStatus.COMPLETED,
                    payment_status=PaymentStatus.COMPLETED,
                    billed_by=admin.id, # Using admin as chiller
                    notes="Walk-in customer",
                    created_at=sale_date
                )
                db.add(invoice)
                db.flush()
                
                # Add 1-4 items per Invoice
                total_amount = 0
                tax_amount = 0
                subtotal_amount = 0
                
                for _ in range(random.randint(1, 4)):
                    med = random.choice(medicines)
                    
                    # Need a batch for invoice item
                    # Try to find existing batch for this med, or pick any batch
                    batch = db.query(Batch).filter(Batch.medicine_id == med.id).first()
                    if not batch:
                        continue
                        
                    qty = random.randint(1, 5)
                    unit_price = med.mrp
                    
                    item_subtotal = qty * unit_price
                    item_tax = item_subtotal * (med.gst_rate / 100)
                    item_total = item_subtotal + item_tax
                    
                    inv_item = InvoiceItem(
                        invoice_id=invoice.id,
                        medicine_id=med.id,
                        batch_id=batch.id,
                        quantity=qty,
                        unit_price=unit_price,
                        tax_percent=med.gst_rate,
                        subtotal=item_subtotal,
                        tax_amount=item_tax,
                        total=item_total
                    )
                    db.add(inv_item)
                    
                    subtotal_amount += item_subtotal
                    tax_amount += item_tax
                    total_amount += item_total

                # Update invoice totals
                invoice.subtotal = subtotal_amount
                invoice.tax_amount = tax_amount
                invoice.total_amount = total_amount
                invoice.paid_amount = total_amount
                invoice.balance_amount = 0
                
                invoice_count += 1
                
        print(f"  Created {invoice_count} Invoices.")

        # 4. HR (Attendance & Salary)
        print("  Generating HR Data (Attendance & Salary)...")
        employees = db.query(Employee).all()
        if employees:
            today = date.today()
            # Attendance for last 30 days
            for emp in employees:
                # Attendance
                for i in range(30):
                    day = today - timedelta(days=i)
                    # Skip Sundays
                    if day.weekday() == 6:
                        continue
                        
                    status = random.choice([AttendanceStatus.PRESENT] * 20 + [AttendanceStatus.LEAVE, AttendanceStatus.ABSENT])
                    
                    att = Attendance(
                        employee_id=emp.id,
                        date=day,
                        status=status,
                        check_in=datetime.combine(day, datetime.strptime("09:00", "%H:%M").time()) if status == AttendanceStatus.PRESENT else None,
                        check_out=datetime.combine(day, datetime.strptime("18:00", "%H:%M").time()) if status == AttendanceStatus.PRESENT else None,
                        working_hours=8.0 if status == AttendanceStatus.PRESENT else 0,
                        record_status='locked' if i > 2 else 'draft',
                        submitted_by=admin.id
                    )
                    db.add(att)
                
                # Salary for previous month
                last_month = today.replace(day=1) - timedelta(days=1)
                salary = SalaryRecord(
                    employee_id=emp.id,
                    month=last_month.month,
                    year=last_month.year,
                    basic_salary=emp.basic_salary,
                    hra=emp.basic_salary * 0.4,
                    allowances=2000,
                    deductions=1000,
                    gross_salary=emp.basic_salary * 1.4 + 2000,
                    net_salary=(emp.basic_salary * 1.4 + 2000) - 1000,
                    is_paid=True,
                    paid_at=datetime.utcnow(),
                    payment_ref=f"TXN-{random.randint(10000,99999)}"
                )
                db.add(salary)
            print(f"  Generated attendance and salary for {len(employees)} employees.")
        else:
            print("  No employees found for HR seeding.")

        # 5. Inventory (Stock Movements & Adjustments)
        print("  Generating Inventory Data...")
        # create explicit movements for the sales generated above (simplified)
        invoices = db.query(Invoice).all()[:20] 
        for inv in invoices:
            for item in inv.items:
                move = StockMovement(
                    movement_type=MovementType.OUT,
                    source_type="shop",
                    source_id=inv.shop_id,
                    destination_type="customer",
                    destination_id=inv.customer_id,
                    medicine_id=item.medicine_id,
                    batch_id=item.batch_id,
                    quantity=item.quantity,
                    reference_type="invoice",
                    reference_id=inv.id,
                    created_by=admin.id,
                    created_at=inv.created_at
                )
                db.add(move)
        
        # Stock Adjustments (Loss/Damaged)
        for _ in range(5):
            shop = random.choice(shops)
            med = random.choice(medicines)
            batch = db.query(Batch).filter(Batch.medicine_id == med.id).first()
            if batch:
                adj = StockAdjustment(
                    adjustment_number=f"ABJ-{random.randint(1000,9999)}",
                    location_type="shop",
                    location_id=shop.id,
                    medicine_id=med.id,
                    batch_id=batch.id,
                    adjustment_type="damage",
                    quantity=random.randint(1, 5),
                    reason="Damaged during handling",
                    adjusted_by=admin.id,
                    status="approved",
                    created_at=datetime.utcnow()
                )
                db.add(adj)
                
                # Add corresponding movement
                move = StockMovement(
                    movement_type=MovementType.OUT,
                    source_type="shop",
                    source_id=shop.id,
                    destination_type="adjustment",
                    medicine_id=med.id,
                    batch_id=batch.id,
                    quantity=adj.quantity,
                    reference_type="adjustment",
                    reference_id=adj.id,
                    created_by=admin.id
                )
                db.add(move)
        print("  Generated inventory movements and adjustments.")

        # 6. Logistics (Dispatches)
        print("  Generating Dispatches...")
        approved_prs = db.query(PurchaseRequest).filter(PurchaseRequest.status == PurchaseRequestStatus.APPROVED).all()
        for pr in approved_prs:
            # Check if dispatch exists
            if db.query(Dispatch).filter(Dispatch.purchase_request_id == pr.id).first():
                continue

            dispatch = Dispatch(
                dispatch_number=f"DIS-{pr.request_number}",
                warehouse_id=pr.warehouse_id,
                shop_id=pr.shop_id,
                purchase_request_id=pr.id,
                status=DispatchStatus.DELIVERED,
                dispatched_by=admin.id,
                received_by=admin.id, # simplifiction
                dispatched_at=datetime.utcnow() - timedelta(days=2),
                delivered_at=datetime.utcnow(),
                notes="Auto-dispatch"
            )
            db.add(dispatch)
            db.flush()
            
            for item in pr.items:
                # Need batch for dispatch
                batch = db.query(Batch).filter(Batch.medicine_id == item.medicine_id).first()
                if not batch: continue
                
                d_item = DispatchItem(
                    dispatch_id=dispatch.id,
                    medicine_id=item.medicine_id,
                    batch_id=batch.id,
                    quantity=item.quantity_approved
                )
                db.add(d_item)
        print(f"  Generated {len(approved_prs)} dispatches.")

        # 7. CRM & Returns
        print("  Generating CRM & Returns...")
        # Returns
        completed_invoices = db.query(Invoice).filter(Invoice.status == InvoiceStatus.COMPLETED).all()
        if completed_invoices:
            # Return 2 random invoices
            for invoice in random.sample(completed_invoices, min(len(completed_invoices), 2)):
                if db.query(Return).filter(Return.invoice_id == invoice.id).first():
                    continue

                ret = Return(
                    return_number=f"RET-{invoice.invoice_number}",
                    invoice_id=invoice.id,
                    shop_id=invoice.shop_id,
                    customer_id=invoice.customer_id,
                    total_refund=100.0, # dummy
                    reason="Customer unsatisfied",
                    status="completed"
                )
                db.add(ret)
        
        # CRM Followups
        if customers:
            for _ in range(5):
                cust = random.choice(customers)
                followup = CustomerFollowup(
                    customer_id=cust.id,
                    followup_type="call",
                    scheduled_date=date.today() + timedelta(days=random.randint(1, 7)),
                    status="pending",
                    notes="Follow up on prescription refill",
                    created_by=admin.id
                )
                db.add(followup)

        # 8. Expiry Warning
        print("  Generating Expiry Data...")
        if medicines:
            med = medicines[0]
            # Create a batch expiring next week
            exp_batch = Batch(
                medicine_id=med.id,
                batch_number=f"EXP-{random.randint(100,999)}",
                manufacturing_date=date.today() - timedelta(days=360),
                expiry_date=date.today() + timedelta(days=5), # Expires in 5 days
                quantity=50,
                purchase_price=med.purchase_price,
                mrp=med.mrp,
                supplier="Seed Supply Co"
            )
            db.add(exp_batch)
            db.flush()
            
            # Add to shop stock so it shows in reports
            sh_stock = ShopStock(
                shop_id=shops[0].id,
                medicine_id=med.id,
                batch_id=exp_batch.id,
                quantity=50
            )
            db.add(sh_stock)

        print("  Values seeded.")
        print("  Values seeded.")
        
        db.commit()
        print("✅ Transactions seeded successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding transactions: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_transactions()
