import json
from unittest import mock, TestCase

from app.commands.list_players import Players
from tests.utils import get_fixture, FIXTURES_PATH


class ListPlayersTests(TestCase):
    def setUp(self) -> None:
        self.data = json.loads(get_fixture(f'{FIXTURES_PATH}/my_players.html'))['players']
        self.players = Players(self.data)

    def test_total_players_content(self):
        self.assertEqual(32, len(self.players.players_content()))

    def test_get_percent_when_0(self):
        self.assertEqual(0.0, self.players.get_percent_skill('width: 0px;'))

    def test_get_percent_when_0_25(self):
        self.assertEqual(0.25, self.players.get_percent_skill('width: 2px;'))

    def test_get_percent_when_0_5(self):
        self.assertEqual(0.5, self.players.get_percent_skill('width: 4px;'))

    def test_get_percent_when_0_75(self):
        self.assertEqual(0.75, self.players.get_percent_skill('width: 6px;'))

    def test_get_percent_when_other(self):
        self.assertEqual(0.0, self.players.get_percent_skill('width: 99px;'))

    def test_get_number_when_is_number(self):
        self.assertEqual(8, self.players.get_number(value='(8)'))
        self.assertEqual(10, self.players.get_number(value='10.'))

    def test_get_number_when_is_none(self):
        self.assertEqual(0, self.players.get_number(value=''))

    @mock.patch('app.commands.list_players.logger')
    def test_get_number_when_text(self, logger_mock):
        self.players.get_number(value='String pega incorretamente')
        self.assertEqual(True, logger_mock.error.called)

    def test_calcule_skill(self):
        row = {
            'intelligence': '(8)',
            'intelligence_percent': 'width: 2px;'
        }
        result = self.players.calcule_skill(row, skill_name='intelligence')
        self.assertEqual(8.25, result)

    def test_parse(self):
        row = {
            'number': '\n\t\t\t14.\xa0',
            'name': 'Deivid Monteiro',
            'player_id': '210231716',
            'age': '27',
            'country': 'nocache-732/img/flags/s_br.gif',
            'value': '2\xa0731\xa0201 R$',
            'salary': '39\xa0185 R$',
            'total_balls': '62',
            'speed': '(8)',
            'speed_percent': 'width: 0px;',
            'stamina': '(9)',
            'stamina_percent': 'width: 0px;',
            'intelligence': '(8)',
            'intelligence_percent': 'width: 0px;',
            'passing': '(8)',
            'passing_percent': 'width: 0px;',
            'shooting': '(2)',
            'shooting_percent': 'width: 0px;',
            'heading': '(2)',
            'heading_percent': 'width: 0px;',
            'keeping': '(1)',
            'keeping_percent': 'width: 0px;',
            'ball_control': '(4)',
            'ball_control_percent': 'width: 0px;',
            'tackling': '(9)',
            'tackling_percent': 'width: 0px;',
            'aerial_passing': '(6)',
            'aerial_passing_percent': 'width: 0px;',
            'set_plays': '(5)',
            'set_plays_percent': 'width: 4px;',
            'experience': '(9)',
            'form': '(9)',
            'is_leal': True,
            'status_form': 'background-image: url(nocache-732/img/player/formgood.png)',
            'status_injury': 'background-image: url(nocache-732/img/player/injury_icon_bw.png)',
            'status_training_camp': 'background-image: url(nocache-732/img/player/icon_trainingcamp_bw.png)',
            'status_ycc': None
        }
        expected = {
            'number': 14,
            'name': 'Deivid Monteiro',
            'player_id': '210231716',
            'age': 27,
            'country': 'br',
            'value': 2731201,
            'salary': 39185,
            'total_balls': 62,
            'speed': 8.0,
            'stamina': 9.0,
            'intelligence': 8.0,
            'passing': 8.0,
            'shooting': 2.0,
            'heading': 2.0,
            'keeping': 1.0,
            'ball_control': 4.0,
            'tackling': 9.0,
            'aerial_passing': 6.0,
            'set_plays': 5.5,
            'experience': 9,
            'form': 9,
            'is_leal': True,
            'status_form': 'background-image: url(nocache-732/img/player/formgood.png)',
            'status_injury': 'background-image: url(nocache-732/img/player/injury_icon_bw.png)',
            'status_training_camp': 'background-image: url(nocache-732/img/player/icon_trainingcamp_bw.png)',
            'status_ycc': None
        }
        result = self.players.parser(row)
        self.assertEqual(expected, result)

    def test_get_infos(self):
        player_content = self.players.players_content()[0]
        result = self.players.get_infos(player_content)
        expected = {
            'number': '\n\t\t\t14.\xa0',
            'name': 'Deivid Monteiro',
            'player_id': '210231716',
            'age': '27',
            'country': 'nocache-732/img/flags/s_br.gif',
            'value': '2\xa0731\xa0201 R$',
            'salary': '39\xa0185 R$',
            'total_balls': '62',
            'speed': '(8)',
            'speed_percent': 'width: 0px;',
            'stamina': '(9)',
            'stamina_percent': 'width: 0px;',
            'intelligence': '(8)',
            'intelligence_percent': 'width: 0px;',
            'passing': '(8)',
            'passing_percent': 'width: 0px;',
            'shooting': '(2)',
            'shooting_percent': 'width: 0px;',
            'heading': '(2)',
            'heading_percent': 'width: 0px;',
            'keeping': '(1)',
            'keeping_percent': 'width: 0px;',
            'ball_control': '(4)',
            'ball_control_percent': 'width: 0px;',
            'tackling': '(9)',
            'tackling_percent': 'width: 0px;',
            'aerial_passing': '(6)',
            'aerial_passing_percent': 'width: 0px;',
            'set_plays': '(5)',
            'set_plays_percent': 'width: 4px;',
            'experience': '(9)',
            'form': '(9)',
            'is_leal': True,
            'status_form': 'background-image: url(nocache-732/img/player/formgood.png)',
            'status_injury': 'background-image: url(nocache-732/img/player/injury_icon_bw.png)',
            'status_training_camp': 'background-image: url(nocache-732/img/player/icon_trainingcamp_bw.png)',
            'status_ycc': None
        }
        self.assertEqual(expected, result)

    @mock.patch.object(Players, 'get_infos')
    @mock.patch.object(Players, 'parser')
    def test_method_get(self, get_infos_mocked, parser_mocked):
        list(self.players.get())
        self.assertEqual(32, get_infos_mocked.call_count)
        self.assertEqual(32, parser_mocked.call_count)
