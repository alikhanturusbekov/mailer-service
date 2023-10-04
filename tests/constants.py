class ErrorMessage:
    MIN_LENGTH_1 = 'String should have at least 1 characters'
    MAX_LENGTH_255 = 'String should have at most 255 characters'

    INVALID_EMAIL_AT = ('value is not a valid email address: The email '
                        'address is not valid. It must have exactly one @-sign.')
    INVALID_EMAIL_DOT = ('value is not a valid email address: The part '
                         'after the @-sign is not valid. It should have a period.')
