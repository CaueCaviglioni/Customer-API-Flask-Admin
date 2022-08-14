from flask_admin.contrib.sqla import ModelView
from flask_admin.actions import action
from models.customer import CustomerModel
from flask import flash, session, abort
from db import db


class CustomerView(ModelView):
    #edit_template = "edit.html"
    list_template = "list.html"

    can_edit = True
    can_create = False

    column_list = ["uuid_customer", "name", "telephone", "is_vip"]
    form_columns = ["uuid_customer", "name", "telephone", "is_vip"]
    column_searchable_list = ["uuid_customer", "name"]

    def is_accessible(self):
        if "logged_in" in session:
            return True
        else:
            abort(403)

    @action(
        "toogle_is_vip",
        "Change VIP Status",
        "Are you sure?"
    )
    def toogle_is_vip_status(self, ids):
        customers = CustomerModel.query.filter(CustomerModel.customer_id.in_(ids)).all()
        for customer in customers:
            customer.is_vip = not customer.is_vip
        db.session.commit()
        flash("Customers changes successfully", "success")


    def on_form_prefill(self, form, id):
        form.uuid_customer.render_kw = {"readonly": True}

    