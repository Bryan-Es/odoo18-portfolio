# Odoo 18 Portfolio - Bryan Esparza

[Español](#español) | [English](#english)

---

## Español

Módulos de ejemplo para **Odoo 18** (Community y Enterprise) que muestran cómo personalizo Odoo para negocios reales: modelos nuevos, vistas, seguridad, secuencias, integración con Fabricación y Ventas, y reportes PDF con QWeb.

Son módulos genéricos escritos desde cero. No contienen código ni datos de ningún cliente.

### Módulos

#### 1. `bz_production_planning` - Planificación de producción simplificada

Para fábricas pequeñas que planifican por semana o por mes y no necesitan el Plan Maestro de Producción completo.

- Plan de producción por período, con una línea por producto, cantidad y fecha.
- Sugiere automáticamente la lista de materiales (BoM) de cada producto.
- Botón **Generar órdenes de fabricación**: crea todas las órdenes del plan de una vez.
- Avance del plan (% de órdenes terminadas), botón inteligente a las órdenes y chatter.
- Flujo: Borrador → Confirmado → Hecho (o Cancelado), con validaciones.

Técnico: 2 modelos nuevos, herencia de `mrp.production`, `mail.thread`, secuencia `PLAN/AAAA/0001`, permisos por grupo de Fabricación, restricciones SQL y de Python.

#### 2. `bz_sale_summary_report` - Campos extra en ventas y reporte PDF

- Campos nuevos en el pedido: **fecha límite de entrega**, **canal de venta** (tienda, teléfono, WhatsApp, web) y **nota interna**.
- Días restantes hasta la fecha límite, resaltados en rojo o amarillo en la lista.
- Nota por línea de producto.
- Reporte PDF **Resumen de Venta** en QWeb con el diseño de la empresa: datos del pedido, líneas con secciones y notas, cantidad total e impuestos.
- Filtro "Con fecha límite" y agrupación por canal de venta.

Técnico: herencia de `sale.order` y `sale.order.line`, herencia de vistas con `xpath`, `ir.actions.report` y plantillas QWeb.

### Instalación

1. Copia la carpeta del módulo a tu ruta de addons (o agrega este repositorio a `addons_path`).
2. Reinicia Odoo y activa el modo desarrollador.
3. Aplicaciones → Actualizar lista de aplicaciones → busca el módulo → Instalar.

Requisitos: Odoo 18.0. `bz_production_planning` necesita Fabricación (`mrp`) y `bz_sale_summary_report` necesita Ventas (`sale_management`).

### Capturas

Ver la carpeta [`docs/screenshots`](docs/screenshots).

### Contacto

Bryan Esparza, Tecnólogo en Desarrollo de Software (TEC Azuay), Cuenca, Ecuador.
Desarrollo y personalización de Odoo 17/18, capacitación y manuales de usuario.

---

## English

Sample **Odoo 18** modules (Community and Enterprise) that show how I customize Odoo for real businesses: new models, views, security, sequences, Manufacturing and Sales integration, and QWeb PDF reports.

They are generic modules written from scratch. They contain no client code or data.

### Modules

#### 1. `bz_production_planning` - Simplified production planning

For small factories that plan by week or month and do not need the full Master Production Schedule.

- Production plan per period, one line per product with quantity and date.
- Suggests the bill of materials (BoM) for each product automatically.
- **Generate Manufacturing Orders** button creates every order in the plan at once.
- Plan progress (% of orders done), smart button to the orders, and chatter.
- Workflow: Draft → Confirmed → Done (or Cancelled), with validations.

Technical: 2 new models, `mrp.production` inheritance, `mail.thread`, `PLAN/YYYY/0001` sequence, Manufacturing group access rights, SQL and Python constraints.

#### 2. `bz_sale_summary_report` - Extra sales fields and PDF report

- New order fields: **delivery deadline**, **sales channel** (store, phone, WhatsApp, website) and **internal note**.
- Days left until the deadline, highlighted red or yellow in the list.
- Per-line product note.
- **Sales Summary** QWeb PDF report using the company layout: order details, lines with sections and notes, total quantity and taxes.
- "With Deadline" filter and group by sales channel.

Technical: `sale.order` and `sale.order.line` inheritance, view inheritance with `xpath`, `ir.actions.report` and QWeb templates.

### Installation

1. Copy the module folder into your addons path (or add this repository to `addons_path`).
2. Restart Odoo and enable developer mode.
3. Apps → Update Apps List → search the module → Install.

Requirements: Odoo 18.0. `bz_production_planning` needs Manufacturing (`mrp`) and `bz_sale_summary_report` needs Sales (`sale_management`).

### Screenshots

See [`docs/screenshots`](docs/screenshots).

### Contact

Bryan Esparza, Software Development Technologist (TEC Azuay), Cuenca, Ecuador.
Odoo 17/18 development and customization, training and user guides.

---

License: LGPL-3
