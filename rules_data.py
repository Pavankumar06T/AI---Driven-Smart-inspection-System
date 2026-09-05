from rules_schema import ComplianceRule

RULES: list[ComplianceRule] = [


    ComplianceRule(
        check_id="WAGE-001",
        scenario="wage_reconciliation",
        title="Wage below applicable minimum wage / floor wage",
        code="Code on Wages, 2019",
        section="Section 6 read with Section 9",
        clause_text=(
            "Section 6 empowers the appropriate Government to fix the minimum rate of "
            "wages payable to employees (time work or piece work). Section 9(2) requires "
            "that any rate fixed under Section 6 not be less than the floor wage fixed by "
            "the Central Government, and existing higher rates cannot be reduced."
        ),
        condition="Extracted monthly wage is below the notified minimum rate / floor wage for the worker's state, sector, and skill category.",
        applies_when={"state": "*", "sector": "*"},
        field_dependencies=["monthly_wage", "worker_skill_category", "state"],
        severity=4,
        violation_type="discrepancy",
    ),

    ComplianceRule(
        check_id="WAGE-002",
        scenario="wage_reconciliation",
        title="Wages not paid within statutory time limit",
        code="Code on Wages, 2019",
        section="Section 17",
        clause_text=(
            "Sets the time limit for payment of wages — monthly wages must be paid by "
            "the 7th day of the following month; full and final settlement on "
            "termination, resignation, or retrenchment must be paid within two "
            "working days."
        ),
        condition="Wage payment date recorded in the register is later than the statutory deadline for the applicable wage period, or settlement on separation exceeds two working days.",
        applies_when={"state": "*", "sector": "*"},
        field_dependencies=["wage_payment_date", "wage_period", "separation_date"],
        severity=3,
        violation_type="discrepancy",
    ),

    ComplianceRule(
        check_id="WAGE-003",
        scenario="wage_reconciliation",
        title="Overtime paid below statutory rate",
        code="Code on Wages, 2019",
        section="Section 14",
        clause_text="Requires overtime work to be paid at a rate not less than twice the normal rate of wages.",
        condition="Recorded overtime pay rate is less than twice the recorded normal wage rate for the same employee.",
        applies_when={"state": "*", "sector": "*"},
        field_dependencies=["overtime_hours", "overtime_pay", "normal_wage_rate"],
        severity=3,
        violation_type="discrepancy",
    ),

    ComplianceRule(
        check_id="WAGE-004",
        scenario="wage_reconciliation",
        title="Wage deductions exceed statutory cap",
        code="Code on Wages, 2019",
        section="Section 18(3)",
        clause_text="Total deductions from an employee's wages in any wage period shall not exceed fifty per cent of such wages.",
        condition="Total recorded deductions for a wage period exceed 50% of the gross wages for that period.",
        applies_when={"state": "*", "sector": "*"},
        field_dependencies=["gross_wages", "total_deductions"],
        severity=3,
        violation_type="discrepancy",
    ),

    ComplianceRule(
        check_id="WAGE-005",
        scenario="wage_reconciliation",
        title="Bonus not paid despite eligibility",
        code="Code on Wages, 2019",
        section="Section 26 (Chapter IV)",
        clause_text="Bonus payment provisions apply to establishments employing 20 or more employees in an accounting year; eligible employees must receive a minimum bonus.",
        condition="Headcount is 20 or more for the accounting year, but no bonus payment record exists for an eligible employee.",
        applies_when={"min_headcount": 20},
        field_dependencies=["headcount", "bonus_payment_record", "employee_monthly_wage"],
        severity=3,
        violation_type="missing",
    ),


    ComplianceRule(
        check_id="SAFETY-001",
        scenario="safety_documentation",
        title="Safety Committee not constituted despite headcount threshold",
        code="Occupational Safety, Health and Working Conditions Code, 2020",
        section="Section 22 — threshold prescribed by rules (500 general / 250 hazardous-process), not fixed in the Code itself",
        clause_text=(
            "Provides for constitution of a Safety Committee, with employer and worker "
            "representatives, in such class of establishments as may be prescribed. "
            "Prescribed threshold (per rules): 500+ workers generally, or 250+ workers "
            "for a factory carrying on a hazardous process."
        ),
        condition="Headcount meets or exceeds the rule-prescribed threshold but no Safety Committee record is present.",
        applies_when={"min_headcount": 500, "min_headcount_hazardous": 250},
        field_dependencies=["safety_committee_record", "headcount", "hazardous_process_flag"],
        severity=5,
        violation_type="missing",
    ),

    ComplianceRule(
        check_id="SAFETY-002",
        scenario="safety_documentation",
        title="Appointment letter not issued",
        code="Occupational Safety, Health and Working Conditions Code, 2020",
        section="Section 6",
        clause_text="Requires every employer to issue a letter of appointment to every employee on appointment, in the prescribed form and content.",
        condition="No appointment letter record exists for an employee listed in the register.",
        applies_when={"state": "*", "sector": "*"},
        field_dependencies=["appointment_letter_record", "employee_name"],
        severity=3,
        violation_type="missing",
    ),

    ComplianceRule(
        check_id="SAFETY-003",
        scenario="safety_documentation",
        title="Working hours exceed statutory limit",
        code="Occupational Safety, Health and Working Conditions Code, 2020",
        section="Section 25 (Chapter VII)",
        clause_text="Caps normal working hours at 8 hours per day and 48 hours per week (subject to prescribed overtime rules).",
        condition="Recorded daily or weekly working hours for an employee exceed the statutory cap without a documented overtime/exemption basis.",
        applies_when={"state": "*", "sector": "*"},
        field_dependencies=["daily_working_hours", "weekly_working_hours"],
        severity=3,
        violation_type="discrepancy",
    ),

    ComplianceRule(
        check_id="SAFETY-004",
        scenario="safety_documentation",
        title="Accident not reported within statutory timeframe",
        code="Occupational Safety, Health and Working Conditions Code, 2020",
        section="Section 10",
        clause_text="Requires the employer to notify the prescribed authority of any accident causing death, or bodily injury preventing the injured person from working for 48 hours or more.",
        condition="A recorded workplace accident meeting the death/48-hour-injury threshold has no corresponding notice/report record.",
        applies_when={"state": "*", "sector": "*"},
        field_dependencies=["accident_record", "notice_to_authority_record"],
        severity=5,
        violation_type="missing",
    ),

    ComplianceRule(
        check_id="SAFETY-005",
        scenario="safety_documentation",
        title="Annual health examination not provided",
        code="Occupational Safety, Health and Working Conditions Code, 2020",
        section="Section 6",
        clause_text="Requires the employer to provide a free annual health examination or test to prescribed classes of employees.",
        condition="Employee falls within a prescribed class (e.g., by age or hazardous-work exposure) but no health-examination record exists for the relevant year.",
        applies_when={"state": "*", "sector": "*"},
        field_dependencies=["health_examination_record", "employee_age", "hazardous_process_flag"],
        severity=3,
        violation_type="missing",
    ),


    ComplianceRule(
        check_id="REG-001",
        scenario="registration_licensing",
        title="Establishment not registered above headcount threshold",
        code="Occupational Safety, Health and Working Conditions Code, 2020",
        section="Section 3(1) read with Section 2",
        clause_text=(
            "Section 3(1) requires every employer of a covered establishment to apply "
            "for registration within sixty days of the Code's applicability to that "
            "establishment. Section 2 defines a covered establishment as, among other "
            "categories, one in which ten or more workers are employed."
        ),
        condition="Headcount is ten or more, but no registration number/document is present.",
        applies_when={"min_headcount": 10},
        field_dependencies=["registration_number", "headcount"],
        severity=5,
        violation_type="missing",
    ),

    ComplianceRule(
        check_id="REG-002",
        scenario="registration_licensing",
        title="Notice of commencement of operations not filed",
        code="Occupational Safety, Health and Working Conditions Code, 2020",
        section="Section 5",
        clause_text="Requires the employer to give notice to the registering authority of commencement (and cessation) of operations.",
        condition="Establishment is operational (per profile/document) but no commencement-notice record exists.",
        applies_when={"state": "*", "sector": "*"},
        field_dependencies=["commencement_notice_record", "operational_status"],
        severity=3,
        violation_type="missing",
    ),

    ComplianceRule(
        check_id="REG-003",
        scenario="registration_licensing",
        title="Contractor license not obtained above contract-labour threshold",
        code="Occupational Safety, Health and Working Conditions Code, 2020",
        section="TBD — confirmed threshold (50+ contract labourers), exact section number in the Contract Labour chapter not verified from available sources; check bare Act before use",
        clause_text=(
            "Contract-labour provisions of the Code apply where 50 or more contract "
            "labourers are engaged in/through an establishment; contractors above this "
            "threshold must obtain a license."
        ),
        condition="Number of contract labourers is 50 or more, but no contractor license record is present.",
        applies_when={"min_contract_labour": 50},
        field_dependencies=["contract_labour_count", "contractor_license_record"],
        severity=4,
        violation_type="missing",
    ),

    ComplianceRule(
        check_id="REG-004",
        scenario="registration_licensing",
        title="Inter-state migrant worker provisions not applied above threshold",
        code="Occupational Safety, Health and Working Conditions Code, 2020",
        section="TBD — confirmed threshold (10+ inter-state migrant workers), exact section number not verified from available sources; check bare Act before use",
        clause_text="Provisions for inter-state migrant workers apply where 10 or more such workers are employed (or were employed on any day of the preceding 12 months).",
        condition="10 or more inter-state migrant workers are recorded, but no ISMW-specific compliance record (e.g., journey allowance, self-declaration registration) is present.",
        applies_when={"min_ismw_count": 10},
        field_dependencies=["ismw_count", "ismw_compliance_record"],
        severity=4,
        violation_type="missing",
    ),

    ComplianceRule(
        check_id="REG-005",
        scenario="registration_licensing",
        title="Establishment headcount misreported relative to legal 'establishment' threshold",
        code="Occupational Safety, Health and Working Conditions Code, 2020",
        section="Section 2 (Definitions)",
        clause_text="Defines a covered 'establishment' by category, including any place where an industry, trade, business, or manufacturing is carried on in which 10 or more workers are employed.",
        condition="Declared headcount in the establishment profile is below 10, but extracted document fields (e.g., wage register row count, attendance records) indicate 10 or more workers actually present.",
        applies_when={"state": "*", "sector": "*"},
        field_dependencies=["declared_headcount", "extracted_worker_count"],
        severity=4,
        violation_type="substantive",
    ),
]