# Copyright 2020-2024 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import datetime

from odoo import api, models


class HrLeave(models.Model):
    _inherit = "hr.leave"

    def _get_number_of_days(self, date_from, date_to, employee_id):
        instance = self
        if self.holiday_status_id.request_unit:
            instance = self.with_context(natural_period=True)
            date_from = datetime.combine(date_from, datetime.min.time())
            date_to = datetime.combine(date_to, datetime.max.time())

        return super(HrLeave, instance)._get_number_of_days(
            date_from, date_to, employee_id
        )

    @api.model_create_multi
    def create(self, vals_list):
        """Only in UX an incorrect value is set, recalculate.
        https://github.com/OCA/hr-holidays/issues/105."""
        res = super().create(vals_list)
        res.filtered(
            lambda x: x.holiday_status_id.request_unit == "natural_day"
        )._compute_number_of_days()
        return res
