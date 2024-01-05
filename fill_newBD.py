from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Applicant, Registration, UkrTest, Pt, Eo
from old_model import ZNO2020


def save_record(session, record):
    existing_applicant = session.query(Applicant).filter_by(out_id=record.outid).first()

    if not existing_applicant:
        registration = Registration(
            reg_name=record.regname,
            reg_type_name=record.regtypename,
            area_name=record.areaname,
            ter_name=record.tername,
            ter_type_name=record.tertypename)

        session.add(registration)
        session.commit()

        eo = Eo(
            name=record.eoname,
            type_name=record.eotypename,
            parent=record.eoparent,
            region_name=record.eoregname,
            area_name=record.eoareaname,
            ter_name=record.eotername)

        session.add(eo)
        session.commit()

        pt = Pt(
            name=record.classprofilename,
            region_name=record.regname,
            area_name=record.areaname,
            ter_name=record.tername)

        session.add(pt)
        session.commit()

        ukr_test = UkrTest(
            status=record.ukrteststatus,
            language=record.classlangname,
            ball100=float(record.ukrball100.replace(',', '.')) if record.ukrball100
                                                                  and record.ukrball100.lower() != 'null' else None,
            ball12=None if record.ukrball12 == 'null' else record.ukrball12,
            ball=None if record.ukrball == 'null' else record.ukrball,
            adapt_scale=record.ukradaptscale,
            pt_id=pt.pt_id)

        session.add(ukr_test)
        session.commit()

        applicant = Applicant(
            out_id=record.outid,
            birth=record.birth,
            reg_id=registration.reg_id,
            sex_type_name=record.sextypename,
            class_profile_name=record.classprofilename,
            class_lang_name=record.classlangname,
            eo_id=eo.eo_id,
            ukr_test_id=ukr_test.test_id)

        session.add(applicant)
        session.commit()


# Підключення до старої та нової бази даних
old_db_engine = create_engine('postgresql://postgres:1234@localhost/ZNO2020')
new_db_engine = create_engine('postgresql://postgres:1234@localhost/NEWZNO2020')

# Створення сесій для старої та нової бази даних
OldSession = sessionmaker(bind=old_db_engine)
NewSession = sessionmaker(bind=new_db_engine)

# Створення сесій для старої та нової бази даних
old_session = OldSession()
new_session = NewSession()

try:
    batch_size = 1000  # Розмір партії для обробки
    offset = 0

    while True:
        zno_records = old_session.query(ZNO2020).offset(offset).limit(batch_size).all()
        if not zno_records:
            break

        for zno_record in zno_records:
            save_record(new_session, zno_record)

        offset += batch_size

finally:
    old_session.close()
    new_session.close()
