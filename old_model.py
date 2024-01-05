from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ZNO2020(Base):
    __tablename__ = 'zno2020'

    outid = Column(String, primary_key=True)
    birth = Column(String)
    sextypename = Column(String)
    regname = Column(String)
    areaname = Column(String)
    tername = Column(String)
    regtypename = Column(String)
    tertypename = Column(String)
    classprofilename = Column(String)
    classlangname = Column(String)
    eoname = Column(String)
    eotypename = Column(String)
    eoregname = Column(String)
    eoareaname = Column(String)
    eotername = Column(String)
    eoparent = Column(String)
    ukrtest = Column(String)
    ukrteststatus = Column(String)
    ukrball100 = Column(String)
    ukrball12 = Column(String)
    ukrball = Column(String)
    ukradaptscale = Column(String)
    ukrptname = Column(String)
    ukrptregname = Column(String)
    ukrptareaname = Column(String)
    ukrpttername = Column(String)