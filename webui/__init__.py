from bankdb import *
from pyisemail import is_email


def preprocess_cus_id(value):
    if len(value) != 18:
        raise RuntimeError(f'cus_id length should be 18. check {value}.')
    if not value.isdigit():
        raise RuntimeError(f'cus_id should be digits. check {value}.')
    return value


def preprocess(data: dict):
    """
    Do some preprocess to data parsed from front-end.
    1. `acc_type`: build from `Number` to `AccountType`
    :param data:
    :return:
    """
    ret = {}
    for key, value in data.items():
        if value is None or value == '':
            continue
        elif key == 'cus_id':
            ret[key] = preprocess_cus_id(value)
        elif key == 'cus_ids':
            ret[key] = []
            for cus_id in value:
                ret[key].append(preprocess_cus_id(cus_id))
        elif key == 'cus_name':
            if len(value) > 16:
                raise RuntimeError(f'{key} should be less than 16 characters')
            ret[key] = value
        elif key == 'cus_phone':
            if len(value) > 16:
                raise RuntimeError(f'{key} should be less than 16 characters')
            if not value.isdigit():
                raise RuntimeError(f'{key} should be digits')
            ret[key] = value
        elif key == 'cus_address':
            if len(value) > 32:
                raise RuntimeError(f'{key} should be less than 32 characters')
            ret[key] = value
        elif key == 'con_name':
            if len(value) > 16:
                raise RuntimeError(f'{key} should be less than 16 characters')
            ret[key] = value
        elif key == 'con_phone':
            if len(value) > 16:
                raise RuntimeError(f'{key} should be less than 16 characters')
            if not value.isdigit():
                raise RuntimeError(f'{key} should be digits')
            ret[key] = value
        elif key == 'con_email':
            if len(value) > 32:
                raise RuntimeError(f'{key} should be less than 32 characters')
            if not is_email(value):
                raise RuntimeError(f'{key} is not a valid email address')
            ret[key] = value
        elif key == 'con_relation':
            if len(value) > 16:
                raise RuntimeError(f'{key} should be less than 16 characters')
            ret[key] = value
        elif key == 'acc_id':
            if len(value) != 16:
                raise RuntimeError(f'{key} length should be 16.')
            if not value.isdigit():
                raise RuntimeError(f'{key} should be digits')
            ret[key] = value
        elif key == 'acc_type':
            if type(value) == str:
                if value != 'STORE' and value != 'CHECK':
                    raise RuntimeError(f'{key} should be either STORE or CHECK in str')
            elif type(value) == int:
                if value != 0 and value != 1:
                    raise RuntimeError(f'{key} should be either 0 or 1 in int')
            ret[key] = account.AccountType.build(value)
        elif key == 'acc_balance':
            value = float(value)
            if value < 0:
                raise RuntimeError(f'{key} should be at least 0.')
            ret[key] = account.AccountType.build(value)
        elif key == 'che_overdraft':
            value = float(value)
            if value < 0:
                raise RuntimeError(f'{key} should be at least 0.')
            ret[key] = account.AccountType.build(value)
        elif key == 'sto_interest_rate':
            value = float(value)
            if value < 0:
                raise RuntimeError(f'{key} should be at least 0.')
            ret[key] = value
        elif key == 'sto_currency_type':
            if value != 'CNY' and value != 'USD':
                raise RuntimeError(f'{key} should be either CNY or USD')
            ret[key] = value
        elif key == 'loa_amount':
            value = float(value)
            if value < 0:
                raise RuntimeError(f'{key} should be at least 0.')
            ret[key] = value
        elif key == 'bra_name':
            if len(value) > 16:
                raise RuntimeError(f'{key} should be less than 16 characters')
            ret[key] = value
    return data
