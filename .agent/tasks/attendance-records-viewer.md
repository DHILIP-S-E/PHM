---
title: Implement Attendance Records Viewing and Summary
status: pending
priority: medium
created: 2026-01-15
---

# Attendance Records Viewing and Summary Feature

## Objective
Implement a comprehensive attendance records viewing system that allows users to see previously marked attendance records and view summary reports.

## Current Status
- ✅ Attendance marking functionality exists
- ✅ Backend API endpoint exists: `GET /api/v1/employees/attendance/{employee_id}`
- ❌ Frontend doesn't load existing attendance records
- ❌ Summary view is not implemented (just a toggle button exists)

## Requirements

### 1. Load Existing Attendance Records
**File:** `src/pages/AttendanceManagement.tsx`

**Changes needed:**
- Modify `loadAttendanceForDate()` to fetch existing attendance from the backend
- For each employee, call the attendance API to get their records for the selected date
- Pre-populate the form with existing data if attendance was already marked
- Only initialize with default values if no record exists

**API Endpoint to use:**
```typescript
GET /api/v1/employees/attendance/{employee_id}?month={month}&year={year}
```

### 2. Implement Summary View
**File:** `src/pages/AttendanceManagement.tsx`

**Features needed:**
- Monthly attendance summary table
- Show all employees with their attendance for the selected month
- Color-coded attendance status (Present, Absent, Half Day, Leave)
- Calculate statistics:
  - Total working days
  - Days present per employee
  - Attendance percentage
  - Total hours worked

**UI Components:**
- Calendar-style view or grid showing dates
- Employee list with attendance status for each day
- Filters: by department, by date range
- Export functionality (optional)

### 3. Add API Service Method
**File:** `src/services/api.ts`

**Add method:**
```typescript
getAttendance: (employeeId: string, params?: { month?: number, year?: number }) => 
  api.get(`/employees/attendance/${employeeId}`, { params })
```

### 4. Prevent Duplicate Attendance Marking
**Current behavior:** Backend returns 400 if attendance already exists for a date

**Required changes:**
- When loading attendance for a date, check if records exist
- If records exist, show them in edit mode with a clear indicator
- Show a warning/info message: "Attendance already marked for this date. You are editing existing records."
- Add a "View Only" mode option

### 5. Enhanced Features (Optional)
- [ ] Bulk attendance actions (mark all present/absent)
- [ ] Copy previous day's attendance
- [ ] Attendance patterns (weekends auto-marked as leave)
- [ ] Generate attendance reports (PDF/Excel)
- [ ] Overtime calculation display
- [ ] Late arrival / early departure tracking

## Implementation Steps

### Step 1: Update API Service
1. Add `getAttendance` method to `employeesApi`
2. Update the `markAttendance` to handle both create and update

### Step 2: Fetch Existing Records
1. Create a `loadExistingAttendance()` function
2. For each employee, fetch their attendance record for `selectedDate`
3. Update the attendance state with fetched data
4. Show loading state while fetching

### Step 3: Build Summary View Component
1. Create a new component or section for summary view
2. Fetch attendance data for the selected month
3. Display in a calendar or table format
4. Add statistics cards (total present, absent, etc.)

### Step 4: Add Edit Mode Indicator
1. Add a state to track which records are existing vs new
2. Show visual indicator (badge, icon) for already-marked attendance
3. Add confirmation dialog before updating existing records

### Step 5: Testing
1. Test marking attendance for the first time
2. Test loading and viewing existing attendance
3. Test editing existing attendance
4. Test summary view with different date ranges
5. Test with multiple employees and departments

## API Endpoints Available

### Mark Attendance (POST)
```
POST /api/v1/employees/attendance
Body: {
  employee_id: string,
  date: string (YYYY-MM-DD),
  status: 'present' | 'absent' | 'half_day' | 'leave',
  check_in?: string (ISO datetime),
  check_out?: string (ISO datetime),
  notes?: string
}
```

### Get Attendance Records (GET)
```
GET /api/v1/employees/attendance/{employee_id}
Query params:
  - month?: number
  - year?: number
  
Response: {
  employee_id: string,
  employee_name: string,
  attendance: Array<{
    id: string,
    date: string,
    status: string,
    check_in: string | null,
    check_out: string | null,
    working_hours: number,
    notes: string | null
  }>
}
```

## Expected Outcome
- Users can view previously marked attendance records
- The form pre-populates with existing data when available
- Summary view shows monthly attendance overview
- Clear visual distinction between new and existing records
- Smooth user experience with proper loading states and error handling

## Related Files
- `src/pages/AttendanceManagement.tsx` - Main component to update
- `src/services/api.ts` - Add API methods
- `backend/app/api/v1/employees.py` - Backend endpoints (already implemented)

## Notes
- The backend already prevents duplicate attendance for the same date
- Need to handle the 400 error gracefully and show appropriate message
- Consider adding a confirmation dialog before saving changes to existing records
