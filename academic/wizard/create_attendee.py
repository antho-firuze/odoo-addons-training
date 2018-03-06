# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)


class CreateAttendeeWizard(models.TransientModel):
  _name = 'academic.create.attendee.wizard'

  # def _get_active_session(self):
  #   context = self.env.context
  #   if context.get('active_model') == 'academic.session':
  #     return context.get('active_id', False)
  #   return False

  # session_id = fields.Many2one(comodel_name="academic.session", string="Session", required=False,
  #                              default=_get_active_session, )

  def _get_active_session(self):
    context = self.env.context

    _logger.error("my_variable : %r", context)

    if context.get('active_model') == 'academic.session':
      return context.get('active_ids', False)
    return False

  session_ids = fields.Many2many(comodel_name="academic.session", string="Sessions", )

  attendee_ids = fields.One2many(comodel_name="academic.attendee.wizard", inverse_name="wizard_id",
                                 string="Attendees to Add", required=False, )

  # create method
  @api.multi
  def action_add_attendee(self):
    # self.ensure_one()


    sessions = self.session_ids
    for session in sessions:
      # _logger.error("my_variable_:_%r", session)
      # return

      att_data = [{'partner_id': att.partner_id.id} for att in self.attendee_ids]
      session.attendee_ids = [(0, 0, data) for data in att_data]

    return {'type': 'ir.actions.act_window_close'}

  # create method & new
  @api.multi
  def action_add_attendee_new(self):
    self.ensure_one()

    session = self.session_id
    att_data = [{'partner_id': att.partner_id.id} for att in self.attendee_ids]
    session.attendee_ids = [(0, 0, data) for data in att_data]

    return {
      'type': 'ir.actions.act_window',
      'target': 'new',
      'view_type': 'form',
      'view_mode': 'form',
      'res_model': 'academic.create.attendee.wizard',
    }


class AttendeeWizard(models.TransientModel):
  _name = 'academic.attendee.wizard'

  wizard_id = fields.Many2one(comodel_name="academic.create.attendee.wizard", string="Wizard", required=False, )
  partner_id = fields.Many2one(comodel_name="res.partner", string="Partner", required=False, )
