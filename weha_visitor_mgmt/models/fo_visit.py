# -*- coding: utf-8 -*-
##############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2017-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Maintainer: Cybrosys Technologies (<https://www.cybrosys.com>)
##############################################################################

import datetime
from odoo import models, fields, api, _


class VisitDetails(models.Model):
    _name = 'fo.visit'
    _inherit = ['mail.thread']
    _description = 'Visit'

    name = fields.Char(string="sequence", default=lambda self: _('New'))
    visitor = fields.Many2one("fo.visitor", string='Visitor')
    phone = fields.Char(string="Phone", required=True)
    email = fields.Char(string="Email", required=True)
    reason = fields.Many2many('fo.purpose', string='Purpose Of Visit', required=True,
                              help='Enter the reason for visit')
    visitor_belongings = fields.One2many('fo.belongings', 'belongings_id_fov_visitor', string="Personal Belongings",
                                         help='Add the belongings details here.')
    check_in_date = fields.Datetime(string="Check In Time", help='Visitor check in time automatically'
                                                                 ' fills when he checked in to the office.')
    check_out_date = fields.Datetime(string="Check Out Time", help='Visitor check out time automatically '
                                                                   'fills when he checked out from the office.')
    visiting_person = fields.Many2one('hr.employee',  string="Meeting With")
    department = fields.Many2one('hr.department',  string="Department")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('check_in', 'Checked In'),
        ('check_out', 'Checked Out'),
        ('cancel', 'Cancelled'),
    ], track_visibility='onchange', default='draft')

    @api.model
    def create(self, vals):
        if vals:
            vals['name'] = self.env['ir.sequence'].next_by_code('fo.visit') or _('New')
            result = super(VisitDetails, self).create(vals)
            return result

    def action_cancel(self):
        self.state = "cancel"

    def action_check_in(self):
        self.state = "check_in"
        self.check_in_date = datetime.datetime.now()

    def action_check_out(self):
        self.state = "check_out"
        self.check_out_date = datetime.datetime.now()

    @api.onchange('visitor')
    def visitor_details(self):
        if self.visitor:
            if self.visitor.phone:
                self.phone = self.visitor.phone
            if self.visitor.email:
                self.email = self.visitor.email

    @api.onchange('visiting_person')
    def get_employee_dpt(self):
        if self.visiting_person:
            self.department = self.visiting_person.department_id


class VisitPurpose(models.Model):
    _name = 'fo.purpose'

    name = fields.Char(string='Purpose', required=True, help='Meeting purpose in short term.eg:Meeting.')
    description = fields.Text(string='Description Of Purpose', help='Description for the Purpose.')






