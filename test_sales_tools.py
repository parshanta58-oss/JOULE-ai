from tools.sales_tools import get_sales_summary,get_top_customers,get_customer_sales,get_order_details,get_sales_by_product

""" result=get_sales_summary("2026-01-01", "2026-01-31")
print(result)

from tools.sales_tools import get_top_customers

 """
""" result = get_top_customers()

for customer in result:
    print(customer) """

""" result = get_customer_sales(1)

print(result) """


""" result = get_order_details(1)

print(result) """

result = get_sales_by_product()

for product in result:
    print(product)