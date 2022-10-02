from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from games.mafia.MafiaWorker import MafiaWorker

# MAFIA_WORKER_CALLBACK = Callable[['MafiaWorker'], None]


class NewMafiaAction:
    worker: 'MafiaWorker'

    started: bool

    def __init__(self) -> None:
        self.started = False

    def act(self, worker: MafiaWorker) -> None:
        self.worker = worker
        if not self.started:
            self.started = True
            self._setup()
        else:
            self._update()

    def _setup(self) -> None:
        raise NotImplementedError

    def _update(self) -> None:
        raise NotImplementedError

    def finished(self) -> bool:
        return self.started and self._actualFinished()

    def _actualFinished(self) -> bool:
        raise NotImplementedError


class CompletableMafiaAction(NewMafiaAction, ABC):
    __completed: bool

    def __init__(self) -> None:
        super().__init__()
        self.__completed = False

    def complete(self) -> None:
        self.__completed = True

    def _actualFinished(self) -> bool:
        return self.__completed


class OneTimeAction(NewMafiaAction, ABC):
    def _update(self) -> None:
        pass

    def _actualFinished(self) -> bool:
        return True


# class NewMafiaParameterAction(NewMafiaAction):
#     __setupClbk: Optional[MAFIA_WORKER_CALLBACK]
#     __updateCbck: Optional[MAFIA_WORKER_CALLBACK]
#     __finishedClbk: BOOL_PROVIDER
#
#     def __init__(self,
#                  finished: Callable[[], bool],
#                  setup: Optional[CALLBACK_FUNCTION] = None,
#                  update: Optional[CALLBACK_FUNCTION] = None
#                  ) -> None:
#         super().__init__()
#         self.__finishedClbk = finished
#         self.__setupClbk = setup
#         self.__updateCbck = update
#
#     def _setup(self) -> None:
#         if self.__setupClbk is not None:
#             self.__setupClbk(self.worker)
#
#     def _update(self) -> None:
#         if self.__updateCbck is not None:
#             self.__updateCbck(self.worker)
#
#     def _actualFinished(self) -> bool:
#         return self.__finishedClbk()


class NewMafiaActionSequence(NewMafiaAction):
    actions: list[NewMafiaAction]
    currentIndex: int

    def __init__(self, start: NewMafiaAction) -> None:
        super().__init__()
        self.actions = [start]
        self.currentIndex = 0

    def then(self, action: NewMafiaAction) -> NewMafiaActionSequence:
        self.actions.append(action)
        return self

    def _setup(self) -> None:
        if not self._actualFinished():
            self.__actCurrent()

    def _update(self) -> None:
        if not self._actualFinished():
            self.__actCurrent()

    def __actCurrent(self) -> None:
        if not (action := self.actions[self.currentIndex]).finished():
            action.act(self.worker)
        else:
            self.currentIndex += 1

    def _actualFinished(self) -> bool:
        return self.currentIndex >= len(self.actions)
