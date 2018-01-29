import os
import csv
import json
from collections import OrderedDict
from copy import deepcopy

os.environ["DJANGO_SETTINGS_MODULE"] = "nvc.settings"


def get_csv_dict(csv_filename):
    with open(csv_filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        rows = [row for row in reader]

    keys = rows[0]
    values = rows[1:]

    csv_dict = OrderedDict()

    for index, key in enumerate(keys):
        csv_dict[key.lower()] = [value[index] for value in values if value[index] != ""]

    return csv_dict


def get_all_feelings_dict():
    return OrderedDict({'emotional': get_csv_dict('emotions.csv'),
                        'mental': get_csv_dict('mental-states.csv'),
                        'physical': get_csv_dict('physical-states.csv')})


def get_all_feelings_list():
    return [get_csv_dict('emotions.csv'),
            get_csv_dict('mental-states.csv'),
            get_csv_dict('physical-states.csv'), ]


def make_feelings_main_category_fixture():
    fixture_list = [
        {
            "model": "entries.FeelingMainCategory",
            "pk": 1,
            "fields": {"feeling_main_category": "emotional"}
        },
        {
            "model": "entries.FeelingMainCategory",
            "pk": 2,
            "fields": {"feeling_main_category": "mental"}
        },
        {
            "model": "entries.FeelingMainCategory",
            "pk": 3,
            "fields": {"feeling_main_category": "physical"}
        }
    ]

    with open(os.path.join('../fixtures', 'feelings_main_cat.json'), 'w') as fixture_file:
        json.dump(fixture_list, fixture_file, indent=4)


def make_feelings_sub_category_fixture():
    idx = 1
    fixture_list = []
    for main_category, sub_category_dict in get_all_feelings_dict().items():
        foreign_key = {'emotional': 1, 'mental': 2, 'physical': 3}.get(main_category)
        for feeling_sub_cat in sub_category_dict.keys():
            fixture_list.append({
                "model": "entries.FeelingSubCategory",
                "pk": idx,
                "fields": {
                    "feeling_sub_category": feeling_sub_cat.lower(),
                    "feeling_main_category": foreign_key
                }
            })

            idx += 1

    with open(os.path.join('../fixtures', 'feelings_sub_cat.json'), 'w') as fixture_file:
        json.dump(fixture_list, fixture_file, indent=4)


def make_feelings_leaf_fixture():
    idx = 1
    fk_idx = 0
    fixture_list = []
    for main_category, sub_category_dict in get_all_feelings_dict().items():
        main_fk = {'emotional': 1, 'mental': 2, 'physical': 3}.get(main_category)
        for sub_cat, feeling_leaf_list in sub_category_dict.items():
            fk_idx += 1
            for feeling_leaf in list(filter(lambda x: x != "", feeling_leaf_list)):
                fixture_list.append({
                    "model": "entries.FeelingLeaf",
                    "pk": idx,
                    "fields": {
                        "feeling_leaf": feeling_leaf.lower(),
                        "feeling_sub_category": fk_idx,
                        "feeling_main_category": main_fk
                    }
                })
                idx += 1

    with open(os.path.join('../fixtures', 'feelings_leaf.json'), 'w') as fixture_file:
        json.dump(fixture_list, fixture_file, indent=4)


def make_need_category_fixture():
    fixture_list = []
    for idx, need_cat in enumerate(get_csv_dict('needs.csv').keys()):
        fixture_list.append({
            "model": "entries.NeedCategory",
            "pk": idx + 1,
            "fields": {
                "need_category": need_cat
            }
        })

    with open(os.path.join('../fixtures', 'needs_cat.json'), 'w') as fixture_file:
        json.dump(fixture_list, fixture_file, indent=4)


def make_need_leaf_fixture():
    fk_idx = 0
    idx = 1
    fixture_list = []
    for need_cat, need_list in get_csv_dict('needs.csv').items():
        fk_idx += 1
        for need_leaf in list(filter(lambda x: x != "", need_list)):
            fixture_list.append({
                "model": "entries.NeedLeaf",
                "pk": idx,
                "fields": {
                    "need_leaf": need_leaf,
                    "need_category": fk_idx
                }
            })
            idx += 1

    with open(os.path.join('../fixtures', 'needs_leaf.json'), 'w') as fixture_file:
        json.dump(fixture_list, fixture_file, indent=4)


def main():
    make_feelings_main_category_fixture()
    make_feelings_sub_category_fixture()
    make_feelings_leaf_fixture()
    make_need_category_fixture()
    make_need_leaf_fixture()


if __name__ == '__main__':
    main()
