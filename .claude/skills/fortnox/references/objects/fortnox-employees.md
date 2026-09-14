# Fortnox Object: Employees

API group `fortnox` · spec tag `fortnox_Employees`

## Purpose

ScheduleId, MonthlySalary and HourlyPay reflect current values, all
 ScheduleIds are returned in DatedSchedules and all MonthlySalary and
 HourlyPay pairs are returned in DatedWages.

## Endpoints

| Method | Path | Summary |
|---|---|---|
| GET | `/3/employees` | Retrieve a list of employees |
| POST | `/3/employees` | Create a new employee |
| GET | `/3/employees/{EmployeeId}` | Retrieve a specific employee |
| PUT | `/3/employees/{EmployeeId}` | Update employee |

## Calling it

Records are wrapped under `Employees`, so pagination works normally:

```python
for record in client.paginate("employees", "Employees"):
    ...
```

## Key fields

`ATFValue`, `ATKValue`, `AbsenceHoursNonVacationBased`, `AbsenceHoursVacationBased`, `AbsenceWorkdaysNonVacationBased`, `AbsenceWorkdaysVacationBased`, `Address1`, `Address2`, `AutoNonRecurringTax`, `AverageHourlyWage`, `AverageWeeklyHours`, `BankAccountNo`, `City`, `ClearingNo`, `CostCenter`, `Country`, `CurrentCompBalance`, `CurrentFlexBalance`, `DatedSalarySupplements`, `DatedSchedules`, `DatedWages`, `Email`, `EmployedTo`, `EmployeeCategories`, `EmployeeChildren`, `EmployeeId`, `EmploymentDate`, `EmploymentForm`, `FirstName`, `ForaType`, `FullName`, `FullTimeEquivalent`, `HourlyPay`, `Inactive`, `IngoingSickLeave`, `IngoingUsedHolidaySupplement`, `IngoingUsedVacationDays`, `InitialComp`, `InitialFlex`, `JobTitle`, `LastName`, `MonthlySalary`, `NonRecurringTax`, `NonVacationBasedCalendarDaysPartial`, `NonVacationBasedCalendarDaysWhole`, `OpeningSalaries`, `PayslipType`, `PersonalIdentityNumber`, `PersonelType`, `Phone1`, `Phone2`, `PostCode`, `PreliminaryTaxDeducted`, `Project`, `SalaryForm`, `ScheduleId`, `TaxAllowance`, `TaxColumn`, `TaxTable`, `VacationBasedAttendanceDays`, `VacationBasedAttendanceHours`, `VacationBasedCalendarDaysWhole`, `VacationBasedSalaryTotal`, `VacationBasedSalaryVariableAddition`, `VacationBasedSalaryWorkedTime`, `VacationCalculationAdvanceVacationDebt`, `VacationCalculationIncludeInCalculation`, `VacationCalculationSameWagePercent`, `VacationCalculationSoleCustody`, `VacationCalculationSumOnlyNoDays`, `VacationCalculationTotalVacationSalarySum`, `VacationCalculationVacationEntitlement`, `VacationCalculationVariableAdditionSum`, `VacationDaysPaid`, `VacationDaysPendingPaid`, `VacationDaysPendingPrepaid`, `VacationDaysPendingSaved`, `VacationDaysPendingSavedYear1`, `VacationDaysPendingSavedYear2`, `VacationDaysPendingSavedYear3`, `VacationDaysPendingSavedYear4`, `VacationDaysPendingSavedYear5`, `VacationDaysPendingSavedYear6Plus`, `VacationDaysPendingUnpaid`, `VacationDaysPrepaid`, `VacationDaysRegisteredPaid`, `VacationDaysRegisteredPrepaid`, `VacationDaysRegisteredSaved`, `VacationDaysRegisteredSavedYear1`, `VacationDaysRegisteredSavedYear2`, `VacationDaysRegisteredSavedYear3`, `VacationDaysRegisteredSavedYear4`, `VacationDaysRegisteredSavedYear5`, `VacationDaysRegisteredSavedYear6Plus`, `VacationDaysRegisteredUnpaid`, `VacationDaysSaved`, `VacationDaysSavedEmploymentRateYear1`, `VacationDaysSavedEmploymentRateYear2`, `VacationDaysSavedEmploymentRateYear3`, `VacationDaysSavedEmploymentRateYear4`, `VacationDaysSavedEmploymentRateYear5`, `VacationDaysSavedEmploymentRateYear6Plus`, `VacationDaysSavedYear1`, `VacationDaysSavedYear2`, `VacationDaysSavedYear3`, `VacationDaysSavedYear4`, `VacationDaysSavedYear5`, `VacationDaysSavedYear6Plus`, `VacationDaysUnpaid`, `WorkingTimeEnumeration`

## Writable fields

`ATFValue`, `ATKValue`, `AbsenceHoursNonVacationBased`, `AbsenceHoursVacationBased`, `AbsenceWorkdaysNonVacationBased`, `AbsenceWorkdaysVacationBased`, `Address1`, `Address2`, `AutoNonRecurringTax`, `AverageHourlyWage`, `AverageWeeklyHours`, `BankAccountNo`, `City`, `ClearingNo`, `CostCenter`, `Country`, `CurrentCompBalance`, `CurrentFlexBalance`, `DatedSalarySupplements`, `DatedSchedules`, `DatedWages`, `Email`, `EmployedTo`, `EmployeeChildren`, `EmployeeId`, `EmploymentDate`, `EmploymentForm`, `FirstName`, `ForaType`, `FullName`, `FullTimeEquivalent`, `HourlyPay`, `Inactive`, `IngoingSickLeave`, `IngoingUsedHolidaySupplement`, `IngoingUsedVacationDays`, `InitialComp`, `InitialFlex`, `JobTitle`, `LastName`, `MonthlySalary`, `NonRecurringTax`, `NonVacationBasedCalendarDaysPartial`, `NonVacationBasedCalendarDaysWhole`, `OpeningSalaries`, `PayslipType`, `PersonalIdentityNumber`, `PersonelType`, `Phone1`, `Phone2`, `PostCode`, `PreliminaryTaxDeducted`, `Project`, `SalaryForm`, `ScheduleId`, `TaxAllowance`, `TaxColumn`, `TaxTable`, `VacationBasedAttendanceDays`, `VacationBasedAttendanceHours`, `VacationBasedCalendarDaysWhole`, `VacationBasedSalaryTotal`, `VacationBasedSalaryVariableAddition`, `VacationBasedSalaryWorkedTime`, `VacationCalculationAdvanceVacationDebt`, `VacationCalculationIncludeInCalculation`, `VacationCalculationSameWagePercent`, `VacationCalculationSoleCustody`, `VacationCalculationSumOnlyNoDays`, `VacationCalculationTotalVacationSalarySum`, `VacationCalculationVacationEntitlement`, `VacationCalculationVariableAdditionSum`, `VacationDaysPaid`, `VacationDaysPendingPaid`, `VacationDaysPendingPrepaid`, `VacationDaysPendingSaved`, `VacationDaysPendingSavedYear1`, `VacationDaysPendingSavedYear2`, `VacationDaysPendingSavedYear3`, `VacationDaysPendingSavedYear4`, `VacationDaysPendingSavedYear5`, `VacationDaysPendingSavedYear6Plus`, `VacationDaysPendingUnpaid`, `VacationDaysPrepaid`, `VacationDaysRegisteredPaid`, `VacationDaysRegisteredPrepaid`, `VacationDaysRegisteredSaved`, `VacationDaysRegisteredSavedYear1`, `VacationDaysRegisteredSavedYear2`, `VacationDaysRegisteredSavedYear3`, `VacationDaysRegisteredSavedYear4`, `VacationDaysRegisteredSavedYear5`, `VacationDaysRegisteredSavedYear6Plus`, `VacationDaysRegisteredUnpaid`, `VacationDaysSaved`, `VacationDaysSavedEmploymentRateYear1`, `VacationDaysSavedEmploymentRateYear2`, `VacationDaysSavedEmploymentRateYear3`, `VacationDaysSavedEmploymentRateYear4`, `VacationDaysSavedEmploymentRateYear5`, `VacationDaysSavedEmploymentRateYear6Plus`, `VacationDaysSavedYear1`, `VacationDaysSavedYear2`, `VacationDaysSavedYear3`, `VacationDaysSavedYear4`, `VacationDaysSavedYear5`, `VacationDaysSavedYear6Plus`, `VacationDaysUnpaid`, `WorkingTimeEnumeration`

Required: `Email`, `FirstName`, `LastName`

## Safe use cases

- Read Employees for investigation, reporting and export.

## Dangerous / live actions

- `POST, PUT` change live accounting data in the customer's company.
- These post to real books. Keep them behind the read-only default, a dry run,
  and explicit approval.

## Dry-run requirements

- Verify with a read-only `GET` first.
- Write out the exact request body and target, and have it reviewed, before any write.
- Run it against a sandbox company before a live tenant.

## Approval requirements

- Explicit user approval for every write. Approval for one write is not approval
  for the next.

## Tested read-only requests

- None yet. Add the exact calls you have run once verified against a real tenant.

## Example response fields

- Fill in after reviewing a successful response. The fields above come from the
  spec, which describes what may be returned, not what a given company does return.

## Date tested

- Not yet verified against a live or sandbox tenant.

## Notes

- Generated from the Fortnox OpenAPI specification; do not edit by hand.
  Regenerate with `python generate_object_notes.py`.
