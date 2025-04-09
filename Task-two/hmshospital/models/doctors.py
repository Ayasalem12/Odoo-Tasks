from odoo import fields,models

class HMSDepartment(models.Model):
    _name = "hospital.doctors"
    _description = 'Hospital Doctors'
    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    image = fields.Binary(string='Image')