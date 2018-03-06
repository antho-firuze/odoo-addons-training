# -*- coding: utf-8 -*-
{
	'name': "academic",

	'summary': """
		Academic Information System Day 1
	""",

	'description': """
			Academic Information System Day 1
	""",

	'author': "antho.firuze@gmail.com",
	'website': "http://www.hdgroup.id",

	'category': 'Uncategorized',
	'version': '0.1',

	'depends': [
		'base',
		'mail',
		'board',
	],

	'data': [
		'menu.xml',
		'views/course.xml',
		'views/session.xml',
		'views/attendee.xml',
		'views/instructor.xml',
		'security/group.xml',
		'security/ir.model.access.csv',
		'wizard/create_attendee.xml',
		'report/session.xml',
		'views/dashboard.xml',
	],

	'installable': True,
	'application': True, 
	'auto_install': False, 
}