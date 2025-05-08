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
    EmployeeDetails,
    LeaveTrend,
    FiscalYearLeaveTypeTrend,
    DepartmentLeaveDistribution,
    ProjectAllocations,
)
from utils.db_utils import get_result_from_query

router = APIRouter()

# Define FastAPI endpoints
@router.get("/employee_leave_details", response_model=List[EmployeeLeave])
def get_employee_leave(db: Session = Depends(get_db)):
    try:
        query = "SELECT * FROM dw.total_leave_days_per_employee_mv"
        result = get_result_from_query(query, db)

        # Transform the raw database result into EmployeeLeave objects
        employee_leave = []
        for empId, firstName, lastName,fiscalId, fiscalStartDate, fiscalEndDate, defaultDays, transferableDays, total_leave_days in result:
            employee_leave.append(EmployeeLeave(
                empId=empId,
                firstName=firstName,
                lastName=lastName,
                fiscalId=fiscalId,
                fiscalStartDate=fiscalStartDate,
                fiscalEndDate=fiscalEndDate,
                defaultDays=defaultDays,
                transferableDays=transferableDays,
                total_leave_days=total_leave_days,
            ))

        return employee_leave
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error occurred{e}")

@router.get("/employee_HR_details", response_model=List[EmployeeDetails])
def get_employee_details(db: Session = Depends(get_db)):
    try:
        query = "SELECT * FROM dw.employee_details_mv"
        result = get_result_from_query(query, db)

        # Transform the raw database result into EmployeeLeave objects
        employee_details = []
        for empId, firstName, lastName, fiscal_start_date, fiscal_end_date, designationName, project_allocation in result:
            employee_details.append(EmployeeDetails(
                empId=empId,
                firstName=firstName,
                lastName=lastName,
                fiscal_start_date = fiscal_start_date,
                fiscal_end_date = fiscal_end_date,
                designationName = designationName,
                project_allocation = project_allocation,
            ))

        return employee_details
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error occurred{e}")

@router.get("/leave_trend", response_model=List[LeaveTrend])
def get_leave_trend(db: Session = Depends(get_db)):
    try:
        query = "SELECT * FROM dw.leave_trends_by_month_mv"
        result = get_result_from_query(query, db)

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

@router.get("/fiscal_year_leave_type_trend", response_model=List[FiscalYearLeaveTypeTrend])
def get_fiscal_year_leave_type_trend(db: Session = Depends(get_db)):
    try:
        query = "SELECT * FROM dw.leave_trend_by_fiscal_year_per_leave_type_mv"
        result = get_result_from_query(query, db)

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
        query = """
            SELECT fiscal_start_date, fiscal_end_date, departmentDescription, leaveTypeName, leave_count 
            FROM dw.leave_request_distribution_by_department_and_leave_types_mv
        """
        result = get_result_from_query(query, db)

        department_leave_distributions = []
        for fiscal_start_date, fiscal_end_date, departmentDescription, leaveTypeName, leave_count in result:
            department_leave_distribution = DepartmentLeaveDistribution(
                fiscal_start_date=fiscal_start_date,
                fiscal_end_date=fiscal_end_date,
                departmentDescription=departmentDescription,
                leaveTypeName=leaveTypeName,
                leave_count=leave_count
            )
            department_leave_distributions.append(department_leave_distribution)

        return department_leave_distributions

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error occurred: {e}")

@router.get("/top_10_project_allocations", response_model=List[ProjectAllocations])
def get_top_10_project_allocations(db: Session = Depends(get_db)):
    try:
        query = "SELECT * FROM dw.top_10_project_allocations_mv"
        result = get_result_from_query(query, db)

        top_project_allocations = []
        for name, request_count in result:
            top_10_project_allocations = ProjectAllocations(
                name=name,
                request_count=request_count
            )
            top_project_allocations.append(top_10_project_allocations)
        return top_project_allocations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error occurred{e}")
