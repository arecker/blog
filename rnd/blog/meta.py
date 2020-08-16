def descendants(cls):
    subclasses = []

    for subclass in cls.__subclasses__():
        subclasses.append(subclass)
        subclasses.extend(descendants(subclass))

    return subclasses
