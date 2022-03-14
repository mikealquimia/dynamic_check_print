# -*- coding: utf-8 -*-

from odoo import models, fields, api

class FormatCheckPrint(models.Model):
    _name = "format.check_print"
    _description = "Format to Check Print"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _order = 'id desc'
    
    name = fields.Char(string="Name")
    state = fields.Selection([
        ('draft', 'Draft'), 
        ('done', 'Done')], string="State", default='draft', tracking=True)
    paper_format = fields.Many2one('report.paperformat', string="Paper Format")
    report_id = fields.Many2one('ir.actions.report', string="Report")
    journal_id = fields.Many2many('account.journal', string='Journal')
    date = fields.Boolean(string="Date", default=True)
    partner = fields.Boolean(string="Partner", default=True)
    amount = fields.Boolean(string="Amount", default=True)
    amount_letters = fields.Boolean(string="Amount in letters", default=True)
    negotiable = fields.Boolean(string="Negotiable", default=True)
    voucher = fields.Boolean(string="Voucher", default=False)
      
    #Date fields
    type_date = fields.Selection([
        ('simple', '13/01/2022'), 
        ('letters', 'January thirteenth, two thousand and twenty two'),
        ('mix0', '13 of January, 2022'),
        ('mix1', 'January 13, 2022')], string="Type of Date", default='mix0', tracking=True)
    date_field = fields.Many2one('ir.model.fields', domain="['&',('ttype','=','date'),('model_id','=','account.payment')]", string="Field to Date")
    text_transform_date = fields.Selection([
        ('capitalize', 'First Letter Of Each Word Capitalized'), 
        ('uppercase', 'ALL LETTERS IN CAPITAL LETTERS'),
        ('lowercase', 'all letters in lowercase')], string="Style Text", default='capitalize', tracking=True)   
    
    #Partner fields
    type_partner = fields.Selection([
        ('company', 'Company of Partner'), 
        ('individual', 'Contact of Partner Company'),
        ('direct', 'Partner of Payment')], string="Type of Partner", default='direct', tracking=True)
    text_transform_partner = fields.Selection([
        ('capitalize', 'First Letter Of Each Word Capitalized'), 
        ('uppercase', 'ALL LETTERS IN CAPITAL LETTERS'),
        ('lowercase', 'all letters in lowercase')], string="Style Text", default='capitalize', tracking=True)
    
    #Amount fields
    type_amount = fields.Selection([
        ('simple', 'Only amount'), 
        ('symbol', 'With symbol(s)')], string="Type of Amount", default='simple', tracking=True)
    pre_symbol = fields.Char(string="Symbol before amount")
    post_symbol = fields.Char(string="Symbol after amount")
    currency_amount = fields.Selection([
        ('none', 'No currency'),
        ('after', 'After amount'), 
        ('before', 'Before amount')], string="Currency", default='none', tracking=True)
    
    #Amount in letter fields
    text_transform_amount_letters = fields.Selection([
        ('capitalize', 'First Letter Of Each Word Capitalized'), 
        ('uppercase', 'ALL LETTERS IN CAPITAL LETTERS'),
        ('lowercase', 'all letters in lowercase')], string="Style Text", default='capitalize', tracking=True)
    type_amount_letter = fields.Selection([
        ('simple', 'Only amount'), 
        ('symbol', 'With symbol(s)')], string="Type of letters Amount", default='simple', tracking=True)
    pre_symbol_letter = fields.Char(string="Symbol before amount")
    post_symbol_letter = fields.Char(string="Symbol after amount")
    currency_amount_letter = fields.Selection([
        ('none', 'No currency'),
        ('before', 'Before amount')], string="Currency", default='none', tracking=True)
    
    #Voucher
    description = fields.Selection([
        ('none', 'No Description'), 
        ('invoices', 'Fields in Invoice(s)'),
        ('payment', 'Field in Payment')], string="Description", default='none', tracking=True)
    fields_description = fields.Many2many('ir.model.fields', string="Description fields", help="They will be separated by a comma", domain="[('model_id','=','account.move')]")
    field_description = fields.Many2one('ir.model.fields', string="Description field", domain="['&',('ttype','=','date'),('model_id','=','account.payment')]")
    account_move = fields.Boolean(string="Account move")
    total_account_move = fields.Boolean(string="Totals")
    
    
    def set_draft(self):
        return self.write({'state': 'draft'})
    
    def set_done(self):
        return self.write({'state': 'done'})