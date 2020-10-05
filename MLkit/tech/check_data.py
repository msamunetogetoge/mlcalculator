def raise_err_cls(data_type):
    if data_type in ["int64", "O"]:
        pass
    else:
        raise Exception
def raise_err_reg(data_type):
    if data_type == "float64":
        pass
    else:
        raise Exception

def check_data_type(model,data_type):
    if model == "regression":
        try:
            raise_err_reg(data_type)
        except Exception :
            return "abon"
    if model == "classification":
        try:
            raise_err_cls(data_type)
        except Exception :
            return "abon"