from sqlalchemy.ext.automap import automap_base
from database.session import engine

Base = automap_base()

Base.prepare(autoload_with=engine)