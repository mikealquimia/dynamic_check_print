# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountPayment(models.Model):
    _inherit = "account.payment"

    def check_do(self):
        self.write({'is_move_sent': True})
        return