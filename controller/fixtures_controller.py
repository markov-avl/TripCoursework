from dataclasses import dataclass

from flask import Blueprint, current_app

from controller.method import Method
from database import database
from entity import Coordinate
from service import CityService, RoadService, CoordinateService, PlaceService


@dataclass
class RoadFixture:
    latlon: tuple[float, float]
    neighbours: list[int]
    coordinate: Coordinate = None


@dataclass
class PlaceFixture:
    latlon: tuple[float, float]
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
    0: RoadFixture(latlon=(43.11630, 131.88244), neighbours=[1, 4]),
    1: RoadFixture(latlon=(43.11573, 131.88549), neighbours=[0, 2, 3]),
    2: RoadFixture(latlon=(43.11527, 131.88826), neighbours=[1, 5, 10]),
    3: RoadFixture(latlon=(43.11804, 131.88631), neighbours=[1, 4, 5, 11]),
    4: RoadFixture(latlon=(43.11862, 131.88327), neighbours=[0, 3, 12]),
    5: RoadFixture(latlon=(43.11753, 131.88902), neighbours=[2, 3, 6]),
    6: RoadFixture(latlon=(43.11791, 131.89086), neighbours=[5, 7, 8]),
    7: RoadFixture(latlon=(43.11902, 131.89108), neighbours=[6, 11, 15]),
    8: RoadFixture(latlon=(43.11732, 131.89367), neighbours=[6, 9, 32]),
    9: RoadFixture(latlon=(43.11579, 131.89501), neighbours=[8, 10]),
    10: RoadFixture(latlon=(43.11409, 131.89457), neighbours=[2, 9, 54]),
    11: RoadFixture(latlon=(43.11980, 131.88694), neighbours=[3, 7, 12, 14]),
    12: RoadFixture(latlon=(43.12038, 131.88391), neighbours=[4, 11, 13]),
    13: RoadFixture(latlon=(43.12152, 131.88428), neighbours=[12, 14, 18]),
    14: RoadFixture(latlon=(43.12092, 131.88729), neighbours=[11, 13, 15, 17]),
    15: RoadFixture(latlon=(43.12013, 131.89147), neighbours=[7, 14, 16]),
    16: RoadFixture(latlon=(43.12119, 131.89186), neighbours=[15, 17, 22]),
    17: RoadFixture(latlon=(43.12207, 131.88771), neighbours=[14, 16, 18, 20]),
    18: RoadFixture(latlon=(43.12269, 131.88467), neighbours=[13, 17, 19]),
    19: RoadFixture(latlon=(43.12377, 131.88514), neighbours=[18, 20, 21]),
    20: RoadFixture(latlon=(43.12316, 131.88817), neighbours=[17, 19, 21]),
    21: RoadFixture(latlon=(43.12432, 131.88855), neighbours=[19, 20, 23, 24]),
    22: RoadFixture(latlon=(43.12241, 131.89201), neighbours=[16, 23]),
    23: RoadFixture(latlon=(43.12428, 131.89233), neighbours=[21, 22, 25]),
    24: RoadFixture(latlon=(43.12811, 131.89233), neighbours=[21, 26]),
    25: RoadFixture(latlon=(43.12819, 131.90222), neighbours=[23, 26, 27, 40]),
    26: RoadFixture(latlon=(43.12902, 131.89246), neighbours=[24, 25, 39]),
    27: RoadFixture(latlon=(43.12670, 131.90696), neighbours=[25, 28, 37, 38]),
    28: RoadFixture(latlon=(43.12125, 131.90359), neighbours=[27, 29, 34, 35]),
    29: RoadFixture(latlon=(43.11920, 131.90179), neighbours=[28, 30, 35]),
    30: RoadFixture(latlon=(43.11527, 131.89651), neighbours=[29, 31, 32, 55]),
    31: RoadFixture(latlon=(43.11184, 131.89636), neighbours=[30]),
    32: RoadFixture(latlon=(43.11674, 131.89662), neighbours=[8, 30, 33]),
    33: RoadFixture(latlon=(43.11814, 131.89995), neighbours=[32, 34, 47]),
    34: RoadFixture(latlon=(43.11961, 131.89928), neighbours=[28, 33]),
    35: RoadFixture(latlon=(43.12030, 131.90477), neighbours=[28, 29, 36]),
    36: RoadFixture(latlon=(43.12495, 131.90898), neighbours=[35, 37, 38]),
    37: RoadFixture(latlon=(43.12677, 131.91220), neighbours=[27, 36, 44, 38]),
    38: RoadFixture(latlon=(43.12745, 131.91031), neighbours=[27, 36, 37, 41]),
    39: RoadFixture(latlon=(43.13018, 131.89276), neighbours=[26, 40]),
    40: RoadFixture(latlon=(43.13297, 131.89984), neighbours=[25, 39, 41]),
    41: RoadFixture(latlon=(43.13312, 131.91147), neighbours=[38, 40, 42, 43]),
    42: RoadFixture(latlon=(43.14408, 131.90701), neighbours=[41, 82, 124, 125, 170]),
    43: RoadFixture(latlon=(43.13215, 131.91520), neighbours=[41, 44, 179]),
    44: RoadFixture(latlon=(43.12266, 131.92546), neighbours=[37, 43, 45, 46, 63]),
    45: RoadFixture(latlon=(43.11959, 131.93220), neighbours=[44, 46]),
    46: RoadFixture(latlon=(43.11897, 131.92181), neighbours=[44, 45, 47]),
    47: RoadFixture(latlon=(43.11806, 131.91842), neighbours=[33, 46, 48]),
    48: RoadFixture(latlon=(43.11377, 131.91756), neighbours=[47, 49, 51]),
    49: RoadFixture(latlon=(43.11245, 131.91722), neighbours=[48, 50, 57]),
    50: RoadFixture(latlon=(43.11511, 131.90782), neighbours=[49, 51, 52]),
    51: RoadFixture(latlon=(43.11587, 131.90821), neighbours=[48, 50, 56]),
    52: RoadFixture(latlon=(43.11574, 131.90490), neighbours=[50, 53]),
    53: RoadFixture(latlon=(43.11477, 131.90130), neighbours=[52, 54, 55]),
    54: RoadFixture(latlon=(43.11377, 131.89688), neighbours=[10, 53]),
    55: RoadFixture(latlon=(43.11608, 131.90259), neighbours=[30, 53, 56]),
    56: RoadFixture(latlon=(43.11702, 131.90610), neighbours=[51, 55]),
    57: RoadFixture(latlon=(43.11217, 131.92473), neighbours=[49, 58, 59]),
    58: RoadFixture(latlon=(43.11279, 131.93413), neighbours=[57, 59, 61]),
    59: RoadFixture(latlon=(43.11132, 131.93408), neighbours=[57, 58, 60]),
    60: RoadFixture(latlon=(43.10960, 131.93795), neighbours=[59, 61]),
    61: RoadFixture(latlon=(43.11314, 131.93610), neighbours=[58, 60, 62]),
    62: RoadFixture(latlon=(43.12808, 131.94018), neighbours=[61, 63, 64, 185]),
    63: RoadFixture(latlon=(43.12980, 131.92911), neighbours=[44, 62]),
    64: RoadFixture(latlon=(43.13428, 131.94773), neighbours=[62, 65]),
    65: RoadFixture(latlon=(43.13936, 131.94850), neighbours=[64, 66, 188]),
    66: RoadFixture(latlon=(43.14581, 131.95310), neighbours=[65, 67]),
    67: RoadFixture(latlon=(43.14985, 131.95292), neighbours=[66, 68]),
    68: RoadFixture(latlon=(43.15088, 131.95447), neighbours=[67, 69]),
    69: RoadFixture(latlon=(43.15363, 131.95314), neighbours=[68, 70]),
    70: RoadFixture(latlon=(43.15968, 131.94516), neighbours=[69, 71, 113]),
    71: RoadFixture(latlon=(43.16365, 131.94074), neighbours=[70, 72, 87]),
    72: RoadFixture(latlon=(43.16562, 131.94215), neighbours=[71, 73]),
    73: RoadFixture(latlon=(43.16897, 131.93305), neighbours=[72, 74, 85, 87]),
    74: RoadFixture(latlon=(43.16910, 131.92748), neighbours=[73, 75]),
    75: RoadFixture(latlon=(43.16916, 131.92220), neighbours=[74, 76, 83]),
    76: RoadFixture(latlon=(43.16766, 131.91482), neighbours=[75, 77, 168]),
    77: RoadFixture(latlon=(43.16450, 131.91383), neighbours=[76, 78, 83]),
    78: RoadFixture(latlon=(43.16356, 131.91331), neighbours=[77, 79, 86, 169]),
    79: RoadFixture(latlon=(43.15542, 131.91108), neighbours=[78, 80, 100]),
    80: RoadFixture(latlon=(43.15154, 131.90786), neighbours=[79, 81, 131]),
    81: RoadFixture(latlon=(43.14928, 131.90632), neighbours=[80, 82, 130]),
    82: RoadFixture(latlon=(43.14737, 131.90598), neighbours=[42, 81, 125]),
    83: RoadFixture(latlon=(43.16542, 131.92215), neighbours=[75, 77, 84]),
    84: RoadFixture(latlon=(43.16683, 131.92728), neighbours=[83, 85]),
    85: RoadFixture(latlon=(43.16688, 131.93239), neighbours=[73, 84]),
    86: RoadFixture(latlon=(43.16331, 131.91520), neighbours=[78, 87, 88]),
    87: RoadFixture(latlon=(43.16628, 131.93280), neighbours=[71, 73, 86]),
    88: RoadFixture(latlon=(43.16033, 131.91696), neighbours=[86, 89]),
    89: RoadFixture(latlon=(43.16168, 131.92198), neighbours=[88, 90, 96]),
    90: RoadFixture(latlon=(43.16365, 131.92962), neighbours=[89, 91]),
    91: RoadFixture(latlon=(43.16354, 131.93035), neighbours=[90, 92]),
    92: RoadFixture(latlon=(43.16026, 131.92926), neighbours=[91, 93]),
    93: RoadFixture(latlon=(43.15996, 131.92814), neighbours=[92, 94, 102]),
    94: RoadFixture(latlon=(43.15958, 131.92664), neighbours=[93, 95, 101]),
    95: RoadFixture(latlon=(43.16038, 131.92404), neighbours=[94, 96]),
    96: RoadFixture(latlon=(43.15988, 131.92321), neighbours=[89, 95, 97]),
    97: RoadFixture(latlon=(43.15889, 131.92346), neighbours=[96, 98, 101]),
    98: RoadFixture(latlon=(43.15708, 131.92353), neighbours=[97, 99, 101, 148]),
    99: RoadFixture(latlon=(43.15576, 131.91364), neighbours=[98, 100]),
    100: RoadFixture(latlon=(43.15528, 131.91297), neighbours=[79, 99, 133, 147]),
    101: RoadFixture(latlon=(43.15736, 131.92664), neighbours=[94, 97, 98, 102]),
    102: RoadFixture(latlon=(43.15719, 131.92715), neighbours=[93, 101, 103, 152]),
    103: RoadFixture(latlon=(43.15683, 131.92833), neighbours=[102, 104, 108]),
    104: RoadFixture(latlon=(43.15924, 131.92825), neighbours=[103, 105]),
    105: RoadFixture(latlon=(43.16054, 131.93166), neighbours=[104, 106]),
    106: RoadFixture(latlon=(43.15903, 131.93460), neighbours=[105, 107]),
    107: RoadFixture(latlon=(43.15640, 131.93464), neighbours=[106, 108, 109]),
    108: RoadFixture(latlon=(43.15615, 131.93084), neighbours=[103, 107]),
    109: RoadFixture(latlon=(43.15520, 131.93670), neighbours=[107, 110]),
    110: RoadFixture(latlon=(43.15413, 131.94099), neighbours=[109, 111, 114]),
    111: RoadFixture(latlon=(43.16102, 131.94005), neighbours=[110, 112]),
    112: RoadFixture(latlon=(43.16168, 131.94250), neighbours=[111, 113]),
    113: RoadFixture(latlon=(43.15990, 131.94387), neighbours=[70, 112]),
    114: RoadFixture(latlon=(43.15307, 131.93563), neighbours=[110, 115]),
    115: RoadFixture(latlon=(43.15088, 131.93602), neighbours=[114, 116]),
    116: RoadFixture(latlon=(43.14690, 131.93057), neighbours=[115, 117]),
    117: RoadFixture(latlon=(43.14380, 131.92769), neighbours=[116, 118]),
    118: RoadFixture(latlon=(43.14221, 131.92705), neighbours=[117, 119]),
    119: RoadFixture(latlon=(43.14136, 131.92597), neighbours=[118, 120, 129]),
    120: RoadFixture(latlon=(43.14083, 131.92430), neighbours=[119, 121]),
    121: RoadFixture(latlon=(43.14167, 131.92185), neighbours=[120, 122]),
    122: RoadFixture(latlon=(43.14086, 131.91555), neighbours=[121, 123]),
    123: RoadFixture(latlon=(43.14462, 131.91379), neighbours=[122, 124]),
    124: RoadFixture(latlon=(43.14365, 131.91057), neighbours=[42, 123]),
    125: RoadFixture(latlon=(43.14834, 131.91031), neighbours=[42, 82, 126]),
    126: RoadFixture(latlon=(43.14900, 131.91207), neighbours=[125, 127, 130, 136]),
    127: RoadFixture(latlon=(43.14756, 131.91761), neighbours=[126, 128, 145]),
    128: RoadFixture(latlon=(43.14693, 131.91958), neighbours=[127, 129]),
    129: RoadFixture(latlon=(43.14352, 131.92147), neighbours=[119, 128]),
    130: RoadFixture(latlon=(43.15022, 131.91065), neighbours=[81, 126, 131, 137]),
    131: RoadFixture(latlon=(43.15078, 131.90979), neighbours=[80, 130, 132]),
    132: RoadFixture(latlon=(43.15420, 131.91147), neighbours=[131, 133]),
    133: RoadFixture(latlon=(43.15407, 131.91306), neighbours=[100, 132, 134]),
    134: RoadFixture(latlon=(43.15376, 131.91503), neighbours=[133, 135, 147]),
    135: RoadFixture(latlon=(43.15150, 131.91422), neighbours=[134, 136, 138]),
    136: RoadFixture(latlon=(43.15006, 131.91344), neighbours=[126, 135, 137, 145]),
    137: RoadFixture(latlon=(43.15066, 131.91160), neighbours=[130, 136]),
    138: RoadFixture(latlon=(43.15074, 131.91712), neighbours=[135, 139, 140, 145]),
    139: RoadFixture(latlon=(43.15144, 131.91742), neighbours=[138]),
    140: RoadFixture(latlon=(43.15057, 131.91776), neighbours=[138, 141, 143]),
    141: RoadFixture(latlon=(43.15071, 131.91946), neighbours=[140, 142]),
    142: RoadFixture(latlon=(43.14920, 131.91984), neighbours=[141]),
    143: RoadFixture(latlon=(43.15038, 131.91838), neighbours=[140, 144]),
    144: RoadFixture(latlon=(43.14905, 131.91908), neighbours=[143]),
    145: RoadFixture(latlon=(43.14877, 131.91813), neighbours=[127, 136, 138, 146]),
    146: RoadFixture(latlon=(43.14797, 131.92076), neighbours=[145]),
    147: RoadFixture(latlon=(43.15494, 131.91540), neighbours=[100, 134, 148]),
    148: RoadFixture(latlon=(43.15548, 131.92280), neighbours=[98, 147, 149]),
    149: RoadFixture(latlon=(43.15393, 131.92228), neighbours=[148, 150]),
    150: RoadFixture(latlon=(43.15179, 131.92497), neighbours=[149, 151]),
    151: RoadFixture(latlon=(43.15075, 131.93033), neighbours=[150]),
    152: RoadFixture(latlon=(43.15559, 131.92718), neighbours=[102, 153]),
    153: RoadFixture(latlon=(43.15518, 131.93065), neighbours=[152, 154, 156]),
    154: RoadFixture(latlon=(43.15409, 131.92595), neighbours=[153, 155, 166]),
    155: RoadFixture(latlon=(43.15312, 131.92565), neighbours=[154, 167]),
    156: RoadFixture(latlon=(43.15496, 131.93207), neighbours=[153, 157]),
    157: RoadFixture(latlon=(43.15398, 131.93202), neighbours=[156, 158, 161]),
    158: RoadFixture(latlon=(43.15329, 131.93314), neighbours=[157, 159]),
    159: RoadFixture(latlon=(43.15100, 131.93280), neighbours=[158, 160]),
    160: RoadFixture(latlon=(43.15119, 131.93147), neighbours=[159, 161]),
    161: RoadFixture(latlon=(43.15251, 131.93078), neighbours=[157, 160, 162]),
    162: RoadFixture(latlon=(43.15113, 131.93069), neighbours=[161, 163]),
    163: RoadFixture(latlon=(43.15229, 131.92902), neighbours=[162, 164]),
    164: RoadFixture(latlon=(43.15320, 131.92898), neighbours=[163, 165]),
    165: RoadFixture(latlon=(43.15323, 131.92758), neighbours=[164, 166]),
    166: RoadFixture(latlon=(43.15284, 131.92724), neighbours=[154, 165, 167]),
    167: RoadFixture(latlon=(43.15248, 131.92700), neighbours=[155, 166]),
    168: RoadFixture(latlon=(43.16497, 131.90477), neighbours=[76, 169]),
    169: RoadFixture(latlon=(43.16130, 131.90752), neighbours=[78, 168]),
    170: RoadFixture(latlon=(43.14258, 131.91027), neighbours=[42, 171]),
    171: RoadFixture(latlon=(43.14108, 131.90864), neighbours=[170, 172]),
    172: RoadFixture(latlon=(43.14030, 131.90941), neighbours=[171, 173]),
    173: RoadFixture(latlon=(43.13782, 131.91490), neighbours=[172, 174]),
    174: RoadFixture(latlon=(43.13666, 131.92662), neighbours=[173, 175, 180]),
    175: RoadFixture(latlon=(43.13497, 131.92632), neighbours=[174, 176]),
    176: RoadFixture(latlon=(43.13344, 131.92490), neighbours=[175, 177]),
    177: RoadFixture(latlon=(43.13294, 131.92168), neighbours=[176, 178]),
    178: RoadFixture(latlon=(43.13203, 131.91992), neighbours=[177, 179]),
    179: RoadFixture(latlon=(43.13262, 131.91610), neighbours=[43, 178]),
    180: RoadFixture(latlon=(43.13720, 131.93125), neighbours=[174, 181]),
    181: RoadFixture(latlon=(43.13601, 131.93597), neighbours=[180, 182, 186]),
    182: RoadFixture(latlon=(43.13378, 131.93606), neighbours=[181, 183]),
    183: RoadFixture(latlon=(43.13394, 131.93799), neighbours=[182, 184]),
    184: RoadFixture(latlon=(43.13309, 131.93645), neighbours=[183, 185]),
    185: RoadFixture(latlon=(43.12949, 131.94031), neighbours=[62, 184]),
    186: RoadFixture(latlon=(43.13663, 131.94224), neighbours=[181, 187]),
    187: RoadFixture(latlon=(43.13835, 131.94576), neighbours=[186, 188]),
    188: RoadFixture(latlon=(43.13754, 131.95305), neighbours=[65, 187]),
}

place_fixtures = {
    0: PlaceFixture(latlon=(43.11527, 131.88534), name='Площадь Победы', address='Площадь Победы'),
    1: PlaceFixture(latlon=(43.11514, 131.88526), name='Сухой фонтан', address='Площадь Победы'),
    2: PlaceFixture(latlon=(43.11511, 131.88671), name='Стела «Город воинской славы»', address='Ленинский район'),
    3: PlaceFixture(latlon=(43.11458, 131.88714), name='Спасо-Преображенский кафедральный собор',
                    address='Ленинский район'),
    4: PlaceFixture(latlon=(43.11670, 131.87977), name='Версаль', address='Фрунзенский район'),
    5: PlaceFixture(latlon=(43.11392, 131.89243), name='Триумфальная арка', address='Ленинский район'),
    6: PlaceFixture(latlon=(43.11752, 131.89825), name='Вид на залив "Золотой рог"', address='Ленинский район'),
    7: PlaceFixture(latlon=(43.11446, 131.90092), name='Военно-исторический музей Тихоокеанского флота',
                    address='Ленинский район, 66'),
    8: PlaceFixture(latlon=(43.16324, 131.91563), name='Яхонт', address='Первореченский район, 1'),
    9: PlaceFixture(latlon=(43.11636, 131.88217), name='Музей им. Арсеньева', address='Фрунзенский район, 20'),
    10: PlaceFixture(latlon=(43.13407, 131.93725), name='Вираж', address='Первореченский район, 17А с1'),
    11: PlaceFixture(latlon=(43.12578, 131.90454), name='Аванта', address='Ленинский район'),
    12: PlaceFixture(latlon=(43.12514, 131.89490), name='Авизо', address='Ленинский район, 16/18'),
    13: PlaceFixture(latlon=(43.12453, 131.89344), name='Приморская государственная картинная галерея',
                     address='Ленинский район, 12'),
    14: PlaceFixture(latlon=(43.14827, 131.93369), name='Днепровская 90а', address='Первореченский район'),
    15: PlaceFixture(latlon=(43.16263, 131.91081), name='Акфес Сейо', address='Первореченский район, 103'),
    16: PlaceFixture(latlon=(43.11697, 131.88608), name='Скульптура Воспоминание о моряке загранплавания',
                     address='Ленинский район'),
    17: PlaceFixture(latlon=(43.11410, 131.89507), name='Музей Ростелекома', address='Ленинский район'),
    18: PlaceFixture(latlon=(43.11270, 131.89123), name='Морские прогулки на катере', address='Ленинский район'),
    19: PlaceFixture(latlon=(43.12028, 131.88759), name='Сибирское Подворье', address='Ленинский район, 26А'),
    20: PlaceFixture(latlon=(43.11489, 131.91605), name='Mini Hotel Graal', address='Ленинский район, 2'),
    21: PlaceFixture(latlon=(43.11237, 131.91416), name='Самурай', address='Ленинский район'),
    22: PlaceFixture(latlon=(43.11520, 131.91497), name='Busse Mini-hotel', address='Ленинский район, 19'),
    23: PlaceFixture(latlon=(43.12713, 131.90161), name='Астория', address='Ленинский район, 44 к6'),
    24: PlaceFixture(latlon=(43.11806, 131.89931), name='Арка любви', address='Ленинский район'),
    25: PlaceFixture(latlon=(43.11973, 131.88377), name='Изба', address='Фрунзенский район, 3 с1'),
    26: PlaceFixture(latlon=(43.11627, 131.88446), name='Антилопа', address='Фрунзенский район, 23А'),
    27: PlaceFixture(latlon=(43.12895, 131.93333), name='Гранит', address='Ленинский район, 13'),
    28: PlaceFixture(latlon=(43.16798, 131.90313), name='Bay garden', address='Советский район, 23Д к2'),
    29: PlaceFixture(latlon=(43.16547, 131.90500), name='Дружба', address='Советский район, 3'),
    30: PlaceFixture(latlon=(43.11731, 131.88031), name='Филин и Сова', address='Фрунзенский район, 5А'),
    31: PlaceFixture(latlon=(43.11853, 131.89068), name='Гостевой дом Ли', address='Ленинский район, 17'),
    32: PlaceFixture(latlon=(43.11636, 131.91417), name='Вид на город', address='Ленинский район'),
    33: PlaceFixture(latlon=(43.11368, 131.89283), name='Музей города', address='Ленинский район, 6'),
    34: PlaceFixture(latlon=(43.12296, 131.88727), name='Каштан', address='Фрунзенский район, 10А'),
    35: PlaceFixture(latlon=(43.12219, 131.88764), name='Capsule Hotel ALOHA', address='Фрунзенский район, 29'),
    36: PlaceFixture(latlon=(43.11994, 131.89659), name='Статуя Будды', address='Ленинский район'),
    37: PlaceFixture(latlon=(43.11790, 131.90218), name='Смотровая площадка', address='Ленинский район'),
    38: PlaceFixture(latlon=(43.16118, 131.90589), name='Набережная на Второй Речке', address='Советский район'),
    39: PlaceFixture(latlon=(43.11738, 131.88079), name='Галерея Арка', address='Фрунзенский район, 4В'),
    40: PlaceFixture(latlon=(43.16617, 131.90365), name='Томь', address='Советский район, 23А'),
}


@blueprint.route('/load', methods=[Method.GET])
def load():
    recreate_schema()

    # Города
    vladivostok = city_service.create('Владивосток')

    # Координаты
    for fixture in [*road_fixtures.values(), *place_fixtures.values()]:
        fixture.coordinate = coordinate_service.create(*fixture.latlon)

    # Дороги
    for i, road_fixture in road_fixtures.items():
        for neighbour in road_fixture.neighbours:
            road_service.create(vladivostok, road_fixture.coordinate, road_fixtures[neighbour].coordinate)
            road_fixtures[neighbour].neighbours.remove(i)

    # Места
    for place_fixture in place_fixtures.values():
        place_service.create(vladivostok, place_fixture.coordinate, place_fixture.name, place_fixture.address)

    return 'Loaded!'
