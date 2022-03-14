# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountJournal(models.Model):
    _inherit = "account.journal"

    checkprint_report = fields.Many2many('format.check_print', string="Check Printing Format")