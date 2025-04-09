{
    'name': 'Hospital Managment',
     # "sequence": -101,
    'depends': ['base'],
    'author': 'Aya Ayamn',
    'category': 'Management',
    'description': 'A custom module for hospital management',
    'data': [
        'views/patients_views.xml',
        'views/departments_views.xml',
        'views/doctors_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}