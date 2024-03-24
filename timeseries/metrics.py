from sklearn.metrics import mean_absolute_error
from sklearn.metrics import f1_score


def calculate_mae(array1, array2):
    mae = mean_absolute_error(array1, array2)
    return mae


def calculate_f1(array1, array2):
    f1 = f1_score(array1, array2)
    return f1
