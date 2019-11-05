import datetime
import sys


def add_cls(record, packet, forms, err=sys.stderr):
    """
    Adds CLS form to packet.

    According to the IVP Guidebook (v3.0, March 2015), Form CLS should be
    completed if the subject or co-participant indicates that the subject is
    Hispanic/Latino.

    Therefore, if the subject is not Hispanic/Latino, do not add a CLS.

    IVP Guidebook:
      https://www.alz.washington.edu/NONMEMBER/UDS/DOCS/VER3/UDS3_ivp_guidebook.pdf

    Form CLS:
      https://www.alz.washington.edu/NONMEMBER/UDS/DOCS/VER3/CLS/CLS_en.pdf
    """

    fields_mapping = {
        'APREFLAN': 'eng_preferred_language',
        'AYRSPAN': 'eng_years_speak_spanish',
        'AYRENGL': 'eng_years_speak_english',
        'APCSPAN': 'eng_percentage_spanish',
        'APCENGL': 'eng_percentage_english',
        'ASPKSPAN': 'eng_proficiency_spanish',
        'AREASPAN': 'eng_proficiency_read_spanish',
        'AWRISPAN': 'eng_proficiency_write_spanish',
        'AUNDSPAN': 'eng_proficiency_oral_spanish',
        'ASPKENGL': 'eng_proficiency_speak_english',
        'AREAENGL': 'eng_proficiency_read_english',
        'AWRIENGL': 'eng_proficiency_write_english',
        'AUNDENGL': 'eng_proficiency_oral_english',
    }

    num_filled_fields = 0
    total_fields = len(fields_mapping)
    cls_form = forms.FormCLS()

    for key, val in fields_mapping.items():
        if record[val].strip():
            setattr(cls_form, key, record[val])
            num_filled_fields += 1

    # If every field is blank, return
    if num_filled_fields == 0:
        return

    # If only some of the fields are filled, make note.
    ptid = record.get('ptid', 'unknown')
    if num_filled_fields != total_fields:
        msg = "[WARNING] CLS form is incomplete for PTID: " \
            + ptid
        print(msg, file=err)

    # Otherwise, check percentages and dates before appending.

    # Check percentages
    try:
        pct_spn = int(record['eng_percentage_spanish'])
    except ValueError:
        msg = "[WARNING] eng_percentage_spanish is not an " \
            "integer for PTID: " + ptid
        print(msg, file=err)

    try:
        pct_eng = int(record['eng_percentage_english'])
    except ValueError:
        msg = "[WARNING] eng_percentage_english is not an " \
            "integer for PTID: " + ptid
        print(msg, file=err)

    if pct_eng + pct_spn != 100:
        msg = "[WARNING] language proficiency " + \
            "percentages do not equal 100 for PTID : " + ptid
        print(msg, file=err)

    visit_date = datetime.datetime(
        int(record['visityr']), int(record['visitmo']), 1)
    cls_added = datetime.datetime(2017, 6, 1)
    if visit_date < cls_added:
        message = "CLS forms should not be in " + \
            "packets from before June 1, 2017 for PTID: " + ptid
        raise Exception(message)

    if record['form_cls_linguistic_history_of_subject_complete'] != '2':
        message = "Could not parse packet as completed CLS form is not " + \
            "marked complete in REDCap for PTID: " + ptid
        raise Exception(message)

    packet.append(cls_form)
