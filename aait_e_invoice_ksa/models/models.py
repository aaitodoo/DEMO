# -*- coding: utf-8 -*-
from odoo import fields , models , api , _

# class AccountMoveLine(models.Model):
#     _inherit = "account.move.line"
    
#     tax_amount= fields.Monetary(string='Tax Amount' ,store=True, readonly=True,currency_field='currency_id')
    

class AccountMoveInherit(models.Model):
    _inherit = "account.move"

    # @api.onchange('line_ids.balance,line_ids.quantity,line_ids.price_unit,line_ids.discount')
    # def get_tax_amount(self):
    #     for this in self:
    #         for line in this.line_ids:
    #             if line.tax_line_id:
    #                 line.tax_amount=line.balance - (line.quantity*(line.price_unit *((1-line.discount)/100.0)))

    @api.onchange('partner_id')
    def _onchange_partner_warning_vat(self):
        if not self.partner_id:
            return
        partner = self.partner_id
        warning = {}
        if partner.company_type == 'company' and not partner.vat:
            title = ("Warning for %s") % partner.name
            message = _("Please add VAT ID for This Partner '%s' !") % (partner.name)
            warning = {
                'title': title,
                'message': message,
            }
        if warning:
            res = {'warning': warning}
            return res

    def write(self, vals):
        res = super(AccountMoveInherit, self).write(vals)
        if self.journal_id.type == 'sale' and self.company_id.id==1 and len(self.preview_invoice())==1:
            self.get_qr_code_data()
        return res

    def get_qr_code_data(self):
        customer_name = ""
        customer_vat = ""
        if self.company_id.id==1:
            if self.move_type in ('out_invoice', 'out_refund'):
                sellername = str(self.company_id.name)
                seller_vat_no = self.company_id.vat or ''
                if self.partner_id.company_type == 'company':
                    customer_name = self.partner_id.name
                    customer_vat = self.partner_id.vat
            else:
                sellername = str(self.partner_id.name)
                seller_vat_no = self.partner_id.vat
                customer_name = self.company_id.name
                customer_vat = self.company_id.vat

            qr_code = " Seller Name: " + sellername
            qr_code += "\n  Seller VAT NO.: " + seller_vat_no if seller_vat_no else " "
            qr_code += "\n  Date: " + str(self.invoice_date) if self.invoice_date else str(self.create_date)
            qr_code += "\n  Total Tax: " + str(self.amount_tax)
            qr_code += "\n  Total Amount: " + str(self.amount_total)
            if customer_name:
                qr_code += "\n  Customer Name: " + customer_name
            if customer_vat:
                qr_code += "\n  Customer Vat: " + customer_vat
            if self.journal_id.type == 'sale':
                qr_code += " \n \n  Invoice URL : "+self.env["ir.config_parameter"].get_param("web.base.url")+self.preview_invoice()['url']
        # print(qr_code)
        return qr_code


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    @api.onchange('partner_id')
    def _onchange_partner_warning_vat(self):
        if not self.partner_id:
            return
        partner = self.partner_id
        warning = {}
        if partner.company_type == 'company' and not partner.vat:
            title = ("Warning for %s") % partner.name
            message = _("Please add VAT ID for This Partner '%s' !"+"من فضلك قم باضافه الرقم الضريبي للعميل") % (partner.name)
            warning = {
                'title': title,
                'message': message,
            }
        if warning:
            res = {'warning': warning}
            return res


class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'

    @api.onchange('partner_id')
    def _onchange_partner_warning_vat(self):
        if not self.partner_id:
            return
        partner = self.partner_id
        warning = {}
        if partner.company_type == 'company' and not partner.vat:
            title = ("Warning for %s") % partner.name
            message = _("Please add VAT ID for This Partner '%s' !"+"من فضلك قم باضافه الرقم الضريبي للمورد") % (partner.name)
            warning = {
                'title': title,
                'message': message,
            }
        if warning:
            res = {'warning': warning}
            return res

