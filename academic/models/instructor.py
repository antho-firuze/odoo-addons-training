# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Instructor(models.Model):
  _inherit = 'res.partner'

  is_instructor = fields.Boolean(string="Is Instructor", )
