"""
This module defines FastAPI endpoints to retrieve various leave-related data from the database.

Endpoints:
- /employee_leave: Retrieve total leave days per employee.
- /leave_trend: Retrieve leave trends by month.
- /leave_distribution: Retrieve leave distribution by leave type.
- /fiscal_year_leave_type_trend: Retrieve leave trends by fiscal year and leave type.
- /department_leave_distribution: Retrieve leave request distribution by department and leave types.
- /department_leave_status_count: Retrieve leave status count by department.
- /most_frequent_leave_reason: Retrieve most frequent leave request reasons.

"""

from typing import List
from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlalchemy import create_engine
from .database import SessionLocal, get_db
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import func
from .schemas import (
    EmployeeLeave,
    LeaveBalance,
    LeaveTrend,
    LeaveDistribution,
    FiscalYearLeaveTypeTrend,
    DepartmentLeaveDistribution,
    DepartmentLeaveStatusCount,
    MostFrequentLeaveReason,
)
from utils.db_utils import get_result_from_query

router = APIRouter()

# FastAPI endpoints
@router.get("/employee_leave", response_model=List[EmployeeLeave])
def get_employee_leave(db: Session = Depends(get_db)):
    try:
        query = "SELECT * FROM dw.total_leave_days_per_employee_mv"
        result = get_result_from_query(query)

        # Transform the raw database result into EmployeeLeave objects
        employee_leave = []
        for empId, firstName, lastName, total_leave_days in result:
            employee_leave.append(EmployeeLeave(
                empId=empId,
                firstName=firstName,
                lastName=lastName,
                total_leave_days=total_leave_days,
            ))

        return employee_leave
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error occurred{e}")

@router.get("/leave_balance", response_model=List[LeaveBalance])
def get_leave_balance(db: Session = Depends(get_db)):
    try:
        query = "SELECT * FROM dw.leave_balances_per_employee_mv"
        result = get_result_from_query(query)

        # Transform the raw database result into LeaveBalance objects
        leave_balances = []
        for row in result:
            leave_balances.append(LeaveBalance(
                empId=row.empId,
                firstName=row.firstName,
                lastName=row.lastName,
                defaultDays=row.defaultDays,
                transferabledays=row.transferabledays,
                leaveDays=row.leaveDays,
                leave_balance=row.leave_balance,
            ))

        return leave_balances
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error occurred{e}")

@router.get("/leave_trend", response_model=List[LeaveTrend])
def get_leave_trend(db: Session = Depends(get_db)):
    try:
        query = "SELECT * FROM dw.leave_trends_by_month_mv"
        result = get_result_from_query(query)

        # Transform the raw database result into LeaveTrend objects
        leave_trends = []
        for row in result:
            leave_trends.append(LeaveTrend(
                month=row.month,
                year=row.year,
                leave_count=row.leave_count,
            ))

        return leave_trends
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error occurred{e}")

@router.get("/leave_distribution", response_model=List[LeaveDistribution])
def get_leave_distribution(db: Session = Depends(get_db)):
    try:
        query = "SELECT * FROM dw.leave_distribution_by_leave_type_mv"
        result = get_result_from_query(query)

        leave_distributions = []
        for leave_type_name, leave_count in result:
            leave_distribution = LeaveDistribution(
                leavetypename=leave_type_name, leave_count=leave_count
            )
            leave_distributions.append(leave_distribution)
        return leave_distributions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error occurred{e}")

@router.get("/fiscal_year_leave_type_trend", response_model=List[FiscalYearLeaveTypeTrend])
def get_fiscal_year_leave_type_trend(db: Session = Depends(get_db)):
    try:
        query = "SELECT * FROM dw.leave_trend_by_fiscal_year_per_leave_type_mv"
        result = get_result_from_query(query)

        fiscal_year_leave_type_trends = []
        for fiscal_id, fiscal_start_date, fiscal_end_date, leavetypename, leave_count in result:
            fiscal_year_leave_type_trend = FiscalYearLeaveTypeTrend(
                fiscal_id=fiscal_id,
                fiscal_start_date=fiscal_start_date,
                fiscal_end_date=fiscal_end_date,
                leavetypename=leavetypename,
                leave_count=leave_count,
            )
            fiscal_year_leave_type_trends.append(fiscal_year_leave_type_trend)
        return fiscal_year_leave_type_trends
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error occurred{e}")


@router.get("/department_leave_distribution", response_model=List[DepartmentLeaveDistribution])
def get_department_leave_distribution(db: Session = Depends(get_db)):
    try:
        query = "SELECT * FROM dw.leave_request_distribution_by_department_and_leave_types_mv"
        result = get_result_from_query(query)

        department_leave_distributions = []
        for departmentDescription, leavetypename, leave_count in result:
            department_leave_distribution = DepartmentLeaveDistribution(
                departmentDescription=departmentDescription,
                leaveTypeName=leavetypename,
                leave_count=leave_count,
            )
            department_leave_distributions.append(department_leave_distribution)
        return department_leave_distributions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error occurred{e}")


@router.get("/department_leave_status_count", response_model=List[DepartmentLeaveStatusCount])
def get_department_leave_status_count(db: Session = Depends(get_db)):
    try:
        query = "SELECT * FROM dw.leave_status_count_by_department_mv"
        result = get_result_from_query(query)

        department_leave_status_counts = []
        for departmentDescription, approved, rejected, requested, cancelled in result:
            department_leave_status_count = DepartmentLeaveStatusCount(
                departmentDescription=departmentDescription,
                approved=approved,
                rejected=rejected,
                requested=requested,
                cancelled=cancelled,
            )
            department_leave_status_counts.append(department_leave_status_count)
        return department_leave_status_counts
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error occurred{e}")

@router.get("/most_frequent_leave_reason", response_model=List[MostFrequentLeaveReason])
def get_most_frequent_leave_reason(db: Session = Depends(get_db)):
    try:
        query = "SELECT * FROM dw.most_frequent_leave_request_reasons_mv"
        result = get_result_from_query(query)

        most_frequent_leave_reasons = []
        for reason, request_count in result:
            most_frequent_leave_reason = MostFrequentLeaveReason(
                reason=reason,
                request_count=request_count
            )
            most_frequent_leave_reasons.append(most_frequent_leave_reason)
        return most_frequent_leave_reasons
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error occurred{e}")

# from fastapi import FastAPI, APIRouter, Depends, HTTPException, BackgroundTasks
# from sqlalchemy.orm import Session
# from typing import List
# import asyncio
# import time
# from .database import get_db
# from .schemas import (
#     EmployeeLeave,
#     LeaveBalance,
#     LeaveTrend,
#     LeaveDistribution,
#     FiscalYearLeaveTypeTrend,
#     DepartmentLeaveDistribution,
#     MostFrequentLeaveReason,
# )
# from utils.db_utils import get_result_from_query


# router = APIRouter()

# # In-memory cache to store the results
# cache = {
#     "employee_leave": [],
#     "leave_balance": [],
#     "leave_trend": [],
#     "leave_distribution": [],
#     "fiscal_year_leave_type_trend": [],
#     "department_leave_distribution": [],
# }

# # Function to refresh data every minute
# async def refresh_data():
#     while True:
#         print("Refreshing data...")
#         try:
#             db: Session = next(get_db())

#             # Update employee_leave
#             query = "SELECT * FROM dw.total_leave_days_per_employee_mv"
#             result = get_result_from_query(query)
#             cache["employee_leave"] = [EmployeeLeave(
#                 empId=empId,
#                 firstName=firstName,
#                 lastName=lastName,
#                 total_leave_days=total_leave_days,
#             ) for empId, firstName, lastName, total_leave_days in result]

#             # Update leave_balance
#             query = "SELECT * FROM dw.leave_balances_per_employee_mv"
#             result = get_result_from_query(query)
#             cache["leave_balance"] = [LeaveBalance(
#                 empId=row.empId,
#                 firstName=row.firstName,
#                 lastName=row.lastName,
#                 defaultDays=row.defaultDays,
#                 transferabledays=row.transferabledays,
#                 leaveDays=row.leaveDays,
#                 leave_balance=row.leave_balance,
#             ) for row in result]

#             # Update leave_trend
#             query = "SELECT * FROM dw.leave_trends_by_month_mv"
#             result = get_result_from_query(query)
#             cache["leave_trend"] = [LeaveTrend(
#                 month=row.month,
#                 year=row.year,
#                 leave_count=row.leave_count,
#             ) for row in result]

#             # Update leave_distribution
#             query = "SELECT * FROM dw.leave_distribution_by_leave_type_mv"
#             result = get_result_from_query(query)
#             cache["leave_distribution"] = [LeaveDistribution(
#                 leavetypename=leave_type_name, leave_count=leave_count
#             ) for leave_type_name, leave_count in result]

#             # Update fiscal_year_leave_type_trend
#             query = "SELECT * FROM dw.leave_trend_by_fiscal_year_per_leave_type_mv"
#             result = get_result_from_query(query)
#             cache["fiscal_year_leave_type_trend"] = [FiscalYearLeaveTypeTrend(
#                 fiscal_id=fiscal_id,
#                 fiscal_start_date=fiscal_start_date,
#                 fiscal_end_date=fiscal_end_date,
#                 leavetypename=leavetypename,
#                 leave_count=leave_count,
#             ) for fiscal_id, fiscal_start_date, fiscal_end_date, leavetypename, leave_count in result]

#             # Update department_leave_distribution
#             query = "SELECT * FROM dw.leave_distribution_by_department_mv"
#             result = get_result_from_query(query)
#             cache["department_leave_distribution"] = [DepartmentLeaveDistribution(
#                 department_name=department_name,
#                 leave_type=leave_type,
#                 leave_count=leave_count,
#             ) for department_name, leave_type, leave_count in result]

#         except Exception as e:
#             print(f"Failed to refresh data: {e}")

#         await asyncio.sleep(60)  # Wait for 1 minute before next refresh

# async def startup_event():
#     # Start the background task to refresh data
#     await refresh_data()

# @router.get("/employee_leave", response_model=List[EmployeeLeave])
# def get_employee_leave():
#     return cache["employee_leave"]

# @router.get("/leave_balance", response_model=List[LeaveBalance])
# def get_leave_balance():
#     return cache["leave_balance"]

# @router.get("/leave_trend", response_model=List[LeaveTrend])
# def get_leave_trend():
#     return cache["leave_trend"]

# @router.get("/leave_distribution", response_model=List[LeaveDistribution])
# def get_leave_distribution():
#     return cache["leave_distribution"]

# @router.get("/most_frequent_leave_reason", response_model=List[MostFrequentLeaveReason])
# def get_leave_distribution():
#     return cache["most_frequent_leave_reason"]