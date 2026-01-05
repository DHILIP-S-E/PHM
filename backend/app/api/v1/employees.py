"""
Employee and HR API Routes - Database Connected
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from datetime import datetime, date

from app.models.employee import (
    EmployeeCreate, EmployeeUpdate, EmployeeResponse, EmployeeListResponse,
    AttendanceCreate, AttendanceResponse, SalaryRecordResponse, ProcessSalaryRequest,
    PerformanceResponse
)
from app.models.common import APIResponse
from app.core.security import get_current_user, require_role
from app.db.database import get_db
from app.db.models import Employee, Attendance, SalaryRecord, AttendanceStatus

router = APIRouter()


def generate_employee_code(db: Session) -> str:
    """Generate unique employee code"""
    count = db.query(func.count(Employee.id)).scalar() or 0
    return f"EMP-{count + 1:04d}"


@router.get("")
async def list_employees(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    department: Optional[str] = None,
    shop_id: Optional[str] = None,
    warehouse_id: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """List all employees"""
    query = db.query(Employee)
    
    if search:
        query = query.filter(
            (Employee.name.ilike(f"%{search}%")) |
            (Employee.email.ilike(f"%{search}%")) |
            (Employee.employee_code.ilike(f"%{search}%"))
        )
    
    if department:
        query = query.filter(Employee.department == department)
    
    if shop_id:
        query = query.filter(Employee.shop_id == shop_id)
    
    if warehouse_id:
        query = query.filter(Employee.warehouse_id == warehouse_id)
    
    if status:
        query = query.filter(Employee.status == status)
    
    total = query.count()
    employees = query.offset((page - 1) * size).limit(size).all()
    
    return {
        "items": [
            {
                "id": e.id,
                "employee_code": e.employee_code,
                "name": e.name,
                "email": e.email,
                "phone": e.phone,
                "designation": e.designation,
                "department": e.department,
                "employment_type": e.employment_type,
                "date_of_joining": e.date_of_joining.isoformat() if e.date_of_joining else None,
                "basic_salary": e.basic_salary,
                "shop_id": e.shop_id,
                "warehouse_id": e.warehouse_id,
                "status": e.status,
                "created_at": e.created_at
            }
            for e in employees
        ],
        "total": total,
        "page": page,
        "size": size
    }


@router.post("")
async def create_employee(
    employee_data: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["super_admin", "hr_manager"]))
):
    """Create a new employee"""
    employee_code = generate_employee_code(db)
    
    employee = Employee(
        employee_code=employee_code,
        name=employee_data.name,
        email=employee_data.email,
        phone=employee_data.phone,
        designation=employee_data.designation,
        department=employee_data.department,
        employment_type=employee_data.employment_type or "full_time",
        date_of_joining=employee_data.date_of_joining,
        date_of_birth=employee_data.date_of_birth,
        gender=employee_data.gender,
        address=employee_data.address,
        city=employee_data.city,
        emergency_contact=employee_data.emergency_contact,
        bank_account=employee_data.bank_account,
        pan_number=employee_data.pan_number,
        pf_number=employee_data.pf_number,
        esi_number=employee_data.esi_number,
        basic_salary=employee_data.basic_salary,
        shop_id=employee_data.shop_id,
        warehouse_id=employee_data.warehouse_id,
        status="active"
    )
    
    db.add(employee)
    db.commit()
    db.refresh(employee)
    
    return APIResponse(
        message="Employee created successfully",
        data={"id": employee.id, "employee_code": employee_code}
    )


@router.get("/{employee_id}")
async def get_employee(
    employee_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get employee by ID"""
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    return {
        "id": employee.id,
        "employee_code": employee.employee_code,
        "user_id": employee.user_id,
        "name": employee.name,
        "email": employee.email,
        "phone": employee.phone,
        "designation": employee.designation,
        "department": employee.department,
        "employment_type": employee.employment_type,
        "date_of_joining": employee.date_of_joining.isoformat() if employee.date_of_joining else None,
        "date_of_birth": employee.date_of_birth.isoformat() if employee.date_of_birth else None,
        "gender": employee.gender,
        "address": employee.address,
        "city": employee.city,
        "emergency_contact": employee.emergency_contact,
        "bank_account": employee.bank_account,
        "pan_number": employee.pan_number,
        "pf_number": employee.pf_number,
        "esi_number": employee.esi_number,
        "basic_salary": employee.basic_salary,
        "shop_id": employee.shop_id,
        "warehouse_id": employee.warehouse_id,
        "status": employee.status,
        "created_at": employee.created_at
    }


@router.put("/{employee_id}")
async def update_employee(
    employee_id: str,
    update_data: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["super_admin", "hr_manager"]))
):
    """Update employee"""
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    update_dict = update_data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(employee, field, value)
    
    db.commit()
    
    return APIResponse(message="Employee updated successfully")


@router.delete("/{employee_id}")
async def delete_employee(
    employee_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["super_admin", "hr_manager"]))
):
    """Delete (deactivate) employee"""
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    employee.status = "terminated"
    db.commit()
    
    return APIResponse(message="Employee terminated successfully")


# ==================== ATTENDANCE ENDPOINTS ====================

@router.post("/attendance")
async def mark_attendance(
    attendance_data: AttendanceCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Mark attendance for an employee"""
    employee = db.query(Employee).filter(Employee.id == attendance_data.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Check if already marked for this date
    existing = db.query(Attendance).filter(
        Attendance.employee_id == attendance_data.employee_id,
        Attendance.date == attendance_data.date
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Attendance already marked for this date")
    
    working_hours = 0.0
    if attendance_data.check_in and attendance_data.check_out:
        delta = attendance_data.check_out - attendance_data.check_in
        working_hours = delta.total_seconds() / 3600
    
    attendance = Attendance(
        employee_id=attendance_data.employee_id,
        date=attendance_data.date,
        status=AttendanceStatus(attendance_data.status) if attendance_data.status else AttendanceStatus.PRESENT,
        check_in=attendance_data.check_in,
        check_out=attendance_data.check_out,
        working_hours=working_hours,
        notes=attendance_data.notes
    )
    
    db.add(attendance)
    db.commit()
    db.refresh(attendance)
    
    return APIResponse(
        message="Attendance marked successfully",
        data={"id": attendance.id, "working_hours": working_hours}
    )


@router.get("/attendance/{employee_id}")
async def get_employee_attendance(
    employee_id: str,
    month: Optional[int] = None,
    year: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get attendance records for an employee"""
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    query = db.query(Attendance).filter(Attendance.employee_id == employee_id)
    
    if month and year:
        query = query.filter(
            func.extract('month', Attendance.date) == month,
            func.extract('year', Attendance.date) == year
        )
    
    attendance = query.order_by(Attendance.date.desc()).all()
    
    return {
        "employee_id": employee_id,
        "employee_name": employee.name,
        "attendance": [
            {
                "id": a.id,
                "date": a.date.isoformat() if a.date else None,
                "status": a.status.value if a.status else "present",
                "check_in": a.check_in.isoformat() if a.check_in else None,
                "check_out": a.check_out.isoformat() if a.check_out else None,
                "working_hours": a.working_hours,
                "notes": a.notes
            }
            for a in attendance
        ]
    }


# ==================== SALARY ENDPOINTS ====================

@router.get("/salary/{employee_id}")
async def get_employee_salary(
    employee_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get salary records for an employee"""
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    salaries = db.query(SalaryRecord).filter(
        SalaryRecord.employee_id == employee_id
    ).order_by(SalaryRecord.year.desc(), SalaryRecord.month.desc()).all()
    
    return {
        "employee_id": employee_id,
        "employee_name": employee.name,
        "salary_records": [
            {
                "id": s.id,
                "month": s.month,
                "year": s.year,
                "basic_salary": s.basic_salary,
                "hra": s.hra,
                "allowances": s.allowances,
                "deductions": s.deductions,
                "pf_deduction": s.pf_deduction,
                "esi_deduction": s.esi_deduction,
                "tax_deduction": s.tax_deduction,
                "bonus": s.bonus,
                "gross_salary": s.gross_salary,
                "net_salary": s.net_salary,
                "is_paid": s.is_paid,
                "paid_at": s.paid_at
            }
            for s in salaries
        ]
    }


@router.post("/salary/process")
async def process_salary(
    request: ProcessSalaryRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["super_admin", "hr_manager"]))
):
    """Process salary for employees"""
    query = db.query(Employee).filter(Employee.status == "active")
    
    if request.employee_ids:
        query = query.filter(Employee.id.in_(request.employee_ids))
    
    employees = query.all()
    processed = []
    
    for employee in employees:
        # Check if already processed
        existing = db.query(SalaryRecord).filter(
            SalaryRecord.employee_id == employee.id,
            SalaryRecord.month == request.month,
            SalaryRecord.year == request.year
        ).first()
        
        if existing:
            continue
        
        basic = employee.basic_salary
        hra = basic * 0.4
        allowances = basic * 0.2
        pf = basic * 0.12
        gross = basic + hra + allowances
        net = gross - pf
        
        salary = SalaryRecord(
            employee_id=employee.id,
            month=request.month,
            year=request.year,
            basic_salary=basic,
            hra=hra,
            allowances=allowances,
            pf_deduction=pf,
            gross_salary=gross,
            net_salary=net
        )
        
        db.add(salary)
        processed.append(employee.id)
    
    db.commit()
    
    return APIResponse(
        message=f"Processed salary for {len(processed)} employees",
        data={"processed_count": len(processed)}
    )


@router.get("/performance/{employee_id}")
async def get_employee_performance(
    employee_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get performance records for an employee"""
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Performance would need a separate table - returning placeholder for now
    return {
        "employee_id": employee_id,
        "employee_name": employee.name,
        "performance": []
    }
