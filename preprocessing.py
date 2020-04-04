import numpy as np

def text_to_date(text):
    text = str(text)
    return np.datetime64('20' + text.split('/')[2] + '-' + text.split('/')[1] + '-' + text.split('/')[0])