from typing import Callable

from games.mafia.logic.MafiaRole import MafiaRole
from games.mafia.logic.MafiaRolesDefinitions import CIVILIAN, COMMISSAR, MAFIA

# Словарь "число игроков" -> "поставщик состава ролей" для такого количества игроков
PLAYABLE_CONFIGURATIONS: dict[int, Callable[[], list[MafiaRole]]] = {
    5: lambda:  [CIVILIAN, CIVILIAN, CIVILIAN, COMMISSAR, MAFIA],
    6: lambda:  [CIVILIAN, CIVILIAN, CIVILIAN, COMMISSAR, MAFIA, MAFIA],
    7: lambda:  [CIVILIAN, CIVILIAN, CIVILIAN, CIVILIAN, COMMISSAR, MAFIA, MAFIA],
    8: lambda:  [CIVILIAN, CIVILIAN, CIVILIAN, CIVILIAN, CIVILIAN, COMMISSAR, MAFIA, MAFIA],
    9: lambda:  [CIVILIAN, CIVILIAN, CIVILIAN, CIVILIAN, CIVILIAN, COMMISSAR, MAFIA, MAFIA, MAFIA],
    10: lambda: [CIVILIAN, CIVILIAN, CIVILIAN, CIVILIAN, CIVILIAN, CIVILIAN, COMMISSAR, MAFIA, MAFIA, MAFIA],
}
