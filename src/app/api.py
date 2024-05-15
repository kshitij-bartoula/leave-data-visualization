from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from .database import SessionLocal, get_db
from sqlalchemy.exc import SQLAlchemyError
from .models import Employee, FactTable, LeaveType, FiscalDetail, Allocation
from .schemas import (
    EmployeeLeave,
    LeaveBalance,
    LeaveTrend,
    LeaveDistribution,
    FiscalYearTrend,
    FiscalYearLeaveTypeTrend,
    DepartmentLeaveDistribution,
    DepartmentLeaveStatusCount,
    MostFrequentLeaveReason,
    LeaveConversionCount,
)
from utils.db_utils import get_result_from_query

router = APIRouter()


# def get_db() -> Session:
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


@router.get("/employee_leave", response_model=List[EmployeeLeave])
def get_employee_leave(db: Session = Depends(get_db)):
    try:
        query_statement = (
            db.query(
                FactTable.empId,
                Employee.firstName,
                Employee.lastName,
                func.sum(FactTable.leaveDays),
            )
            .join(Employee, Employee.empId == FactTable.empId)
            .group_by(FactTable.empId, Employee.firstName, Employee.lastName)
        )
        result = get_result_from_query(query_statement)
        employee_leave = []
        for empId, firstName, lastName, total_leave_days in result:
            employee = EmployeeLeave(
                empId=empId,
                firstName=firstName,
                lastName=lastName,
                total_leave_days=total_leave_days,
            )
            employee_leave.append(employee)
        return employee_leave
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error occurred{e}")


@router.get("/leave_balance", response_model=List[LeaveBalance])
def get_leave_balance(db: Session = Depends(get_db)):
    try:

        query_statement = (
            db.query(
                FactTable.empId,
                Employee.firstName,
                Employee.lastName,
                func.max(FactTable.defaultDays),
                func.max(FactTable.transferableDays),
                func.sum(FactTable.leaveDays),
                func.max(FactTable.defaultDays)
                + func.max(FactTable.transferableDays)
                - func.sum(FactTable.leaveDays),
            )
            .join(Employee, Employee.empId == FactTable.empId)
            .group_by(FactTable.empId, Employee.firstName, Employee.lastName)
        )
        result = get_result_from_query(query_statement)

        leave_balances = []
        for (
            empId,
            firstName,
            lastName,
            defaultDays,
            transferabledays,
            leaveDays,
            leave_balance,
        ) in result:
            leave_balance = LeaveBalance(
                empId=empId,
                firstName=firstName,
                lastName=lastName,
                defaultDays=defaultDays,
                transferabledays=transferabledays,
                leaveDays=leaveDays,
                leave_balance=leave_balance,
            )
            leave_balances.append(leave_balance)

        return leave_balances
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error occurred{e}")


@router.get("/leave_trend", response_model=List[LeaveTrend])
def get_leave_trend(db: Session = Depends(get_db)):
    try:
        query_statement = (
            db.query(
                func.extract("month", FactTable.startDate),
                func.extract("year", FactTable.startDate),
                func.count(FactTable.id),
            )
            .group_by(func.extract("month", FactTable.startDate), func.extract("year", FactTable.startDate))
        )
        result = get_result_from_query(query_statement)
        leave_trends = []
        for month, year, leave_count in result:
            leave_trend = LeaveTrend(month=month, year=year, leave_count=leave_count)
            leave_trends.append(leave_trend)
        return leave_trends
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error occurred{e}")


@router.get("/leave_distribution", response_model=List[LeaveDistribution])
def get_leave_distribution(db: Session = Depends(get_db)):
    try:
        query_statement = (
            db.query(LeaveType.leavetypename, func.count(FactTable.id))
            .join(LeaveType, LeaveType.leave_type_id == FactTable.leaveTypeId)
            .group_by(LeaveType.leavetypename)
        )
        result = get_result_from_query(query_statement)
        leave_distributions = []
        for leave_type_name, leave_count in result:
            leave_distribution = LeaveDistribution(
                leavetypename=leave_type_name, leave_count=leave_count
            )
            leave_distributions.append(leave_distribution)
        return leave_distributions
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error occurred{e}")


@router.get("/fiscal_year_trend", response_model=List[FiscalYearTrend])
def get_fiscal_year_trend(db: Session = Depends(get_db)):
    try:
        query_statement = (
            db.query(
                FiscalDetail.fiscal_id,
                FiscalDetail.fiscal_start_date,
                FiscalDetail.fiscal_end_date,
                func.count(FactTable.id),
            )
            .join(FiscalDetail, FiscalDetail.fiscal_id == FactTable.fiscalId)
            .group_by(FiscalDetail.fiscal_id, FiscalDetail.fiscal_start_date, FiscalDetail.fiscal_end_date)
        )
        result = get_result_from_query(query_statement)
        fiscal_year_trends = []
        for fiscal_id, fiscal_start_date, fiscal_end_date, leave_count in result:
            fiscal_year_trend = FiscalYearTrend(
                fiscal_id=fiscal_id,
                fiscal_start_date=fiscal_start_date,
                fiscal_end_date=fiscal_end_date,
                leave_count=leave_count
            )
            fiscal_year_trends.append(fiscal_year_trend)
        return fiscal_year_trends
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail=f"Database error occurred{e}")


@router.get("/fiscal_year_leave_type_trend", response_model=List[FiscalYearLeaveTypeTrend])
def get_fiscal_year_leave_type_trend(db: Session = Depends(get_db)):
    try:
        query_statement = (
            db.query(
                FiscalDetail.fiscal_id,
                FiscalDetail.fiscal_start_date,
                FiscalDetail.fiscal_end_date,
                LeaveType.leavetypename,
                func.count(FactTable.id),
            )
            .join(FiscalDetail, FiscalDetail.fiscal_id == FactTable.fiscalId)
            .join(LeaveType, LeaveType.leave_type_id == FactTable.leaveTypeId)
            .group_by(FiscalDetail.fiscal_id, FiscalDetail.fiscal_start_date, FiscalDetail.fiscal_end_date, LeaveType.leavetypename)
        )
        result = get_result_from_query(query_statement)
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
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail=f"Database error occurred{e}")


@router.get("/department_leave_distribution", response_model=List[DepartmentLeaveDistribution])
def get_department_leave_distribution(db: Session = Depends(get_db)):
    try:
        query_statement = (
            db.query(
                Employee.departmentDescription,
                LeaveType.leavetypename,
                func.count(FactTable.id),
            )
            .join(Employee, Employee.empId == FactTable.empId)
            .join(LeaveType, LeaveType.leave_type_id == FactTable.leaveTypeId)
            .group_by(Employee.departmentDescription, LeaveType.leavetypename)
        )
        result = get_result_from_query(query_statement)
        department_leave_distributions = []
        for departmentDescription, leavetypename, leave_count in result:
            department_leave_distribution = DepartmentLeaveDistribution(
                departmentDescription=departmentDescription,
                leaveTypeName=leavetypename,
                leave_count=leave_count,
            )
            department_leave_distributions.append(department_leave_distribution)
        return department_leave_distributions
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error occurred{e}")


@router.get("/department_leave_status_count", response_model=List[DepartmentLeaveStatusCount])
def get_department_leave_status_count(db: Session = Depends(get_db)):
    try:
        query_statement = (
            db.query(
                Employee.departmentDescription,
                func.count(func.CASE([(FactTable.status == 'APPROVED', 1)], else_=None)).label("approved"),
                func.count(func.CASE([(FactTable.status == 'REJECTED', 1)], else_=None)).label("rejected"),
                func.count(func.CASE([(FactTable.status == 'REQUESTED', 1)], else_=None)).label("requested"),
                func.count(func.CASE([(FactTable.status == 'CANCELLED', 1)], else_=None)).label("cancelled"),
            )
            .join(Employee, Employee.empId == FactTable.empId)
            .group_by(Employee.departmentDescription)
        )
        result = get_result_from_query(query_statement)
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
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail=f"Database error occurred{e}")

@router.get("/most_frequent_leave_reason", response_model=List[MostFrequentLeaveReason])
def get_most_frequent_leave_reason(db: Session = Depends(get_db)):
    try:
        query_statement = (
            db.query(
                FactTable.reason,
                func.count(FactTable.id),
            )
            .group_by(FactTable.reason)
        )

        result = get_result_from_query(query_statement)
        most_frequent_leave_reasons = []
        for reason, request_count in result:
            most_frequent_leave_reason = MostFrequentLeaveReason(
                reason=reason,
                request_count=request_count
            )
            most_frequent_leave_reasons.append(most_frequent_leave_reason)
        return most_frequent_leave_reasons
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error occurred{e}")


@router.get("/leave_conversion_count", response_model=LeaveConversionCount)
def get_leave_conversion_count(db: Session = Depends(get_db)):
    try:
        query_statement = (
            db.query(
                func.sum(func.CASE([(FactTable.isConverted == 1, 1)], else_=0)).label("conversion_count")
            ).statement
        )
        result = get_result_from_query(query_statement)
        leave_conversion_count = LeaveConversionCount(
            conversion_count=result[0]["conversion_count"]
        )
        return leave_conversion_count
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail=f"Database error occurred{e}")