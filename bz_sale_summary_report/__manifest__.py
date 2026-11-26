{
    "name": "Sales Summary Report",
    "version": "18.0.1.0.0",
    "category": "Sales/Sales",
    "summary": "Extra sales fields (deadline, channel, notes) and a custom QWeb PDF summary",
    "description": """
Adds practical fields to quotations and sales orders and a printable summary.

* Delivery deadline, sales channel and internal note on the order.
* Days left until the deadline, highlighted in the list view.
* Per-line note printed on the PDF.
* "Sales Summary" PDF report built with QWeb and the company layout.
    """,
    "author": "Bryan Esparza",
    "website": "https://github.com/",
    "license": "LGPL-3",
    "depends": ["sale_management"],
    "data": [
        "views/sale_order_views.xml",
        "report/sale_summary_report.xml",
        "report/sale_summary_templates.xml",
    ],
    "installable": True,
    "application": False,
}
