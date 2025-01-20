from sqlmodel import create_engine

DATABASE_URL = "mysql+pymysql://firas:firas19idir@localhost/jciDB"

engine=create_engine(DATABASE_URL)
