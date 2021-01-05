import json
import re
from typing import Iterable

from parsel import Selector

from app.const import MAPPING_KEY_TRAINING_REPORT, MAPPING_SKILL
from app.log import logger


class Players:
    def __init__(self, data):
        self.data = data

    def get(self) -> Iterable:
        for player_content in self.players_content():
            player = self.get_infos(player_content)
            yield player['player_id'], self.parser(player)

    def players_content(self) -> list:
        sel = Selector(text=self.data)
        return sel.xpath("//div[@id='players_container']/div").extract()

    @staticmethod
    def maximizations(body: str) -> list:
        regex = r"(\[.*\])"
        if match := re.findall(regex, body):
            data = json.loads(match[0])
        else:
            return []

        result = []
        for item in data:
            if item.get('showInNavigator') == 'false' and item['color'] == 'rgba(255,0,0,0.7)':
                code = item['data'][0]['y']
                result.append(MAPPING_KEY_TRAINING_REPORT[code])
        return result

    @staticmethod
    def count_stars(html: str) -> int:
        return html.count('fa fa-star fa-2x lit')

    @staticmethod
    def parser_skill(names: list) -> list:
        try:
            return [MAPPING_SKILL[name] for name in names]
        except KeyError:
            return []

    def scout_report(self, body: str) -> Iterable:
        if not body:
            return {}

        sel = Selector(body)
        potencial = sel.xpath("//dl/dd[1]//li[@class='blurred']/span[last()]//text()").extract()
        stars = sel.xpath("//div[@class='flex-grow-1']/span[@class='stars']").extract()
        return {
            'highest_potential': self.parser_skill(potencial[0:2]),
            'lowest_potential': self.parser_skill(potencial[2:4]),
            'highest_stars': self.count_stars(html=stars[0]),
            'lowest_stars': self.count_stars(html=stars[1]),
            'training_speed_stars': self.count_stars(html=stars[2])
        }

    @staticmethod
    def get_infos(player_content: str) -> dict:
        sel = Selector(text=player_content)

        return dict(
            number=sel.xpath("//a[@class='subheader']/text()").get(),
            name=sel.xpath("//span[@class='player_name']/text()").get(),
            player_id=sel.xpath("//span[@class='player_id_span']/text()").get(),
            age=sel.xpath("//table[1]//tr[1]/td[1]/strong/text()").get(),
            country=sel.xpath("//div[@class='dg_playerview_info']/table[1]//tr[4]/td/img/@src").get(),
            value=sel.xpath("//table[1]//tr[last() - 3]/td/span[@class='bold']/text()").get(),
            salary=sel.xpath("//table[1]//tr[last() - 2]/td/span[@class='bold']/text()").get(),
            total_balls=sel.xpath("//table[1]//tr[last() - 1]/td/span[@class='bold']/text()").get(),
            speed=sel.xpath("//tr[1]/td[@class='skillval']/text()").get(),
            speed_percent=sel.xpath("//tr[1]/td[@class='skill_exact']//div[@class='skill_exact_bar']//@style").get(),
            stamina=sel.xpath("//tr[2]/td[@class='skillval']/text()").get(),
            stamina_percent=sel.xpath("//tr[2]/td[@class='skill_exact']//div[@class='skill_exact_bar']//@style").get(),
            intelligence=sel.xpath("//tr[3]/td[@class='skillval']/text()").get(),
            intelligence_percent=sel.xpath("//tr[3]/td[@class='skill_exact']//div[@class='skill_exact_bar']//@style").get(),
            passing=sel.xpath("//tr[4]/td[@class='skillval']/text()").get(),
            passing_percent=sel.xpath("//tr[4]/td[@class='skill_exact']//div[@class='skill_exact_bar']//@style").get(),
            shooting=sel.xpath("//tr[5]/td[@class='skillval']/text()").get(),
            shooting_percent=sel.xpath("//tr[5]/td[@class='skill_exact']//div[@class='skill_exact_bar']//@style").get(),
            heading=sel.xpath("//tr[6]/td[@class='skillval']/text()").get(),
            heading_percent=sel.xpath("//tr[6]/td[@class='skill_exact']//div[@class='skill_exact_bar']//@style").get(),
            keeping=sel.xpath("//tr[7]/td[@class='skillval']/text()").get(),
            keeping_percent=sel.xpath("//tr[7]/td[@class='skill_exact']//div[@class='skill_exact_bar']//@style").get(),
            ball_control=sel.xpath("//tr[8]/td[@class='skillval']/text()").get(),
            ball_control_percent=sel.xpath("//tr[8]/td[@class='skill_exact']//div[@class='skill_exact_bar']//@style").get(),
            tackling=sel.xpath("//tr[9]/td[@class='skillval']/text()").get(),
            tackling_percent=sel.xpath("//tr[9]/td[@class='skill_exact']//div[@class='skill_exact_bar']//@style").get(),
            aerial_passing=sel.xpath("//tr[10]/td[@class='skillval']/text()").get(),
            aerial_passing_percent=sel.xpath("//tr[10]/td[@class='skill_exact']//div[@class='skill_exact_bar']//@style").get(),
            set_plays=sel.xpath("//tr[11]/td[@class='skillval']/text()").get(),
            set_plays_percent=sel.xpath("//tr[11]/td[@class='skill_exact']//div[@class='skill_exact_bar']//@style").get(),
            experience=sel.xpath("//tr[12]/td[@class='skillval']/text()").get(),
            form=sel.xpath("//tr[13]/td[@class='skillval']/text()").get(),
            is_leal=bool(sel.xpath("//div[@class='mainContent loyal_player_container']").get()),
            # Campos extras ainda não parseados
            status_form=sel.xpath("//div[@class='p_sublinks']/span[1]/span/span/span[@class='player_icon_image']/@style").get(),
            status_injury=sel.xpath("//div[@class='p_sublinks']/span[2]/span/span/span[@class='player_icon_image']/@style").get(),
            status_training_camp=sel.xpath("//div[@class='p_sublinks']/span[3]/span/span/span[@class='player_icon_image']/@style").get(),
            status_ycc=sel.xpath("//div[@class='p_sublinks']/span[4]/span/span/span[@class='player_icon_image']/@style").get(),
        )

    @staticmethod
    def get_percent_skill(value: str) -> float:
        if value == 'width: 2px;':
            return 0.25
        elif value == 'width: 4px;':
            return 0.5
        elif value == 'width: 6px;':
            return 0.75
        else:
            return 0.0

    @staticmethod
    def get_number(value: str) -> int:
        if value:
            try:
                return int(re.sub('[^0-9]', '', value))
            except ValueError:
                logger.error(f'Dado coletado incorretamente: O valor "{value}" deveria ser parseado um número')
        return 0

    def calcule_skill(self, row: dict, skill_name: str):
        absolute_number = self.get_number(row[skill_name])
        percente_number = self.get_percent_skill(row.pop(f'{skill_name}_percent'))
        return absolute_number + percente_number

    def parser(self, row: dict) -> dict:
        row['country'] = row['country'][-6:-4]
        row['number'] = self.get_number(row['number'])
        row['salary'] = self.get_number(row['salary'])
        row['value'] = self.get_number(row['value'])
        row['age'] = self.get_number(row['age'])
        row['total_balls'] = self.get_number(row['total_balls'])
        row['experience'] = self.get_number(row['experience'])
        row['form'] = self.get_number(row['form'])
        row['speed'] = self.calcule_skill(row, skill_name='speed')
        row['stamina'] = self.calcule_skill(row, skill_name='stamina')
        row['intelligence'] = self.calcule_skill(row, skill_name='intelligence')
        row['passing'] = self.calcule_skill(row, skill_name='passing')
        row['shooting'] = self.calcule_skill(row, skill_name='shooting')
        row['heading'] = self.calcule_skill(row, skill_name='heading')
        row['keeping'] = self.calcule_skill(row, skill_name='keeping')
        row['ball_control'] = self.calcule_skill(row, skill_name='ball_control')
        row['tackling'] = self.calcule_skill(row, skill_name='tackling')
        row['aerial_passing'] = self.calcule_skill(row, skill_name='aerial_passing')
        row['set_plays'] = self.calcule_skill(row, skill_name='set_plays')
        return row
