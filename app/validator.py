def validate(data, validationClass):
    valid_info = validationClass(data)
    if valid_info.validate():
        print('success')
    else:
        print('error')
    def decorator(func):
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
        return wrapper
    return decorator