# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.http import request
from odoo.tools import pdf, split_every

class AccountPayment(models.Model):
    _inherit = "account.payment"

    no_negociable = fields.Boolean(string='No negotiable')

    def print_checks(self):
        for rec in self:
            if rec.journal_id.checkprint_report:
                action_report = rec.journal_id.checkprint_report.report_id
                return action_report.report_action(self)
            else:
                raise ValidationError(_("You do not have a check format set in this journal, set a format in your journal or print it from the PRINT button"))
        return

    def check_do(self):
        for rec in self:
            rec.write({'is_move_sent': True})
        return

    def action_post(self):
        for payment in self:
            try:
                if not payment.check_number:
                    return super(AccountPayment, self).action_post()
                else:
                    temp_number = payment.check_number
                    temp_number_journal = int(payment.journal_id.check_next_number) + 1
                    res = super(AccountPayment, self).action_post()
                    payment.check_number = temp_number
                    payment.journal_id.write({'check_next_number':temp_number_journal})
            except:
                print("ERROR")

    def numbers_to_letters(self, num, complete=True):
        print(self.env.user.partner_id.lang)
        if 'en' in self.env.user.partner_id.lang:
            in_letter = {
                '0': 'zero',
                '1': 'one',
                '2': 'two',
                '3': 'three',
                '4': 'four',
                '5': 'five',
                '6': 'six',
                '7': 'seven',
                '8': 'eight',
                '9': 'nine',
                '10': 'ten',
                '11': 'eleven',
                '12': 'twelve',
                '13': 'thirteen',
                '14': 'fourteen',
                '15': 'fifteen',
                '16': 'sixteen',
                '17': 'seventeen',
                '18': 'eighteen',
                '19': 'nineteen',
                '2x': 'twenty',
                '3x': 'thirty',
                '4x': 'forty',
                '5x': 'fifty',
                '6x': 'sixty',
                '7x': 'seventy',
                '8x': 'eighty',
                '9x': 'ninety',
                '1xx': 'one hundred',
                '2xx': 'two hundred',
                '3xx': 'three hundred',
                '4xx': 'four hundred',
                '5xx': 'five hundred',
                '6xx': 'six hundred',
                '7xx': 'seven hundred',
                '8xx': 'eight hundred',
                '9xx': 'nine hundred',
                '1xxx': 'one thousand',
                'xxxxxx': 'thousand',
                '1xxxxxx': 'one million',
                'x:x': 'millions'
            }
        elif 'es' in self.env.user.partner_id.lang:
            in_letter = {
                '0': 'zero',
                '1': 'uno',
                '2': 'dos',
                '3': 'tres',
                '4': 'cuatro',
                '5': 'cinco',
                '6': 'seis',
                '7': 'siete',
                '8': 'ocho',
                '9': 'nueve',
                '10': 'diez',
                '11': 'once',
                '12': 'doce',
                '13': 'trece',
                '14': 'catorce',
                '15': 'quince',
                '16': 'dieciseis',
                '17': 'diecisiete',
                '18': 'dieciocho',
                '19': 'diecinueve',
                '20': 'veinte',
                '21': 'veintiuno',
                '22': 'veintidos',
                '23': 'veintitres',
                '24': 'veinticuatro',
                '25': 'veinticinco',
                '26': 'veintiseis',
                '27': 'veintisiete',
                '28': 'veintiocho',
                '29': 'veintinueve',
                '3x': 'treinta',
                '4x': 'cuarenta',
                '5x': 'cincuenta',
                '6x': 'sesenta',
                '7x': 'setenta',
                '8x': 'ochenta',
                '9x': 'noventa',
                '100': 'cien',
                '1xx': 'ciento',
                '2xx': 'dos cientos',
                '3xx': 'tres cientos',
                '4xx': 'cuatro cientos',
                '5xx': 'quinientos',
                '6xx': 'seis cientos',
                '7xx': 'sete cientos',
                '8xx': 'ocho cientos',
                '9xx': 'nove cientos',
                '1xxx': 'un mil',
                'xxxxxx': 'mil',
                '1xxxxxx': 'un millón',
                'x:x': 'millones'
            }
        else:
            return

        num_clean = str(num).replace(',', '')
        parts = num_clean.split('.')
        integer = 0
        decimal = 0
        if parts[0]:

            integer = str(int(parts[0]))
        if len(parts) > 1 and parts[1]:
            decimal = parts[1][0:2].ljust(2, '0')

        return_num_in_letter = 'ERROR'
        if int(integer) < 30:
            return_num_in_letter = in_letter[integer]
        elif int(integer) < 100:
            return_num_in_letter = in_letter[integer[0] + 'x']
            if integer[1] != '0':
                return_num_in_letter = return_num_in_letter + ' y ' + in_letter[integer[1]]
        elif int(integer) < 101:
            return_num_in_letter = in_letter[integer]
        elif int(integer) < 1000:
            return_num_in_letter = in_letter[integer[0] + 'xx']
            if integer[1:3] != '00':
                return_num_in_letter = return_num_in_letter + ' ' + self.numbers_to_letters(integer[1:3], False)
        elif int(integer) < 2000:
            return_num_in_letter = in_letter[integer[0] + 'xxx']
            if integer[1:4] != '000':
                return_num_in_letter = return_num_in_letter + ' ' + self.numbers_to_letters(integer[1:4], False)
        elif int(integer) < 1000000:
            thousands = int(integer.rjust(6)[0:3])
            hundreds = integer.rjust(6)[3:7]
            return_num_in_letter = self.numbers_to_letters(
                str(thousands), False) + ' ' + in_letter['xxxxxx']
            if hundreds != '000':
                return_num_in_letter = return_num_in_letter + ' ' + self.numbers_to_letters(hundreds, False)
        elif int(integer) < 2000000:
            return_num_in_letter = in_letter[integer[0] + 'xxxxxx']
            if integer[1:7] != '000000':
                return_num_in_letter = return_num_in_letter + ' ' + self.numbers_to_letters(integer[1:7], False)
        elif int(integer) < 1000000000000:
            millions = int(integer.rjust(12)[0:6])
            thousands = integer.rjust(12)[6:12]
            return_num_in_letter = self.numbers_to_letters(
                str(millions), False) + ' ' + in_letter['x:x']
            if thousands != '000000':
                return_num_in_letter = return_num_in_letter + ' ' + self.numbers_to_letters(thousands, False)
        if not complete:
            return return_num_in_letter
        if self.env.user.partner_id.lang == 'en':
            if decimal == 0:
                letters = '%s exactly' % return_num_in_letter
            else:
                letters = '%s with %s/100' % (return_num_in_letter, decimal)
        else: 
            if decimal == 0:
                letters = '%s exactos' % return_num_in_letter
            else:
                letters = '%s con %s/100' % (return_num_in_letter, decimal)
        self.write({'check_amount_in_words': letters})