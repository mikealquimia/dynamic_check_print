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
    view_id = fields.Many2one('ir.ui.view', string="View")
    page_height = fields.Float(string="Page Height (mm)")
    page_width = fields.Float(string="Page Width (mm)")
    orientation = fields.Selection([
        ('Landscape', 'Landscape'), 
        ('Portrait', 'Portrait')], string="Orientation", default='Portrait')
    journal_id = fields.Many2many('account.journal', string='Journal')
    date = fields.Boolean(string="Date", default=True)
    partner = fields.Boolean(string="Partner", default=True)
    amount = fields.Boolean(string="Amount", default=True)
    amount_letters = fields.Boolean(string="Amount in letters", default=True)
    negotiable = fields.Boolean(string="Not Negotiable", default=True)
    voucher = fields.Boolean(string="Voucher", default=False)
    
    #Voucher fields
    top_negotiable = fields.Float(string="Top Not Negotiable (cm)")
    left_negotiable = fields.Float(string="Left Not Negotiable (cm)") 
    
    #Date fields
    type_date = fields.Selection([
        ('simple', '13/01/2022'), 
        ('mix0', '13 of January, 2022'),
        ('mix1', 'January 13, 2022')], string="Type of Date", default='mix0', tracking=True)
    date_field = fields.Many2one('ir.model.fields', domain="['&',('ttype','=','date'),('model_id','=','account.payment')]", string="Field to Date")
    text_transform_date = fields.Selection([
        ('capitalize', 'First Letter Of Each Word Capitalized'), 
        ('uppercase', 'ALL LETTERS IN CAPITAL LETTERS'),
        ('lowercase', 'all letters in lowercase')], string="Style Text", default='capitalize', tracking=True)
    top_date = fields.Float(string="Top Date (cm)")
    left_date = fields.Float(string="Left Date (cm)") 
    
    #Partner fields
    type_partner = fields.Selection([
        ('company', 'Company of Partner'), 
        ('direct', 'Partner of Payment')], string="Type of Partner", default='direct', tracking=True)
    text_transform_partner = fields.Selection([
        ('capitalize', 'First Letter Of Each Word Capitalized'), 
        ('uppercase', 'ALL LETTERS IN CAPITAL LETTERS'),
        ('lowercase', 'all letters in lowercase')], string="Style Text", default='capitalize', tracking=True)
    top_partner = fields.Float(string="Top Partner (cm)")
    left_partner = fields.Float(string="Left Partner (cm)")
    
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
    top_amount = fields.Float(string="Top Amount (cm)")
    left_amount = fields.Float(string="Left Amount (cm)")
    
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
    top_amount_letters = fields.Float(string="Top Amount in letter (cm)")
    left_amount_letters = fields.Float(string="Left Amount in letter (cm)")
    
    #Voucher
    description = fields.Selection([
        ('none', 'No Description'), 
        ('invoices', 'Fields in Invoice(s)'),
        ('payment', 'Field in Payment')], string="Description", default='none', tracking=True)
    fields_description = fields.Many2many('ir.model.fields', string="Description fields", help="They will be separated by a comma", domain="['&', ('model_id', '=', 'account.move'), '|', '|', '|', '|', '|', '|', ('ttype', '=', 'char'), ('ttype', '=', 'float'), ('ttype', '=', 'many2one'), ('ttype', '=', 'monetary'), ('ttype', '=', 'reference'), ('ttype', '=', 'selection'), ('ttype', '=', 'text')]")
    field_description = fields.Many2one('ir.model.fields', string="Description field", domain="['&',('ttype','=','char'),('model_id','=','account.payment')]")
    top_description = fields.Float(string="Top Description (cm)")
    left_description = fields.Float(string="Left Description (cm)")

    account_move = fields.Boolean(string="Account move")
    top_account_move = fields.Float(string="Top Table Account Move (cm)")
    left_account_move = fields.Float(string="Left Table Account Move (cm)")
    width_code = fields.Float(string="Width Col Code (cm)")
    width_name = fields.Float(string="Width Col Name (cm)")
    width_credit = fields.Float(string="Width Col Credit (cm)")
    width_debit = fields.Float(string="Width Col Debit (cm)")

    total_account_move = fields.Boolean(string="Totals")
    top_total_account_move = fields.Float(string="Top Totals Account Move (cm)")
    left_total_account_move = fields.Float(string="Left Totals Account Move (cm)")
    width_total_debit = fields.Float(string="Width Col Total Debit (cm)")
    width_total_credit = fields.Float(string="Width Col Total Credit (cm)")
    
    
    def set_draft(self):
        self.view_id.unlink()
        self.report_id.unlink()
        self.paper_format.unlink()
        return self.write({'state': 'draft'})
    
    def set_done(self):
        name_view = 'Check ' + str(self.name)
        name_report = str("format_checkprint.")+ str(name_view.replace(" ","_"))
        name_report = name_report.lower()
        arch_base = """<?xml version="1.0"?>
                <t t-name="{xml_report_name}">
                    <t t-call="web.html_container">
                        <t t-foreach="docs" t-as="o">
                            <t  t-if="o.state == 'posted'" t-esc="o.check_do()"/>
                            <div class="article">
                                <div class="page" style="font-family:'cool_font'">                            
                                    """.format(xml_report_name = name_report)
        if self.date:
            date = """<strong>{country} <strong t-field='o.{field_date}' """.format(country = self.env.company.country_id.name, field_date = self.date_field.name)
            if self.type_date == 'simple':
                date += str("""t-options="{'format': 'dd/MM/YYYY'}"/>""")
            if self.type_date == 'mix0':
                date += str("""t-options="{'format': 'dd of MMMM '}"/>""")
                date += """<strong t-field='o.{field_date}' """.format(field_date = self.date_field.name)
                date += str("""t-options="{'format': ', YYYY '}"/>""")
            if self.type_date == 'mix1':
                date += str("""t-options="{'format': 'MMMM dd '}"/>""")
                date += """<strong t-field='o.{field_date}' """.format(field_date = self.date_field.name)
                date += str("""t-options="{'format': ', YYYY '}"/>""")
            date += """</strong>"""
            arch_base += """<div style="font-size: 110%; position: absolute; top: {top_date}cm; left: {left_date}cm; font-family:'cool_font'; width: 15cm">
                                        {xml_date}
                                    </div>
                                    """.format(xml_date = date, top_date = self.top_date, left_date = self.left_date)
        
        if self.amount:
            amount = """<strong>"""
            currency_symbol = self.env.company.currency_id.symbol
            if self.currency_amount == 'before':
                amount+="""{currency}""".format(currency = currency_symbol)
            if self.type_amount == 'simple':
                amount+=str("""<strong t-esc="'{:,.2f}'.format(o.amount)"/>""")
            if self.type_amount == 'symbol':
                amount+="""{pre_symbol}""".format(pre_symbol = self.pre_symbol)
                amount+=str("""<strong t-esc="'{:,.2f}'.format(o.amount)"/>""")
                amount+="""{post_symbol}""".format(post_symbol = self.post_symbol)
            if self.currency_amount == 'after':
                amount+="""{currency}""".format(currency = currency_symbol)
            amount += """</strong>"""
            arch_base += """<div style="font-size: 110%; position: absolute; top: {top_amount}cm; left: {left_amount}cm">
                                        {xml_amount}
                                    </div>
                                    """.format(xml_amount = amount, top_amount = self.top_amount, left_amount = self.left_amount)
        
        if self.amount:
            partner = """<strong>
                                            """
            if self.type_partner == 'company':
                partner+="""<t t-if="o.partner_id.parent_id"><t t-esc='o.partner_id.parent_id.name'/></t>
                                            <t t-if="not o.partner_id.parent_id"><t t-esc='o.partner_id.name'/></t>
                                        """
            if self.type_partner == 'direct':
                partner+="""<t t-esc='o.partner_id.name'/>
                                        """
            partner += """</strong>"""
            arch_base += """<div style="font-size: 110%; position: absolute; top: {top_partner}cm; left: {left_partner}cm; width: 15cm">
                                        {xml_partner}
                                    </div>
                                    """.format(xml_partner = partner, top_partner = self.top_partner, left_partner = self.left_partner)
        
        if self.amount_letters:
            amount_letters = """<strong>"""
            currency_letter = self.env.company.currency_id.currency_unit_label
            if self.type_amount_letter == 'simple':
                amount_letters+=str("""<strong t-esc="o.check_amount_in_words"/>""")
            if self.type_amount_letter == 'symbol':
                amount_letters+="""{pre_symbol}""".format(pre_symbol = self.pre_symbol_letter)
                amount_letters+=str("""<strong t-esc="o.check_amount_in_words"/>""")
                amount_letters+="""{post_symbol}""".format(post_symbol = self.post_symbol_letter)
            if self.currency_amount_letter == 'after':
                amount_letters+="""{currency}""".format(currency = currency_letter)
            amount_letters += """</strong>"""
            arch_base += """<div style="font-size: 110%; text-transform: capitalize; position: absolute; top: {top_amount_letters}cm; left: {left_amount_letters}cm; width:18cm; font-family:'Calibri'; letter-spacing: 0.1em">
                                        {xml_amount_letter}
                                    </div>
                                    """.format(xml_amount_letter = amount_letters, top_amount_letters = self.top_amount_letters, left_amount_letters = self.left_amount_letters) 
        
        if self.negotiable:
            arch_base += """<div style="font-size: 110%; position: absolute; top: {top_negotiable}cm; left: {left_negotiable}cm; width: 5cm">
                                        <strong>NO NEGOTIABLE</strong>
                                    </div>
                                    """.format(top_negotiable = self.top_negotiable, left_negotiable = self.left_negotiable)
             
        if self.voucher:
            if self.description != 'none':
                description = """<strong>
                                            """
                
                if self.description == 'payment':
                    description += """<span t-esc="o.{field_description}"/>""".format(field_description = self.field_description.name)
                    
                if self.description == "invoices":
                    fields_description = """"""
                    for field_span in self.fields_description:
                        if field_span.ttype == 'many2one':
                            fields_description += """<span t-esc="o.{field_name}.name"/>, 
                                                """.format(field_name = field_span.name)
                        else:
                            fields_description += """<span t-esc="o.{field_name}"/>, 
                                                """.format(field_name = field_span.name)
                    description += """<t t-foreach="o.invoice_vendor_bill_id" t-as="invoice">
                                                {fields_description}
                                            </t>""".format(fields_description = fields_description)
                
                description += """</strong>"""
                arch_base += """<div style="position: absolute; top: {top_description}cm; left: {left_description}cm; width: 20cm">
                                        {xml_description}
                                    </div>
                                    """.format(xml_description = description, top_description = self.top_description, left_description = self.left_description)
        
            if self.account_move:
                arch_base += """<div style="font-size: 110%; position: absolute; top: {top_account_move}cm; left: {left_account_move}cm">
                                        <table>
                                            <tbody>
                                                <t t-set="debit" t-value="0"/>
                                                <t t-set="credit" t-value="0"/>
                                                 <tr t-foreach="o.line_ids" t-as="l">
                                                    <td style="font-size: 100%; width: {width_code}cm">
                                                        <strong t-field="l.account_id.code"/>
                                                    </td>
                                                    <td style="font-size: 100%; width: {width_name}cm">
                                                        <strong t-field="l.account_id.name"/>
                                                    </td>
                                                    <td style="font-size: 100%; width: {width_debit}cm; text-align:right;">
                                                        """.format(top_account_move = self.top_account_move, left_account_move = self.left_account_move, width_code = self.width_code, width_name = self.width_name, width_debit = self.width_debit)
                arch_base += str("""<strong t-field="l.debit" t-esc-options="{'widget': 'monetary', 'display_currency': o.currency_id}"/>
                                                    """)
                arch_base += """<t t-set="debit" t-value="debit+l.debit"/>
                                                    </td>
                                                    <td style="font-size: 100%; width: {width_credit}cm; text-align:right;">
                                                        """.format(width_credit = self.width_credit)
                arch_base += str("""<strong t-field="l.credit" t-esc-options="{'widget': 'monetary', 'display_currency': o.currency_id}"/>
                                                        <t t-set="credit" t-value="credit+l.credit"/>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </div>
                                    """)

            if self.total_account_move:
                arch_base += """<div style="font-size: 110%; position: absolute; top: {top_total_account_move}cm; left: {left_total_account_move}cm; width: 5cm">
                                        <table>
                                            <tbody>
                                                <tr t-foreach="o.line_ids" t-as="l">
                                                    <td style="font-size: 100%; width: {width_total_credit}cm">
                                                        """.format(top_total_account_move = self.top_total_account_move, left_total_account_move = self.left_total_account_move, width_total_credit = self.width_total_credit)
                arch_base += str("""<strong t-esc="debit" t-options="{'widget': 'monetary', 'display_currency': o.currency_id}"/>
                                                    </td>
                                                    """)
                arch_base += """<td style="font-size: 100%; width: {width_total_debit}cm">
                                                        """.format(width_total_debit = self.width_total_debit)
                arch_base += str("""<strong t-esc="credit" t-options="{'widget': 'monetary', 'display_currency': o.currency_id}"/>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </div>
                                    """)

        arch_base += """
                                </div>
                            </div>
                        </t>
                    </t>
                </t>"""
        
        vals_view = {
            'name': 'View ' + name_view,
            'type': 'qweb',
            'priority': 16,
            'active': True,
            'mode': 'primary',
            'arch_base': arch_base,
        }
        view_report = self.env['ir.ui.view'].create(vals_view)
        name_report_id = name_view.replace(" ","_")
        name_report_id = name_report_id.lower()
        vals_view_id = {
            'module': 'format_checkprint',
            'name': name_report_id,
            'model': 'ir.ui.view',
            'res_id': view_report.id
        }
        view_report_id = self.env['ir.model.data'].create(vals_view_id)
        vals_paper = {
            'name': 'Paper ' + str(self.name),
            'format': 'custom',
            'orientation': self.orientation,
            'page_height': self.page_height,
            'page_width': self.page_width,
            'margin_top': 0.00,
            'margin_bottom': 0.00,
            'margin_left': 0.00,
            'margin_right': 0.00,
            'header_spacing': 0,
            'dpi': 90
            }
        paperformat = self.env['report.paperformat'].create(vals_paper)
        data_models = self.env['ir.model'].search([('model', '=', 'account.payment')])
        binding_model = False
        for binding in data_models:
            binding_model = binding.id
        vals_report_id = {
            'name': name_view,
            'report_type': 'qweb-pdf',
            'paperformat_id': paperformat.id,
            'model': 'account.payment',
            'binding_model_id': binding_model,
            'report_name': name_report,
        }
        report_id = self.env['ir.actions.report'].create(vals_report_id)
        self.write({'view_id': view_report})
        self.write({'paper_format': paperformat})
        self.write({'report_id': report_id})
        self.write({'state': 'done'})
        return 