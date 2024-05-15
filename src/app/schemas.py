from pydantic import BaseModel
from datetime import datetime, date


class EmployeeLeave(BaseModel):
    empId: int
    firstName: str
    lastName: str
    total_leave_days: int


class LeaveBalance(BaseModel):
    empId: int
    firstName: str
    lastName: str
    defaultDays: int
    transferabledays: int
    leaveDays: int
    leave_balance: int


class LeaveTrend(BaseModel):
    month: int
    year: int
    leave_count: int


class LeaveDistribution(BaseModel):
    leavetypename: str
    leave_count: int


class FiscalYearTrend(BaseModel):
    fiscal_id: int
    fiscal_start_date: datetime
    fiscal_end_date: datetime
    leave_count: int


class FiscalYearLeaveTypeTrend(BaseModel):
    fiscal_id: int
    fiscal_start_date: datetime
    fiscal_end_date: datetime
    leavetypename: str
    leave_count: int


class DepartmentLeaveDistribution(BaseModel):
    departmentDescription: str
    leaveTypeName: str
    leave_count: int


class DepartmentLeaveStatusCount(BaseModel):
    departmentDescription: str
    approved: int
    rejected: int
    requested: int
    cancelled: int


class MostFrequentLeaveReason(BaseModel):
    reason: str
    request_count: int


class LeaveConversionCount(BaseModel):
    conversion_count: int