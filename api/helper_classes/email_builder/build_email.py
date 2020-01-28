from jinja2 import Environment, PackageLoader, select_autoescape
import json

subject_from_type = {
	'email_confirmation': 'Sign up confirmation',
}

env = Environment(
	loader=PackageLoader('helper_classes.email_builder.build_email', 'templates'),
	autoescape=select_autoescape(['html']))


def build_email(recipient, email_type, **kwargs):
	email_data = {}

	template = env.get_template(email_type + '.html')

	email_data['body'] = template.render(**kwargs)
	email_data['subject'] = subject_from_type[email_type]
	email_data['recipient'] = recipient
	
	return email_data
