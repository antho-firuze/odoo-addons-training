# -*- coding: utf-8 -*-

from odoo import models, fields, api
import time

SESSION_STATES = [('draft', 'Draft'), ('confirmed', 'Confirmed'), ('done', 'Done'), ('cancel', 'Cancel')]


class Session(models.Model):
  _name = 'academic.session'
  _inherit = 'mail.thread'

  name = fields.Char("Name", required=True, track_visibility='onchange', )
  course_id = fields.Many2one(comodel_name="academic.course", string="Course", required=False, track_visibility='onchange', )
  instructor_id = fields.Many2one(comodel_name="res.partner", string="Instructor", required=False, track_visibility='onchange', )
  start_date = fields.Date(string="Start Date", required=False, default=lambda self: time.strftime("%Y-%m-%d"), track_visibility='onchange', )
  duration = fields.Integer(string="Duration", required=False, track_visibility='onchange', )
  seats = fields.Integer(string="Seats", required=False, track_visibility='onchange', )
  is_active = fields.Boolean(string="Active", track_visibility='onchange', )
  attendee_ids = fields.One2many(comodel_name="academic.attendee", inverse_name="session_id", string="Attendees",
                                 required=False, track_visibility='onchange', )
  taken_seats = fields.Float(compute="_calc_taken_seats", string="Taken Seat", required=False, )
  image_small = fields.Binary(string="Image Small",  )

  _sql_constraints = [
    ('cek_unik_name', 'UNIQUE(name)', 'Name harus unik'),
  ]

  @api.depends('attendee_ids', 'seats')
  def _calc_taken_seats(self):
    for rec in self:
      if rec.seats > 0:
        rec.taken_seats = 100 * len(rec.attendee_ids) / rec.seats
      else:
        rec.taken_seats = 0

  @api.onchange('seats')
  def _onchange_seats(self):
    if self.seats > 0:
      self.taken_seats = 100 * len(self.attendee_ids) / self.seats
    else:
      self.taken_seats = 0.0

  @api.multi
  def _cek_instructor(self):
    for session in self:
      x = [att.partner_id.id for att in session.attendee_ids]
      if session.instructor_id.id in x:
        return False
      return True

  _constraints = [(_cek_instructor, 'Instructor cannot be Attendee', ['instructor_id', 'attendee_ids'])]

  @api.multi
  def copy(self, default=None):
    self.ensure_one()
    default = dict(default or {}, name=('%s (Copy)' % self.name))
    return super(Session, self).copy(default=default)

  state = fields.Selection(string="State", selection=SESSION_STATES,
                           required=True,
                           readonly=True,
                           default=SESSION_STATES[0][0], track_visibility='onchange', )

  @api.multi
  def action_draft(self):
    self.state = SESSION_STATES[0][0]

  @api.multi
  def action_confirm(self):
    self.state = SESSION_STATES[1][0]

  @api.multi
  def action_done(self):
    self.state = SESSION_STATES[2][0]

  @api.multi
  def action_cancel(self):
    self.state = SESSION_STATES[3][0]
