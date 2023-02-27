from dataclasses import dataclass

from flask import Blueprint, current_app

from controller.method import Method
from database import database
from entity import Coordinate
from service import CityService, RoadService, CoordinateService, PlaceService


@dataclass
class RoadFixture:
    latitude: float
    longitude: float
    neighbours: list[int]
    coordinate: Coordinate = None


@dataclass
class PlaceFixture:
    latitude: float
    longitude: float
    name: str
    address: str
    coordinate: Coordinate = None


def recreate_schema() -> None:
    with current_app.app_context():
        database.drop_all()
        database.create_all()


blueprint = Blueprint('fixtures', __name__, url_prefix='/fixtures')

city_service = CityService()
coordinate_service = CoordinateService()
road_service = RoadService()
place_service = PlaceService()

road_fixtures = {
    0: RoadFixture(longitude=131.88244, latitude=43.11630, neighbours=[1, 4]),
    1: RoadFixture(longitude=131.88549, latitude=43.11573, neighbours=[0, 2, 3]),
    2: RoadFixture(longitude=131.88826, latitude=43.11527, neighbours=[1, 5, 10]),
    3: RoadFixture(longitude=131.88631, latitude=43.11804, neighbours=[1, 4, 5, 11]),
    4: RoadFixture(longitude=131.88327, latitude=43.11862, neighbours=[0, 3, 12]),
    5: RoadFixture(longitude=131.88902, latitude=43.11753, neighbours=[2, 3, 6]),
    6: RoadFixture(longitude=131.89086, latitude=43.11791, neighbours=[5, 7, 8]),
    7: RoadFixture(longitude=131.89108, latitude=43.11902, neighbours=[6, 11, 15]),
    8: RoadFixture(longitude=131.89367, latitude=43.11732, neighbours=[6, 9, 32]),
    9: RoadFixture(longitude=131.89501, latitude=43.11579, neighbours=[8, 10]),
    10: RoadFixture(longitude=131.89457, latitude=43.11409, neighbours=[2, 9, 54]),
    11: RoadFixture(longitude=131.88694, latitude=43.11980, neighbours=[3, 7, 12, 14]),
    12: RoadFixture(longitude=131.88391, latitude=43.12038, neighbours=[4, 11, 13]),
    13: RoadFixture(longitude=131.88428, latitude=43.12152, neighbours=[12, 14, 18]),
    14: RoadFixture(longitude=131.88729, latitude=43.12092, neighbours=[11, 13, 15, 17]),
    15: RoadFixture(longitude=131.89147, latitude=43.12013, neighbours=[7, 14, 16]),
    16: RoadFixture(longitude=131.89186, latitude=43.12119, neighbours=[15, 17, 22]),
    17: RoadFixture(longitude=131.88771, latitude=43.12207, neighbours=[14, 16, 18, 20]),
    18: RoadFixture(longitude=131.88467, latitude=43.12269, neighbours=[13, 17, 19]),
    19: RoadFixture(longitude=131.88514, latitude=43.12377, neighbours=[18, 20, 21]),
    20: RoadFixture(longitude=131.88817, latitude=43.12316, neighbours=[17, 19, 21]),
    21: RoadFixture(longitude=131.88855, latitude=43.12432, neighbours=[19, 20, 23, 24]),
    22: RoadFixture(longitude=131.89201, latitude=43.12241, neighbours=[16, 23]),
    23: RoadFixture(longitude=131.89233, latitude=43.12428, neighbours=[21, 22, 25]),
    24: RoadFixture(longitude=131.89233, latitude=43.12811, neighbours=[21, 26]),
    25: RoadFixture(longitude=131.90222, latitude=43.12819, neighbours=[23, 26, 27, 40]),
    26: RoadFixture(longitude=131.89246, latitude=43.12902, neighbours=[24, 25, 39]),
    27: RoadFixture(longitude=131.90696, latitude=43.12670, neighbours=[25, 28, 37, 38]),
    28: RoadFixture(longitude=131.90359, latitude=43.12125, neighbours=[27, 29, 34, 35]),
    29: RoadFixture(longitude=131.90179, latitude=43.11920, neighbours=[28, 30, 35]),
    30: RoadFixture(longitude=131.89651, latitude=43.11527, neighbours=[29, 31, 32, 55]),
    31: RoadFixture(longitude=131.89636, latitude=43.11184, neighbours=[30]),
    32: RoadFixture(longitude=131.89662, latitude=43.11674, neighbours=[8, 30, 33]),
    33: RoadFixture(longitude=131.89995, latitude=43.11814, neighbours=[32, 34, 47]),
    34: RoadFixture(longitude=131.89928, latitude=43.11961, neighbours=[28, 33]),
    35: RoadFixture(longitude=131.90477, latitude=43.12030, neighbours=[28, 29, 36]),
    36: RoadFixture(longitude=131.90898, latitude=43.12495, neighbours=[35, 37, 38]),
    37: RoadFixture(longitude=131.91220, latitude=43.12677, neighbours=[27, 36, 44, 38]),
    38: RoadFixture(longitude=131.91031, latitude=43.12745, neighbours=[27, 36, 37, 41]),
    39: RoadFixture(longitude=131.89276, latitude=43.13018, neighbours=[26, 40]),
    40: RoadFixture(longitude=131.89984, latitude=43.13297, neighbours=[25, 39, 41]),
    41: RoadFixture(longitude=131.91147, latitude=43.13312, neighbours=[38, 40, 42, 43]),
    42: RoadFixture(longitude=131.90701, latitude=43.14408, neighbours=[41, 82, 124, 125, 170]),
    43: RoadFixture(longitude=131.91520, latitude=43.13215, neighbours=[41, 44, 179]),
    44: RoadFixture(longitude=131.92546, latitude=43.12266, neighbours=[37, 43, 45, 46, 63]),
    45: RoadFixture(longitude=131.93220, latitude=43.11959, neighbours=[44, 46]),
    46: RoadFixture(longitude=131.92181, latitude=43.11897, neighbours=[44, 45, 47]),
    47: RoadFixture(longitude=131.91842, latitude=43.11806, neighbours=[33, 46, 48]),
    48: RoadFixture(longitude=131.91756, latitude=43.11377, neighbours=[47, 49, 51]),
    49: RoadFixture(longitude=131.91722, latitude=43.11245, neighbours=[48, 50, 57]),
    50: RoadFixture(longitude=131.90782, latitude=43.11511, neighbours=[49, 51, 52]),
    51: RoadFixture(longitude=131.90821, latitude=43.11587, neighbours=[48, 50, 56]),
    52: RoadFixture(longitude=131.90490, latitude=43.11574, neighbours=[50, 53]),
    53: RoadFixture(longitude=131.90130, latitude=43.11477, neighbours=[52, 54, 55]),
    54: RoadFixture(longitude=131.89688, latitude=43.11377, neighbours=[10, 53]),
    55: RoadFixture(longitude=131.90259, latitude=43.11608, neighbours=[30, 53, 56]),
    56: RoadFixture(longitude=131.90610, latitude=43.11702, neighbours=[51, 55]),
    57: RoadFixture(longitude=131.92473, latitude=43.11217, neighbours=[49, 58, 59]),
    58: RoadFixture(longitude=131.93413, latitude=43.11279, neighbours=[57, 59, 61]),
    59: RoadFixture(longitude=131.93408, latitude=43.11132, neighbours=[57, 58, 60]),
    60: RoadFixture(longitude=131.93795, latitude=43.10960, neighbours=[59, 61]),
    61: RoadFixture(longitude=131.93610, latitude=43.11314, neighbours=[58, 60, 62]),
    62: RoadFixture(longitude=131.94018, latitude=43.12808, neighbours=[61, 63, 64, 185]),
    63: RoadFixture(longitude=131.92911, latitude=43.12980, neighbours=[44, 62]),
    64: RoadFixture(longitude=131.94773, latitude=43.13428, neighbours=[62, 65]),
    65: RoadFixture(longitude=131.94850, latitude=43.13936, neighbours=[64, 66, 188]),
    66: RoadFixture(longitude=131.95310, latitude=43.14581, neighbours=[65, 67]),
    67: RoadFixture(longitude=131.95292, latitude=43.14985, neighbours=[66, 68]),
    68: RoadFixture(longitude=131.95447, latitude=43.15088, neighbours=[67, 69]),
    69: RoadFixture(longitude=131.95314, latitude=43.15363, neighbours=[68, 70]),
    70: RoadFixture(longitude=131.94516, latitude=43.15968, neighbours=[69, 71, 113]),
    71: RoadFixture(longitude=131.94074, latitude=43.16365, neighbours=[70, 72, 87]),
    72: RoadFixture(longitude=131.94215, latitude=43.16562, neighbours=[71, 73]),
    73: RoadFixture(longitude=131.93305, latitude=43.16897, neighbours=[72, 74, 85, 87]),
    74: RoadFixture(longitude=131.92748, latitude=43.16910, neighbours=[73, 75]),
    75: RoadFixture(longitude=131.92220, latitude=43.16916, neighbours=[74, 76, 83]),
    76: RoadFixture(longitude=131.91482, latitude=43.16766, neighbours=[75, 77, 168]),
    77: RoadFixture(longitude=131.91383, latitude=43.16450, neighbours=[76, 78, 83]),
    78: RoadFixture(longitude=131.91331, latitude=43.16356, neighbours=[77, 79, 86, 169]),
    79: RoadFixture(longitude=131.91108, latitude=43.15542, neighbours=[78, 80, 100]),
    80: RoadFixture(longitude=131.90786, latitude=43.15154, neighbours=[79, 81, 131]),
    81: RoadFixture(longitude=131.90632, latitude=43.14928, neighbours=[80, 82, 130]),
    82: RoadFixture(longitude=131.90598, latitude=43.14737, neighbours=[42, 81, 125]),
    83: RoadFixture(longitude=131.92215, latitude=43.16542, neighbours=[75, 77, 84]),
    84: RoadFixture(longitude=131.92728, latitude=43.16683, neighbours=[83, 85]),
    85: RoadFixture(longitude=131.93239, latitude=43.16688, neighbours=[73, 84]),
    86: RoadFixture(longitude=131.91520, latitude=43.16331, neighbours=[78, 87, 88]),
    87: RoadFixture(longitude=131.93280, latitude=43.16628, neighbours=[71, 73, 86]),
    88: RoadFixture(longitude=131.91696, latitude=43.16033, neighbours=[86, 89]),
    89: RoadFixture(longitude=131.92198, latitude=43.16168, neighbours=[88, 90, 96]),
    90: RoadFixture(longitude=131.92962, latitude=43.16365, neighbours=[89, 91]),
    91: RoadFixture(longitude=131.93035, latitude=43.16354, neighbours=[90, 92]),
    92: RoadFixture(longitude=131.92926, latitude=43.16026, neighbours=[91, 93]),
    93: RoadFixture(longitude=131.92814, latitude=43.15996, neighbours=[92, 94, 102]),
    94: RoadFixture(longitude=131.92664, latitude=43.15958, neighbours=[93, 95, 101]),
    95: RoadFixture(longitude=131.92404, latitude=43.16038, neighbours=[94, 96]),
    96: RoadFixture(longitude=131.92321, latitude=43.15988, neighbours=[89, 95, 97]),
    97: RoadFixture(longitude=131.92346, latitude=43.15889, neighbours=[96, 98, 101]),
    98: RoadFixture(longitude=131.92353, latitude=43.15708, neighbours=[97, 99, 101, 148]),
    99: RoadFixture(longitude=131.91364, latitude=43.15576, neighbours=[98, 100]),
    100: RoadFixture(longitude=131.91297, latitude=43.15528, neighbours=[79, 99, 133, 147]),
    101: RoadFixture(longitude=131.92664, latitude=43.15736, neighbours=[94, 97, 98, 102]),
    102: RoadFixture(longitude=131.92715, latitude=43.15719, neighbours=[93, 101, 103, 152]),
    103: RoadFixture(longitude=131.92833, latitude=43.15683, neighbours=[102, 104, 108]),
    104: RoadFixture(longitude=131.92825, latitude=43.15924, neighbours=[103, 105]),
    105: RoadFixture(longitude=131.93166, latitude=43.16054, neighbours=[104, 106]),
    106: RoadFixture(longitude=131.93460, latitude=43.15903, neighbours=[105, 107]),
    107: RoadFixture(longitude=131.93464, latitude=43.15640, neighbours=[106, 108, 109]),
    108: RoadFixture(longitude=131.93084, latitude=43.15615, neighbours=[103, 107]),
    109: RoadFixture(longitude=131.93670, latitude=43.15520, neighbours=[107, 110]),
    110: RoadFixture(longitude=131.94099, latitude=43.15413, neighbours=[109, 111, 114]),
    111: RoadFixture(longitude=131.94005, latitude=43.16102, neighbours=[110, 112]),
    112: RoadFixture(longitude=131.94250, latitude=43.16168, neighbours=[111, 113]),
    113: RoadFixture(longitude=131.94387, latitude=43.15990, neighbours=[70, 112]),
    114: RoadFixture(longitude=131.93563, latitude=43.15307, neighbours=[110, 115]),
    115: RoadFixture(longitude=131.93602, latitude=43.15088, neighbours=[114, 116]),
    116: RoadFixture(longitude=131.93057, latitude=43.14690, neighbours=[115, 117]),
    117: RoadFixture(longitude=131.92769, latitude=43.14380, neighbours=[116, 118]),
    118: RoadFixture(longitude=131.92705, latitude=43.14221, neighbours=[117, 119]),
    119: RoadFixture(longitude=131.92597, latitude=43.14136, neighbours=[118, 120, 129]),
    120: RoadFixture(longitude=131.92430, latitude=43.14083, neighbours=[119, 121]),
    121: RoadFixture(longitude=131.92185, latitude=43.14167, neighbours=[120, 122]),
    122: RoadFixture(longitude=131.91555, latitude=43.14086, neighbours=[121, 123]),
    123: RoadFixture(longitude=131.91379, latitude=43.14462, neighbours=[122, 124]),
    124: RoadFixture(longitude=131.91057, latitude=43.14365, neighbours=[42, 123]),
    125: RoadFixture(longitude=131.91031, latitude=43.14834, neighbours=[42, 82, 126]),
    126: RoadFixture(longitude=131.91207, latitude=43.14900, neighbours=[125, 127, 130, 136]),
    127: RoadFixture(longitude=131.91761, latitude=43.14756, neighbours=[126, 128, 145]),
    128: RoadFixture(longitude=131.91958, latitude=43.14693, neighbours=[127, 129]),
    129: RoadFixture(longitude=131.92147, latitude=43.14352, neighbours=[119, 128]),
    130: RoadFixture(longitude=131.91065, latitude=43.15022, neighbours=[81, 126, 131, 137]),
    131: RoadFixture(longitude=131.90979, latitude=43.15078, neighbours=[80, 130, 132]),
    132: RoadFixture(longitude=131.91147, latitude=43.15420, neighbours=[131, 133]),
    133: RoadFixture(longitude=131.91306, latitude=43.15407, neighbours=[100, 132, 134]),
    134: RoadFixture(longitude=131.91503, latitude=43.15376, neighbours=[133, 135, 147]),
    135: RoadFixture(longitude=131.91422, latitude=43.15150, neighbours=[134, 136, 138]),
    136: RoadFixture(longitude=131.91344, latitude=43.15006, neighbours=[126, 135, 137, 145]),
    137: RoadFixture(longitude=131.91160, latitude=43.15066, neighbours=[130, 136]),
    138: RoadFixture(longitude=131.91712, latitude=43.15074, neighbours=[135, 139, 140, 145]),
    139: RoadFixture(longitude=131.91742, latitude=43.15144, neighbours=[138]),
    140: RoadFixture(longitude=131.91776, latitude=43.15057, neighbours=[138, 141, 143]),
    141: RoadFixture(longitude=131.91946, latitude=43.15071, neighbours=[140, 142]),
    142: RoadFixture(longitude=131.91984, latitude=43.14920, neighbours=[141]),
    143: RoadFixture(longitude=131.91838, latitude=43.15038, neighbours=[140, 144]),
    144: RoadFixture(longitude=131.91908, latitude=43.14905, neighbours=[143]),
    145: RoadFixture(longitude=131.91813, latitude=43.14877, neighbours=[127, 136, 138, 146]),
    146: RoadFixture(longitude=131.92076, latitude=43.14797, neighbours=[145]),
    147: RoadFixture(longitude=131.91540, latitude=43.15494, neighbours=[100, 134, 148]),
    148: RoadFixture(longitude=131.92280, latitude=43.15548, neighbours=[98, 147, 149]),
    149: RoadFixture(longitude=131.92228, latitude=43.15393, neighbours=[148, 150]),
    150: RoadFixture(longitude=131.92497, latitude=43.15179, neighbours=[149, 151]),
    151: RoadFixture(longitude=131.93033, latitude=43.15075, neighbours=[150]),
    152: RoadFixture(longitude=131.92718, latitude=43.15559, neighbours=[102, 153]),
    153: RoadFixture(longitude=131.93065, latitude=43.15518, neighbours=[152, 154, 156]),
    154: RoadFixture(longitude=131.92595, latitude=43.15409, neighbours=[153, 155, 166]),
    155: RoadFixture(longitude=131.92565, latitude=43.15312, neighbours=[154, 167]),
    156: RoadFixture(longitude=131.93207, latitude=43.15496, neighbours=[153, 157]),
    157: RoadFixture(longitude=131.93202, latitude=43.15398, neighbours=[156, 158, 161]),
    158: RoadFixture(longitude=131.93314, latitude=43.15329, neighbours=[157, 159]),
    159: RoadFixture(longitude=131.93280, latitude=43.15100, neighbours=[158, 160]),
    160: RoadFixture(longitude=131.93147, latitude=43.15119, neighbours=[159, 161]),
    161: RoadFixture(longitude=131.93078, latitude=43.15251, neighbours=[157, 160, 162]),
    162: RoadFixture(longitude=131.93069, latitude=43.15113, neighbours=[161, 163]),
    163: RoadFixture(longitude=131.92902, latitude=43.15229, neighbours=[162, 164]),
    164: RoadFixture(longitude=131.92898, latitude=43.15320, neighbours=[163, 165]),
    165: RoadFixture(longitude=131.92758, latitude=43.15323, neighbours=[164, 166]),
    166: RoadFixture(longitude=131.92724, latitude=43.15284, neighbours=[154, 165, 167]),
    167: RoadFixture(longitude=131.92700, latitude=43.15248, neighbours=[155, 166]),
    168: RoadFixture(longitude=131.90477, latitude=43.16497, neighbours=[76, 169]),
    169: RoadFixture(longitude=131.90752, latitude=43.16130, neighbours=[78, 168]),
    170: RoadFixture(longitude=131.91027, latitude=43.14258, neighbours=[42, 171]),
    171: RoadFixture(longitude=131.90864, latitude=43.14108, neighbours=[170, 172]),
    172: RoadFixture(longitude=131.90941, latitude=43.14030, neighbours=[171, 173]),
    173: RoadFixture(longitude=131.91490, latitude=43.13782, neighbours=[172, 174]),
    174: RoadFixture(longitude=131.92662, latitude=43.13666, neighbours=[173, 175, 180]),
    175: RoadFixture(longitude=131.92632, latitude=43.13497, neighbours=[174, 176]),
    176: RoadFixture(longitude=131.92490, latitude=43.13344, neighbours=[175, 177]),
    177: RoadFixture(longitude=131.92168, latitude=43.13294, neighbours=[176, 178]),
    178: RoadFixture(longitude=131.91992, latitude=43.13203, neighbours=[177, 179]),
    179: RoadFixture(longitude=131.91610, latitude=43.13262, neighbours=[43, 178]),
    180: RoadFixture(longitude=131.93125, latitude=43.13720, neighbours=[174, 181]),
    181: RoadFixture(longitude=131.93597, latitude=43.13601, neighbours=[180, 182, 186]),
    182: RoadFixture(longitude=131.93606, latitude=43.13378, neighbours=[181, 183]),
    183: RoadFixture(longitude=131.93799, latitude=43.13394, neighbours=[182, 184]),
    184: RoadFixture(longitude=131.93645, latitude=43.13309, neighbours=[183, 185]),
    185: RoadFixture(longitude=131.94031, latitude=43.12949, neighbours=[62, 184]),
    186: RoadFixture(longitude=131.94224, latitude=43.13663, neighbours=[181, 187]),
    187: RoadFixture(longitude=131.94576, latitude=43.13835, neighbours=[186, 188]),
    188: RoadFixture(longitude=131.95305, latitude=43.13754, neighbours=[65, 187]),
}

place_fixtures = {
    0: PlaceFixture(longitude=131.88534, latitude=43.11527, name='Площадь Победы', address='Площадь Победы'),
    1: PlaceFixture(longitude=131.88526, latitude=43.11514, name='Сухой фонтан', address='Площадь Победы'),
    2: PlaceFixture(longitude=131.88671, latitude=43.11511, name='Стела «Город воинской славы»',
                    address='Ленинский район'),
    3: PlaceFixture(longitude=131.88714, latitude=43.11458, name='Спасо-Преображенский кафедральный собор',
                    address='Ленинский район'),
    4: PlaceFixture(longitude=131.87977, latitude=43.11670, name='Версаль', address='Фрунзенский район'),
    5: PlaceFixture(longitude=131.89243, latitude=43.11392, name='Триумфальная арка', address='Ленинский район'),
    6: PlaceFixture(longitude=131.89825, latitude=43.11752, name='Вид на залив "Золотой рог"',
                    address='Ленинский район'),
    7: PlaceFixture(longitude=131.90092, latitude=43.11446, name='Военно-исторический музей Тихоокеанского флота',
                    address='Ленинский район, 66'),
    8: PlaceFixture(longitude=131.91563, latitude=43.16324, name='Яхонт', address='Первореченский район, 1'),
    9: PlaceFixture(longitude=131.88217, latitude=43.11636, name='Музей им. Арсеньева',
                    address='Фрунзенский район, 20'),
    10: PlaceFixture(longitude=131.93725, latitude=43.13407, name='Вираж', address='Первореченский район, 17А с1'),
    11: PlaceFixture(longitude=131.90454, latitude=43.12578, name='Аванта', address='Ленинский район'),
    12: PlaceFixture(longitude=131.89490, latitude=43.12514, name='Авизо', address='Ленинский район, 16/18'),
    13: PlaceFixture(longitude=131.89344, latitude=43.12453, name='Приморская государственная картинная галерея',
                     address='Ленинский район, 12'),
    14: PlaceFixture(longitude=131.93369, latitude=43.14827, name='Днепровская 90а', address='Первореченский район'),
    15: PlaceFixture(longitude=131.91081, latitude=43.16263, name='Акфес Сейо', address='Первореченский район, 103'),
    16: PlaceFixture(longitude=131.88608, latitude=43.11697, name='Скульптура Воспоминание о моряке загранплавания',
                     address='Ленинский район'),
    17: PlaceFixture(longitude=131.89507, latitude=43.11410, name='Музей Ростелекома', address='Ленинский район'),
    18: PlaceFixture(longitude=131.89123, latitude=43.11270, name='Морские прогулки на катере',
                     address='Ленинский район'),
    19: PlaceFixture(longitude=131.88759, latitude=43.12028, name='Сибирское Подворье', address='Ленинский район, 26А'),
    20: PlaceFixture(longitude=131.91605, latitude=43.11489, name='Mini Hotel Graal', address='Ленинский район, 2'),
    21: PlaceFixture(longitude=131.91416, latitude=43.11237, name='Самурай', address='Ленинский район'),
    22: PlaceFixture(longitude=131.91497, latitude=43.11520, name='Busse Mini-hotel', address='Ленинский район, 19'),
    23: PlaceFixture(longitude=131.90161, latitude=43.12713, name='Астория', address='Ленинский район, 44 к6'),
    24: PlaceFixture(longitude=131.89931, latitude=43.11806, name='Арка любви', address='Ленинский район'),
    25: PlaceFixture(longitude=131.88377, latitude=43.11973, name='Изба', address='Фрунзенский район, 3 с1'),
    26: PlaceFixture(longitude=131.88446, latitude=43.11627, name='Антилопа', address='Фрунзенский район, 23А'),
    27: PlaceFixture(longitude=131.93333, latitude=43.12895, name='Гранит', address='Ленинский район, 13'),
    28: PlaceFixture(longitude=131.90313, latitude=43.16798, name='Bay garden', address='Советский район, 23Д к2'),
    29: PlaceFixture(longitude=131.90500, latitude=43.16547, name='Дружба', address='Советский район, 3'),
    30: PlaceFixture(longitude=131.88031, latitude=43.11731, name='Филин и Сова', address='Фрунзенский район, 5А'),
    31: PlaceFixture(longitude=131.89068, latitude=43.11853, name='Гостевой дом Ли', address='Ленинский район, 17'),
    32: PlaceFixture(longitude=131.91417, latitude=43.11636, name='Вид на город', address='Ленинский район'),
    33: PlaceFixture(longitude=131.89283, latitude=43.11368, name='Музей города', address='Ленинский район, 6'),
    34: PlaceFixture(longitude=131.88727, latitude=43.12296, name='Каштан', address='Фрунзенский район, 10А'),
    35: PlaceFixture(longitude=131.88764, latitude=43.12219, name='Capsule Hotel ALOHA',
                     address='Фрунзенский район, 29'),
    36: PlaceFixture(longitude=131.89659, latitude=43.11994, name='Статуя Будды', address='Ленинский район'),
    37: PlaceFixture(longitude=131.90218, latitude=43.11790, name='Смотровая площадка', address='Ленинский район'),
    38: PlaceFixture(longitude=131.90589, latitude=43.16118, name='Набережная на Второй Речке',
                     address='Советский район'),
    39: PlaceFixture(longitude=131.88079, latitude=43.11738, name='Галерея Арка', address='Фрунзенский район, 4В'),
    40: PlaceFixture(longitude=131.90365, latitude=43.16617, name='Томь', address='Советский район, 23А'),
}


@blueprint.route('/load', methods=[Method.GET])
def load():
    recreate_schema()

    # Города
    vladivostok = city_service.create('Владивосток')

    # Координаты
    for fixture in [*road_fixtures.values(), *place_fixtures.values()]:
        fixture.coordinate = coordinate_service.create(vladivostok, fixture.longitude, fixture.latitude)

    # Дороги
    for i, road_fixture in road_fixtures.items():
        for neighbour in road_fixture.neighbours:
            road_service.create(road_fixture.coordinate, road_fixtures[neighbour].coordinate)
            road_fixtures[neighbour].neighbours.remove(i)

    # Места
    for place_fixture in place_fixtures.values():
        place_service.create(place_fixture.coordinate, place_fixture.name, place_fixture.address)

    return 'Loaded!'
