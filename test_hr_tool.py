from tools.hr_tool import (
    get_employee_details,
    get_employee_attendance,
    get_employee_leaves,
    get_department_employees,
    get_employee_count_by_department
)

print(get_employee_details(10))

print(get_employee_attendance(10))

print(get_employee_leaves(10))

print(get_department_employees(1))

print(get_employee_count_by_department())