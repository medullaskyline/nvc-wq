import os
import csv
import json
from copy import deepcopy

os.environ["DJANGO_SETTINGS_MODULE"] = "nvc.settings"


def get_all_feelings_dict():
    return {'emotional': get_csv_dict('emotions.csv'),
            'physical': get_csv_dict('physical-states.csv'),
            'mental': get_csv_dict('mental-states.csv')}


def get_csv_dict(csv_filename):
    with open(csv_filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        rows = [row for row in reader]

    keys = rows[0]
    values = rows[1:]

    # todo: can this be clearer?
    return {key.lower(): [value_row[keys.index(key)].lower() for value_row in values if value_row[keys.index(key)]]
            for key in keys}


def make_needs_fixture():
    needs_dict = get_csv_dict('needs.csv')

    idx = 1
    fixture_list = []
    for category, needs_list in needs_dict.items():
        main_fix = {
            "model": "entries.Need",
            "fields": {"category": category}
        }
        for need in needs_list:
            need_fix = deepcopy(main_fix)
            need_fix['fields']['name'] = need
            need_fix['pk'] = idx
            fixture_list.append(need_fix)
            idx += 1

    with open(os.path.join('../fixtures', 'needs.json'), 'w') as fixture_file:
        json.dump(fixture_list, fixture_file, indent=4)


def make_feelings_fixture():
    feelings_dict = get_all_feelings_dict()

    idx = 1
    fixture_list = []
    for main_category, main_category_dict in feelings_dict.items():
        main_fix = {
            "model": "entries.Feeling",
            "fields": {"main_category": main_category}
        }
        for sub_category, feeling_list in main_category_dict.items():
            sub_fix = deepcopy(main_fix)
            sub_fix['fields']['sub_category'] = sub_category

            for feeling in feeling_list:
                feel_fix = deepcopy(sub_fix)
                feel_fix['fields']['name'] = feeling
                feel_fix['pk'] = idx
                fixture_list.append(feel_fix)
                idx += 1

    with open(os.path.join('../fixtures', 'feelings.json'), 'w') as fixture_file:
        json.dump(fixture_list, fixture_file, indent=4)



def main():
    # make_needs_fixture()
    make_feelings_fixture()


if __name__ == '__main__':
    main()
