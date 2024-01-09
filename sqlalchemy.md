pip3 install sqlalchemy

python3
>>> import sqlalchemy
>>> sqlalchemy.__version__
>>> from sqlalchemy import create_engine
>>> engine = create_engine("sqlite:///:memory:", echo=True)
>>> from sqlalchemy.orm import declarative_base
>>> Base = declarative_base()

>>> class User(Base):
...   __tablename__ = "users"
...   id = Column(Integer, primary_key=True)
...   name = Column(String)
...   fullname = Column(String)
...   nickname = Column(String)
...   def __repr__(self):
...     return "<User(name='%s', fullname='%s', nickname='%s')>" % (
...       self.name,
...       self.fullname,
...       self.nickname,
...     )
...

>>> User.__table__

>>> Base.metadata.create_all(engine)
>>> user1 = User(name="jazzy", fullname="Jasmine Dahilig", nickname="jazzyfresh")

>>> Session = sessionmaker(bind=engine)
>>> session = Session()
>>> session.add(user1)
>>> session.add_all(
...   [
...     User(name="dondi", fullname="John David Dionisio", nickname="dondi"),
...     User(name="ray", fullname="Ray Toal", nickname="rtoal"),
...   ]
... )

>>> session.new

>>> session.commit()
