from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Employee(Base):
    __tablename__ = "public.employee_details"

    empId = Column(Integer, primary_key=True, index=True)
    designationId = Column(Integer)
    designationName = Column(String(255))
    firstName = Column(String(255))
    middleName = Column(String(255))
    lastName = Column(String(255))
    email = Column(String(255))
    departmentDescription = Column(String(255))
    allocations = relationship("Allocation", back_populates="employee")
    fact_table = relationship("FactTable", back_populates="employee")

class Allocation(Base):
    __tablename__ = "public.allocations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    type = Column(String(255))
    empId = Column(Integer, ForeignKey("public.employee_details.empId"))
    employee = relationship("Employee", back_populates="allocations")

class FiscalDetail(Base):
    __tablename__ = "public.fiscal_detail"

    fiscal_id = Column(Integer, primary_key=True, index=True)
    fiscal_start_date = Column(DateTime(timezone=True))
    fiscal_end_date = Column(DateTime(timezone=True))
    fact_table = relationship("FactTable", back_populates="fiscal_detail")

class LeaveType(Base):
    __tablename__ = "public.leave_type"

    leave_type_id = Column(Integer, primary_key=True, index=True)
    leavetypename = Column(String(255))
    fact_table = relationship("FactTable", back_populates="leave_type")

class FactTable(Base):
    __tablename__ = "public.fact_table"

    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer)
    empId = Column(Integer, ForeignKey("public.employee_details.empId"))
    teamManagerId = Column(Integer)
    isHr = Column(Boolean)
    isSupervisor = Column(Boolean)
    startDate = Column(DateTime(timezone=True))
    endDate = Column(DateTime(timezone=True))
    leaveDays = Column(Integer)
    reason = Column(String(255))
    status = Column(String(255))
    remarks = Column(String(255))
    leaveTypeId = Column(Integer, ForeignKey("public.leave_type.leave_type_id"))
    defaultDays = Column(Integer)
    transferableDays = Column(Integer)
    isConsecutive = Column(Integer)
    fiscalId = Column(Integer, ForeignKey("public.fiscal_detail.fiscal_id"))
    fiscalIsCurrent = Column(Boolean)
    isConverted = Column(Integer)
    createdAt = Column(DateTime(timezone=True))
    updatedAt = Column(DateTime(timezone=True))

    employee = relationship("Employee", back_populates="fact_table")
    leave_type = relationship("LeaveType", back_populates="fact_table")
    fiscal_detail = relationship("FiscalDetail", back_populates="fact_table")
