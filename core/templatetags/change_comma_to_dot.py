from django.template import Library

register = Library()

def change_comma_to_dot(number):
    number_changed = str(number).replace(',','.')
    return number_changed

register.filter('change_comma_to_dot', change_comma_to_dot)