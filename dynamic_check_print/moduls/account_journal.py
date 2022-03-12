# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountJournal(models.Model):
    _inherit = "account.journal"

    checkprint_report = fields.Many2one('ir.actions.report', domain=[('model_id','=','account.payment')], string="Check Printing Format")