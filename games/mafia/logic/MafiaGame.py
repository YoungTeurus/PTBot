import random
from typing import Optional

from chat.ChatMessage import ChatMessage
from games.mafia.logic.MafiaAction import SendWhisperMessage, WaitBeforeNextAction, SendGlobalMessage, MafiaAction, \
    StartNewNight, StartNewDay, NoStateMutationMafiaAction, LockingMafiaAction, WaitForAnswerFromMany, ANSWERS_DICT, \
    CheckIfGameEnded, KillPlayer
from games.mafia.logic.MafiaPlayer import MafiaPlayer
from games.mafia.logic.MafiaPlayerDistribution import PLAYABLE_CONFIGURATIONS
from games.mafia.logic.MafiaProperties import DAY_TALKING_DURATION_SECS, FIRST_NIGHT_MAFIA_TALKING_DURATION_SECS, \
    DAY_JUDGMENT_VOTE_DURATION_SECS, DAY_JUDGMENT_GUILTY_ANSWER_DURATION_SECS, \
    DAY_JUDGMENT_GUILTY_KILL_VOTE_DURATION_SECS
from games.mafia.logic.MafiaRoleActions import MafiaRoleActions
from games.mafia.logic.MafiaRolesDefinitions import MAFIA, NIGHT_ROLES_TURN_ORDER
from games.mafia.logic.MafiaState import MafiaState
from games.mafia.logic.NewMafiaAction import NewMafiaAction
from games.mafia.logic.Utils import VOTED_COUNT_DICT, countOnlyNotNoneAnswers, extractFirstArg
from properties import COMMAND_PREFIX
from utils.ArgsDevider import splitArgs
from utils.ConsoleProvider import CONSOLE
from utils.RandUtils import randPopFromArr
from utils.Utils import dictMostCommon


class MafiaGame:
    state: MafiaState

    # Текущее длительное действие, завершения которого необходимо дождаться перед выполнением следующего действия из actionQueue
    currentLockingAction: Optional[LockingMafiaAction]

    currentAction: Optional[NewMafiaAction]
    actions: list[NewMafiaAction]
    # Действия, выполняемые по мере поступления и завершения предыдущего действия:
    actionQueue: list[MafiaAction]
    # Дейсвтия, выполянемые сразу же:
    immediateActionQueue: list[NoStateMutationMafiaAction]

    def __init__(self, playersNames: list[str]):
        players = self.__makePlayers(playersNames)
        self.state = MafiaState(players)
        CONSOLE.print("Game is ready, players = '{}'".format(self.state.players))

        self.currentLockingAction = None
        self.actionQueue = []
        self.immediateActionQueue = []

        self.currentAction = None
        self.actions = []

    @staticmethod
    def __makePlayers(playersNames: list[str]) -> list[MafiaPlayer]:
        rolesToDistribute = PLAYABLE_CONFIGURATIONS[len(playersNames)]()

        players = []
        for name in playersNames:
            chosenRole = randPopFromArr(rolesToDistribute)
            players.append(MafiaPlayer(name, chosenRole))

        return players

    def start(self) -> None:
        self.__sendRolesToPlayers()
        self.__nightZeroMafiaMeeting()
        self.__nextDay()

    def __sendRolesToPlayers(self):
        actions: list[MafiaAction] = []

        for player in self.state.players:
            actions.append(
                SendWhisperMessage("{}, ваша роль - {}".format(player.nick, player.role.name), player.nick))

        self.actionQueue.extend(actions)

    def __nightZeroMafiaMeeting(self):
        actions: list[MafiaAction] = []

        mafiaNicknames: list[str] = []
        for player in self.state.players:
            if player.role == MAFIA:
                mafiaNicknames.append(player.nick)

        for mafia in mafiaNicknames:
            actions.append(SendWhisperMessage("Члены мафии: {}".format(", ".join(mafiaNicknames)), mafia))

        actions.append(SendGlobalMessage(
            "Город спит. Члены мафии в течении {} секунд знакомятся.".format(FIRST_NIGHT_MAFIA_TALKING_DURATION_SECS)))
        actions.append(WaitBeforeNextAction(FIRST_NIGHT_MAFIA_TALKING_DURATION_SECS))

        self.actionQueue.extend(actions)

    def __nextDay(self):
        self.state.nextDay()

        actions: list[MafiaAction] = []

        actions.append(SendGlobalMessage(
            "Город просыпается, у горожан есть {} секунд на знакомство.".format(DAY_TALKING_DURATION_SECS)))
        actions.append(WaitBeforeNextAction(DAY_TALKING_DURATION_SECS))
        actions.append(StartNewNight())

        self.actionQueue.extend(actions)

    def nextNight(self):
        self.state.nextNight()

        actions: list[MafiaAction] = []

        actions.append(SendGlobalMessage("Город засыпает."))

        # TODO: Для всех ночных ролей выполнить их onNightStart действие:
        # В порядке действия ночных ролей выполнить их onNightTurn действие:
        for role in NIGHT_ROLES_TURN_ORDER:
            actions.extend(MafiaRoleActions.onNightTurn(role, self))
        # TODO: Для всех ночных ролей выполнить их onNightEnd действие:

        # После выполнения всех действий - начать новый день
        actions.append(StartNewDay())

        self.actionQueue.extend(actions)

    def nextDay(self):
        def validateVote(msg: ChatMessage) -> bool:
            bodyWithoutPrefix = msg.body[len(COMMAND_PREFIX):]
            args = splitArgs(bodyWithoutPrefix)
            if len(args) == 0:
                self.immediateActionQueue.append(SendWhisperMessage("В сообщении не найдено имя выставляемого!", msg.sender))
                return False
            name = args[0]
            if name not in self.state.getAllAliveNicknames():
                self.immediateActionQueue.append(
                    SendWhisperMessage("Имя '{}' не найдено среди имён живых игроков".format(name), msg.sender))
                return False
            return True

        def countVotes(votes: ANSWERS_DICT) -> None:
            self.immediateActionQueue.append(SendGlobalMessage("Сбор кандидатур для суда завершён..."))

            # player_nick => number_of_votes
            targetsToVoteKill: VOTED_COUNT_DICT = countOnlyNotNoneAnswers(votes, extractFirstArg)

            CONSOLE.print("Голоса на суде: {}".format(targetsToVoteKill))

            if len(targetsToVoteKill) == 0:
                CONSOLE.print("Цель для суда не была выбрана")
                self.immediateActionQueue.append(
                    SendGlobalMessage("Ни одна кандидатура не выбрана"))
                return
            mostCommonNames: list[str] = dictMostCommon(targetsToVoteKill)
            realVoteKill: str = random.choice(mostCommonNames)
            CONSOLE.print("Цель суда - {}".format(realVoteKill))
            startJudgement(realVoteKill)

        possibleAnswers = ["да", "нет"]
        def validateJudgementVote(msg: ChatMessage) -> bool:
            bodyWithoutPrefix = msg.body[len(COMMAND_PREFIX):]
            args = splitArgs(bodyWithoutPrefix)
            if len(args) == 0:
                self.immediateActionQueue.append(
                    SendWhisperMessage("В сообщении не найдено ответа на голосование!", msg.sender))
                return False
            voteAnswer = args[0]
            if voteAnswer not in possibleAnswers:
                self.immediateActionQueue.append(
                    SendWhisperMessage("Возможные ответы: {}".format(possibleAnswers), msg.sender))
                return False
            self.immediateActionQueue.append(
                SendWhisperMessage("Принят ответ '{}'".format(voteAnswer), msg.sender))
            return True

        def startJudgement(voteKillName: str) -> None:
            def countJudgementVotes(votes: ANSWERS_DICT) -> None:
                self.immediateActionQueue.append(SendGlobalMessage("Сбор голосов для суда завершён..."))

                # "да"/"нет" => number_of_votes
                choises: VOTED_COUNT_DICT = countOnlyNotNoneAnswers(votes, extractFirstArg)

                yes: int = choises["да"] if "да" in choises else 0
                no: int = choises["нет"] if "нет" in choises else 0
                no += len([None for vote in votes if vote is None])  # Неответившие считаются за "нет"

                if yes > no:
                    self.immediateActionQueue.append(SendGlobalMessage("Суд проголосовал ЗА казнь {}...".format(voteKillName)))
                    self.actionQueue.append(KillPlayer(voteKillName, "Городской суд"))
                else:
                    self.immediateActionQueue.append(SendGlobalMessage("Суд проголосовал ПРОТИВ казни {}...".format(voteKillName)))

            self.actionQueue.append(SendGlobalMessage("Проводится суд над {}. У вас есть {} секунд, чтобы оправдаться".format(voteKillName, DAY_JUDGMENT_GUILTY_ANSWER_DURATION_SECS)))
            self.actionQueue.append(WaitBeforeNextAction(DAY_JUDGMENT_GUILTY_ANSWER_DURATION_SECS))
            self.actionQueue.append(SendGlobalMessage("Горожане, виновен ли {}? Ответьте с помощью '!да' или '!нет'".format(voteKillName)))

            voters = self.state.getAllAliveNicknames()
            voters.remove(voteKillName)
            self.actionQueue.append(WaitForAnswerFromMany(voters, DAY_JUDGMENT_GUILTY_KILL_VOTE_DURATION_SECS, countJudgementVotes, validateJudgementVote))


        self.state.nextDay()

        self.immediateActionQueue.append(
            SendGlobalMessage("Город просыпается. Наступил день номер {}.".format(self.state.dayNumber)))

        # TODO: Выполнить onDayStart действия ролей
        # Выполнить текущие actions, накопившиеся за ночь.
        # Проверить, выиграла ли какая-либо из команд
        self.actionQueue.append(CheckIfGameEnded())
        # Дать время на общение
        self.actionQueue.append(SendGlobalMessage(
            "Жители города могут обсудить произошедшее за ночь в течении {} секунд".format(DAY_TALKING_DURATION_SECS)))
        self.actionQueue.append(WaitBeforeNextAction(DAY_TALKING_DURATION_SECS))
        # Суд
        self.actionQueue.append(SendGlobalMessage(
            "Начинается суд. Любой житель в течении {} секунд может отправить сообщение по типу '{}имя_игрока', чтобы выставить его кандидатуру".format(
                DAY_JUDGMENT_VOTE_DURATION_SECS, COMMAND_PREFIX)))
        self.actionQueue.append(WaitForAnswerFromMany(self.state.getAllAliveNicknames(), DAY_JUDGMENT_VOTE_DURATION_SECS, countVotes, validateVote))

        # Начать новую ночь
