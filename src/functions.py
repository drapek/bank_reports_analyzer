def get_set_from_iter_by_attr(iterable_collection, attr_name):
    """
    This will concatenate all sets stored under "attr_name" param in given collection.
    :param iterable_collection:
    :param attr_name:
    :return:
    """
    global_set = set()
    for obj in iterable_collection:
        global_set = global_set.union(obj[attr_name])
    return global_set
