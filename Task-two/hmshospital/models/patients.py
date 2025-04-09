from odoo import models, fields, api
from odoo.exceptions import ValidationError
class Patient(models.Model):
    _name = 'hospital.patients'
    _description = 'Hospital Patient'

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    birth_date = fields.Date(string='Birth Date')
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    address = fields.Text(string='Address')
    doctors_id = fields.Many2many('hospital.doctors', string='Doctors')
    department_id = fields.Many2one('hospital.departments', string='Department')
    capacity_id = fields.Integer(related='department_id.capacity', string="Capacity")
    history_log = fields.One2many('hospital.patient.log','patients_id',string='History Log')
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')
    ], string="State", default='undetermined')
    cr_ratio = fields.Float(string='CR Ratio')
    pcr = fields.Boolean(string='PCR')
    history = fields.Text(string='History')
    blood_type = fields.Selection([
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-')
    ], string='Blood Type')

    image = fields.Binary(string='Image')



    @api.depends('birth_date')
    def _compute_age(self):
        for record in self:
            if record.birth_date:
                today = fields.Date.today()
                record.age = today.year - record.birth_date.year - (
                    (today.month, today.day) < (record.birth_date.month, record.birth_date.day)
                )
            else:
                record.age = 0
    @api.onchange('department_id')
    def _onchange_department_id(self):
        if self.department_id:
            self.doctor_ids = False
            return {'domain': {'doctor_ids': []}}
        return {'domain': {'doctor_ids': [('id', '=', False)]}}

    @api.onchange('age')
    def _onchange_age(self):
        if self.age < 30:
            self.pcr = True
            return {'warning': {'title': 'PCR Checked', 'message': 'PCR has been automatically checked as age is below 30.'}}
        elif self.age >= 50:
            self.history_log = False

    @api.onchange('history_log','age')
    def _onchange_age(self):
        for record in self:
            if record.age >=50:
               record.history_log = False

    @api.constrains('pcr', 'cr_ratio')
    def _check_cr_ratio(self):
        for record in self:
            if record.pcr and not record.cr_ratio:
                raise ValidationError("CR Ratio is mandatory when PCR is checked.")

