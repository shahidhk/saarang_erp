from django.core.validators import RegexValidator


'''
This regex assumes that you have a clean string,
you should clean the string for spaces and other characters
'''

isalphavalidator = RegexValidator(r'^[\d]*$',
                             message='Enter valid mobile number',
                             code='Invalid name')