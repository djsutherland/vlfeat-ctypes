# from dsift import vl_dsift
# from imsmooth import vl_imsmooth
# from phow import vl_phow

# Not doing actual imports here until the functions are called, because
# otherwise "python -m vlfeat.download" doesn't work (since it first loads
# this __init__, which loads things that nead the actual lib, which crashes...).
#
# TODO: do lazy-import in a way that doesn't break docstrings and such

def vl_dsift(*args, **kwargs):
    from .dsift import vl_dsift as f
    return f(*args, **kwargs)

def vl_imsmooth(*args, **kwargs):
    from .imsmooth import vl_imsmooth as f
    return f(*args, **kwargs)

def vl_phow(*args, **kwargs):
    from .phow import vl_phow as f
    return f(*args, **kwargs)

def vl_kmeans(*args, **kwargs):
    from .kmeans import vl_kmeans as f
    return f(*args, **kwargs)
