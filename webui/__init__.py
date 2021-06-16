from bankdb import *


def preprocess(data):
    """
    Do some preprocess to data parsed from front-end.
    1. `acc_type`: build from `Number` to `AccountType`
    :param data:
    :return:
    """
    if 'acc_type' in data:
        data['acc_type'] = account.AccountType.build(data['acc_type'])
    if data.get('cus_name') == '':
        data.pop('cus_name', None)
    if data.get('cus_id') == '':
        data.pop('cus_id', None)
    return data
