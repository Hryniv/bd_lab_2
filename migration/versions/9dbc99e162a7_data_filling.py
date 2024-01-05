"""data filling

Revision ID: 9dbc99e162a7
Revises: 565e0590aa2b
Create Date: 2023-12-29 14:25:06.891863

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from models import Base, Applicant, Registration, UkrTest, Pt, Eo
from old_model import ZNO2020

# revision identifiers, used by Alembic.
revision: str = '9dbc99e162a7'
down_revision: Union[str, None] = '565e0590aa2b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    engine = create_engine('postgresql://postgres:1234@localhost/ZNO2020')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    for model in [Applicant, UkrTest, Pt, Eo, Registration]:
        session.query(model).delete()

    session.commit()

    zno_records = session.query(ZNO2020).limit(100).all()

    for zno_record in zno_records:
        registration = Registration(
            reg_name=zno_record.regname,
            reg_type_name=zno_record.regtypename,
            area_name=zno_record.areaname,
            ter_name=zno_record.tername,
            ter_type_name=zno_record.tertypename)

        session.add(registration)
        session.commit()

        eo = Eo(
            name=zno_record.eoname,
            type_name=zno_record.eotypename,
            parent=zno_record.eoparent,
            region_name=zno_record.eoregname,
            area_name=zno_record.eoareaname,
            ter_name=zno_record.eotername)

        session.add(eo)
        session.commit()

        pt = Pt(
            name=zno_record.classprofilename,
            region_name=zno_record.regname,
            area_name=zno_record.areaname,
            ter_name=zno_record.tername)

        session.add(pt)
        session.commit()

        ukr_test = UkrTest(
            status=zno_record.ukrteststatus,
            language=zno_record.classlangname,
            ball100=float(zno_record.ukrball100.replace(',', '.')) if zno_record.ukrball100
                                                                      and zno_record.ukrball100.lower() != 'null' else None,
            ball12=None if zno_record.ukrball12 == 'null' else zno_record.ukrball12,
            ball=None if zno_record.ukrball == 'null' else zno_record.ukrball,
            adapt_scale=zno_record.ukradaptscale,
            pt_id=pt.pt_id)

        session.add(ukr_test)
        session.commit()

        applicant = Applicant(
            out_id=zno_record.outid,
            birth=zno_record.birth,
            reg_id=registration.reg_id,
            sex_type_name=zno_record.sextypename,
            class_profile_name=zno_record.classprofilename,
            class_lang_name=zno_record.classlangname,
            eo_id=eo.eo_id,
            ukr_test_id=ukr_test.test_id)

        session.add(applicant)
        session.commit()

    session.close()


def downgrade() -> None:
    engine = create_engine('postgresql://postgres:1234@localhost/ZNO2020')

    # Create tables
    Base.metadata.create_all(bind=engine)

    # Create a session
    session = Session(engine)

    # Delete all records in reverse order to maintain foreign key constraints
    for model in [Applicant, UkrTest, Pt, Eo, Registration]:
        session.query(model).delete()

    # Commit the changes
    session.commit()

    # Close the session
    session.close()
