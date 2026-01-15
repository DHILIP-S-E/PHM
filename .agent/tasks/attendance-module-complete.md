---
title: Complete Attendance Module Implementation
status: pending
priority: high
created: 2026-01-15
dependencies: 
  - Employee creation system (✅ completed)
  - Basic attendance marking (✅ completed)
---

# Complete Attendance Module - Full System Design

## ✅ Already Implemented (Foundation)

1. **Employee Management**
   - Warehouse Admin can create warehouse employees
   - Pharmacy Admin can create pharmacy employees  
   - Auto-assignment of warehouse_id/shop_id
   - Email optional, master data for departments/designations

2. **Basic Attendance Marking**
   - Day-wise attendance loading (`GET /employees/attendance/daily`)
   - Mark attendance for employees (`POST /employees/attendance`)
   - Entity-based filtering (admins see only their employees)
   - Load existing attendance records

## 🎯 Module Structure

```
📋 Attendance (Sidebar)
├── Attendance Marker (Daily Marking)
└── Attendance Report (View & Analysis)
```

## 1️⃣ ATTENDANCE MARKER (Daily Operation)

### Current Status
- ✅ Basic functionality working
- ❌ Needs UX/business logic improvements

### Requirements

#### A. Date & Entity Selection
- [x] Default to today's date
- [ ] Lock past dates (read-only except Super Admin)
- [ ] Super Admin can select any entity
- [ ] Admins auto-locked to their entity
- [ ] Show entity name clearly in header

#### B. Employee List Loading
**Logic:**
```python
# Backend filter
employees = db.query(Employee).filter(
    Employee.status == "active",  # Only active
    Employee.warehouse_id == current_user.warehouse_id  # Entity scope
)
```

**Frontend Display:**
- Employee name
- Employee code
- Department
- Designation
- Status dropdown (Present/Absent/Half Day/Leave)

#### C. Default Behavior
- [ ] **Default status = "Absent"** (safe default, not Present)
- [ ] Pre-load existing records if date already marked
- [ ] Visual indicator for already-marked attendance

#### D. Save & Submit Actions
1. **Save (Draft)**
   - Allows partial marking
   - Can edit later
   - No validation

2. **Submit & Lock Day** ⭐ NEW
   - Validates all employees marked
   - Locks the date
   - Creates audit log entry
   - Only Super Admin can unlock

#### E. Validation Rules
- [ ] Cannot mark future dates
- [ ] Cannot mark past dates (except Super Admin)
- [ ] Cannot change submitted dates (except Super Admin)
- [ ] Show warning if not all employees marked

#### F. UI Enhancements
- [ ] Bulk actions: "Mark All Present/Absent"
- [ ] Filter by department
- [ ] Search employees
- [ ] Statistics: X of Y marked
- [ ] Color coding by status
- [ ] Export daily attendance (Excel/PDF)

## 2️⃣ ATTENDANCE REPORT (View & Analysis)

### Purpose
Read-only view for analysis, accountability, and payroll

### A. Access Control
| Role | Access |
|------|--------|
| Super Admin | All entities, all employees |
| Warehouse Admin | Own warehouse employees only |
| Pharmacy Admin | Own shop employees only |
| Employee | Only self (My Attendance) |

### B. Filter Panel
- [ ] Date range selector
- [ ] Employee dropdown (admins only)
- [ ] Department filter
- [ ] Status filter (Present/Absent/Leave/Half Day)
- [ ] Entity selector (Super Admin only)

### C. View Types

**1. Table View (Default)**
```
Date | Employee | Department | Status | Check-In | Check-Out | Hours | Notes
```

**2. Calendar View (Monthly)**
```
Grid showing each date:
├── Day cell shows: X present, Y absent
└── Click to expand: employee list
```

**3. Summary View**
```
Employee-wise summary for selected period:
├── Total working days
├── Present days
├── Absent days  
├── Leave days
└── Attendance %
```

### D. Statistics Dashboard
- [ ] Total employees
- [ ] Today's attendance %
- [ ] Monthly trend graph
- [ ] Department-wise breakdown
- [ ] Top absentees alert

### E. Export Options
- [ ] Excel export for payroll
- [ ] PDF report
- [ ] Filtered data export
- [ ] Date range export

### F. Employee Self-View ("My Attendance")
- [ ] Calendar view of own attendance
- [ ] Monthly summary card
- [ ] No edit capability
- [ ] Attendance percentage
- [ ] Leave balance (if applicable)

## 3️⃣ BACKEND API ENDPOINTS

### Already Implemented
- ✅ `GET /employees/attendance/daily?date=YYYY-MM-DD` - Get all attendance for a date
- ✅ `POST /employees/attendance` - Mark attendance
- ✅ `GET /employees/attendance/{employee_id}` - Get employee's attendance history

### Required New Endpoints

#### A. Submit & Lock Day
```python
POST /employees/attendance/submit
Body: {
    "date": "2026-01-15",
    "entity_type": "warehouse",
    "entity_id": "xxx"
}
Response: {
    "locked": true,
    "submitted_by": "user_id",
    "submitted_at": "timestamp"
}
```

#### B. Unlock Day (Super Admin)
```python
POST /employees/attendance/unlock
Body: {
    "date": "2026-01-15",
    "reason": "Correction needed"
}
```

#### C. Attendance Report
```python
GET /employees/attendance/report
Params:
    - date_from: YYYY-MM-DD
    - date_to: YYYY-MM-DD
    - employee_id: optional
    - department: optional
    - status: optional
Response: {
    "summary": {...},
    "records": [...],
    "stats": {...}
}
```

#### D. Bulk Mark
```python
POST /employees/attendance/bulk
Body: {
    "date": "2026-01-15",
    "employee_ids": ["id1", "id2"],
    "status": "present"
}
```

#### E. My Attendance (Employee)
```python
GET /employees/attendance/my
Params:
    - month: 1-12
    - year: 2026
Response: {
    "employee_id": "xxx",
    "month_summary": {...},
    "attendance": [...]
}
```

## 4️⃣ DATABASE CHANGES

### New Fields in `attendance` Table
```sql
ALTER TABLE attendance ADD COLUMN:
- is_locked BOOLEAN DEFAULT FALSE
- locked_by VARCHAR(36)
- locked_at TIMESTAMP
- submitted_by VARCHAR(36)
- submitted_at TIMESTAMP
```

### New Table: `attendance_locks`
```sql
CREATE TABLE attendance_locks (
    id VARCHAR(36) PRIMARY KEY,
    date DATE NOT NULL,
    entity_type VARCHAR(20) NOT NULL,
    entity_id VARCHAR(36) NOT NULL,
    is_locked BOOLEAN DEFAULT TRUE,
    locked_by VARCHAR(36),
    locked_at TIMESTAMP,
    unlocked_by VARCHAR(36),
    unlocked_at TIMESTAMP,
    unlock_reason TEXT,
    UNIQUE(date, entity_type, entity_id)
)
```

## 5️⃣ PERMISSIONS MATRIX

### Attendance Marker
| Action | Super Admin | Warehouse Admin | Pharmacy Admin | Employee |
|--------|-------------|-----------------|----------------|----------|
| View marker | ✅ All entities | ✅ Own warehouse | ✅ Own shop | ❌ |
| Mark attendance | ✅ | ✅ | ✅ | ❌ |
| Submit & lock | ✅ | ✅ | ✅ | ❌ |
| Unlock day | ✅ | ❌ | ❌ | ❌ |
| Edit past dates | ✅ | ❌ | ❌ | ❌ |

### Attendance Report
| View Type | Super Admin | Warehouse Admin | Pharmacy Admin | Employee |
|-----------|-------------|-----------------|----------------|----------|
| All employees | ✅ All | ✅ Own entity | ✅ Own entity | ❌ |
| My attendance | ✅ | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ✅ | ❌ |
| Analytics | ✅ | ✅ | ✅ | ❌ |

## 6️⃣ IMPLEMENTATION PLAN

### Phase 1: Core Features (High Priority)
1. ✅ Day-wise attendance loading
2. ✅ Basic attendance marking
3. [ ] Default status = "Absent"
4. [ ] Lock past dates
5. [ ] Submit & lock functionality
6. [ ] Prevent duplicate marking

### Phase 2: Reporting (High Priority)
1. [ ] Create Attendance Report page
2. [ ] Table view with filters
3. [ ] Date range filtering
4. [ ] Employee-wise attendance history
5. [ ] Export to Excel

### Phase 3: Enhanced Features (Medium Priority)
1. [ ] Calendar view
2. [ ] Monthly summary
3. [ ] Bulk actions
4. [ ] Department filtering
5. [ ] Statistics dashboard

### Phase 4: Employee Features (Medium Priority)
1. [ ] "My Attendance" view for employees
2. [ ] Mobile-responsive calendar
3. [ ] Leave balance integration
4. [ ] Attendance percentage display

### Phase 5: Advanced Features (Low Priority)
1. [ ] Super Admin override with audit
2. [ ] Payroll integration
3. [ ] Automated alerts for absenteeism
4. [ ] Trend analysis & charts
5. [ ] Geolocation check-in (optional)

## 7️⃣ UI/UX SPECIFICATIONS

### Attendance Marker Screen
```
┌─────────────────────────────────────────────┐
│ 📋 Attendance Marker                        │
│                                             │
│ Date: [2026-01-15] 📅  Entity: Warehouse A │
│                                             │
│ ⚡ Bulk Actions: [Mark All Present ▼]      │
│                                             │
│ ┌───────────────────────────────────────┐ │
│ │ Employee           Dept     Status    │ │
│ │ ─────────────────────────────────────│ │
│ │ 👤 John Doe (E001) Ops     [Present▼]│ │
│ │ 👤 Jane Smith(E002) Pharm  [Absent ▼]│ │
│ │ ...                                   │ │
│ └───────────────────────────────────────┘ │
│                                             │
│ Status: 8 of 10 marked                     │
│ [Save Draft] [Submit & Lock Day 🔒]       │
└─────────────────────────────────────────────┘
```

### Attendance Report Screen
```
┌─────────────────────────────────────────────┐
│ 📊 Attendance Report                        │
│                                             │
│ 📅 From:[2026-01-01] To:[2026-01-31]      │
│ 👤 Employee: [All ▼]  Dept: [All ▼]       │
│                                             │
│ ┌─── Summary ───────────────────────────┐ │
│ │ Present: 85% | Absent: 10% | Leave: 5%│ │
│ └────────────────────────────────────────┘ │
│                                             │
│ 📋 [Table] [Calendar] [Summary] [Export]   │
│                                             │
│ ┌───────────────────────────────────────┐ │
│ │ Date     Employee    Status   Hours   │ │
│ │ ──────────────────────────────────────│ │
│ │ 15-Jan   John Doe    Present  8.5h    │ │
│ │ 15-Jan   Jane Smith  Absent   0h      │ │
│ └───────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

## 8️⃣ TESTING CHECKLIST

### Functional Tests
- [ ] Warehouse Admin sees only warehouse employees
- [ ] Pharmacy Admin sees only shop employees
- [ ] Employee sees only own attendance
- [ ] Cannot mark future dates
- [ ] Cannot edit locked dates (non-admin)
- [ ] Super Admin can unlock dates
- [ ] Duplicate marking prevented
- [ ] Bulk actions work correctly

### Edge Cases
- [ ] New employee appears in attendance
- [ ] Inactive employee disappears
- [ ] Employee transferred between entities
- [ ] Attendance on holidays
- [ ] Half-day calculation
- [ ] Export with no data

### Performance
- [ ] Load 100+ employees efficiently
- [ ] Report generation for 3 months
- [ ] Bulk marking 50 employees
- [ ] Export large dataset

## 9️⃣ SUCCESS CRITERIA

✅ **Attendance Marker**
- Admins can mark attendance for all employees in <30 seconds
- Default status prevents accidental no-shows
- Submit & lock prevents tampering
- UI is intuitive and fast

✅ **Attendance Report**
- Generate monthly report in <3 seconds
- Export to Excel works flawlessly
- Filters are responsive
- Employees can view their own records

✅ **Security**
- Entity isolation 100% enforced
- Past dates locked properly
- Audit trail for all changes
- Super Admin override logged

## 📚 Related Documentation
- Employee Creation Flow: `.agent/WAREHOUSE_ADMIN_PERMISSIONS.md`
- Current Implementation: `src/pages/AttendanceManagement.tsx`
- API Endpoints: `backend/app/api/v1/employees.py`
- Database Models: `backend/app/db/models.py`

## 🔄 Migration Notes

If moving from current implementation:
1. Keep existing `attendance` table
2. Add new fields for locking
3. Create migration for attendance_locks table
4. Update API to include lock checks
5. Frontend backwards compatible during transition
