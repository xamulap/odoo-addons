# -*- coding: utf-8 -*-
# Copyright © 2017 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, SUPERUSER_ID


def add_key_to_existing_invoices(cr, registry):
    """This post-init-hook will update all existing invoices"""
    env = api.Environment(cr, SUPERUSER_ID, {})
    invoice_obj = env['account.invoice']
    print invoice_obj
    invoices = invoice_obj.search([])
    if invoices:
        sii_key_obj = env['aeat.sii.mapping.registration.keys']
        sale_key = sii_key_obj.search(
            [('code', '=', '01'), ('type', '=', 'sale')],
            limit=1)
        purchase_key = sii_key_obj.search(
            [('code', '=', '01'), ('type', '=', 'purchase')],
            limit=1)
        print sale_key
        print purchase_key
        if purchase_key:
            cr.execute("""
                UPDATE account_invoice
                SET registration_key = %s
                WHERE type IN ('in_invoice', 'in_refund');""",
                       (purchase_key.id,))
        if sale_key:
            cr.execute("""
                UPDATE account_invoice
                SET registration_key = %s
                WHERE type NOT IN ('in_invoice', 'in_refund');""",
                       (sale_key.id,))
        cr.execute("""
            ALTER TABLE account_invoice
            ALTER COLUMN registration_key SET NOT NULL;
            """)