from games.lobby.Lobby import PlayerLobbySettings
from utils.RandUtils import randFromArr

onGameStart = [
    "Лобби закрывается, Мафия начинается..."
]

onLobbyClose = [
    "Лобби закрывается, город расходится по своим делам..."
]

onTooLittlePeopleToStart = [
    "В лобби слишком мало игроков для начала игры - {} (нужно 5+)"
]

onTooManyPeopleInLobby = [
    "Лобби полно - в Мафию нельзя играть более чем вдесятером"
]

onPlayerJoin = [
    "{}, приветствуем в Мафии!"
]

onPlayerJoinAlreadyIn = [
    "{}, вы уже присоединились к лобби"
]

onPlayerLeave = [
    "{} покидает Мафию"
]

onPlayerLeaveNotPresent = [
    "{}, вы отсутствуете в лобби"
]

MAFIA_LOBBY_SETTINGS: PlayerLobbySettings =\
    PlayerLobbySettings(5, 10,
                        lambda players: randFromArr(onTooLittlePeopleToStart),
                        lambda player, players: randFromArr(onTooManyPeopleInLobby).format(player, players),
                        lambda player, players: randFromArr(onPlayerJoin).format(player, players),
                        lambda player, players: randFromArr(onPlayerJoinAlreadyIn).format(player, players),
                        lambda player, players: randFromArr(onPlayerLeave).format(player, players),
                        lambda player, players: randFromArr(onPlayerLeaveNotPresent).format(player, players)
                        )