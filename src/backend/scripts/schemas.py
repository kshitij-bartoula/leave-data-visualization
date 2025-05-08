"""
Defines Pydantic models for various leave-related data.

Imports BaseModel from Pydantic and datetime, date from datetime module.

Models:
- EmployeeLeave: Model for employee leave data.
- LeaveBalance: Model for leave balance data.
- LeaveTrend: Model for leave trend data.
- LeaveDistribution: Model for leave distribution data.
- FiscalYearLeaveTypeTrend: Model for leave trends by fiscal year and leave type.
- DepartmentLeaveDistribution: Model for leave request distribution by department and leave types.
- DepartmentLeaveStatusCount: Model for leave status count by department.
- MostFrequentLeaveReason: Model for most frequent leave request reasons.
"""

from pydantic import BaseModel
from datetime import datetime, date


class EmployeeLeave(BaseModel):
    empId: int
    firstName: str
    lastName: str
    fiscalId: int
    fiscalStartDate: date
    fiscalEndDate: date
    defaultDays: int
    transferableDays: int
    total_leave_days: int

class EmployeeDetails(BaseModel):
    empId: int
    firstName: str
    lastName: str
    fiscal_start_date: date
    fiscal_end_date: date
    designationName: str
    project_allocation: str

class LeaveTrend(BaseModel):
    month: int
    year: int
    leave_count: int

class FiscalYearLeaveTypeTrend(BaseModel):
    fiscal_id: int
    fiscal_start_date: date
    fiscal_end_date: date
    leavetypename: str
    leave_count: int


class DepartmentLeaveDistribution(BaseModel):
    fiscal_start_date: date
    fiscal_end_date: date
    departmentDescription: str
    leaveTypeName: str
    leave_count: int

class ProjectAllocations(BaseModel):
    name: str
    request_count: int
