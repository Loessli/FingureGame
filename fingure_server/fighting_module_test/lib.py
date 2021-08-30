from .hero_info import HeroInfo
from .skills import Skill
import csv


def loading_csv_config(csv_path: str) -> list:
    csv_data = []
    with open(csv_path) as csv_config:
        temp_data = csv.reader(csv_config)
        for temp in temp_data:
            csv_data.append(temp)
    return csv_data


def loading_skill_config(skill_conf: str) -> Skill:
    config = skill_conf.split(",")
    return Skill(config[0], config[1], config[2], config[3], config[4])


def loading_hero_info_config_by_id(csv_data: list, _id: int) -> HeroInfo:
    type_data = csv_data[0]
    real_conf = csv_data[_id][1:12]
    skill1 = loading_skill_config(real_conf[9])
    skill2 = loading_skill_config(real_conf[10])
    ctor_data = {}
    for i in range(len(real_conf)-2):
        ctor_data[type_data[i+1]] = real_conf[i]
    ctor_data["skill1"] = skill1
    ctor_data["skill2"] = skill2
    return HeroInfo(ctor_data)


