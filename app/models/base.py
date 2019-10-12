from app import db

def to_json(inst, cls, ignore=[]):
    """
    Jsonify the sql alchemy query result.
    """
    convert = dict()
    # add your coversions for things like datetime's 
    # and what-not that aren't serializable.
    d = dict()
    for c in cls.__table__.columns:
        if c.name in ignore:
            continue
        v = getattr(inst, c.name)
        if c.type in convert.keys() and v is not None:
            try:
                d[c.name] = convert[c.type](v)
            except:
                d[c.name] = "Error:  Failed to covert using ", str(convert[c.type])
        elif v is None:
            d[c.name] = str()
        else:
            d[c.name] = v
    return d


class BaseModel(db.Model):
    """Base data model for all objects"""
    __abstract__ = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def json(self, ignore=[]):
        return to_json(self, self.__class__, ignore)

    @staticmethod
    def json_list(lst, ignore=[]):
        return [i.json(ignore) for i in lst]

    def add_to_db(self):
        db.session.add(self)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()