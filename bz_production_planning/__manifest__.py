{
    "name": "Production Planning (Simplified)",
    "version": "18.0.1.0.0",
    "category": "Manufacturing/Manufacturing",
    "summary": "Plan production by period and generate manufacturing orders in one click",
    "description": """
Simplified production planning for small and medium manufacturers.

* Create a production plan for a period with one line per product.
* The bill of materials is suggested automatically for each product.
* Generate all manufacturing orders from the plan in one click.
* Track the progress of every manufacturing order from the plan.
    """,
    "author": "Bryan Esparza",
    "website": "https://github.com/Bryan-Es/odoo18-portfolio",
    "license": "LGPL-3",
    "depends": ["mrp"],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "views/production_plan_views.xml",
        "views/mrp_production_views.xml",
        "views/menus.xml",
    ],
    "installable": True,
    "application": False,
}
