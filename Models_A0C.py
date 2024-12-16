from dataclasses import field, dataclass
from typing import List, Dict, NewType
import threading
from copy import deepcopy

############################
"""Section FUNCTION UTILS"""
############################
def dataFilter(item, filter_mode, user_state) -> bool:
    match filter_mode.condition:
        case filter_mode.NEUTRAL:
            return item
        case filter_mode.POSITIVE:
            return item.filter_value >= user_state.minimum
        case filter_mode.NEGATIVE:
            return item.filter_value < user_state.minimum

###################
"""Section TYPES"""
###################
UserID = NewType('UserID', str)
MessageID = NewType('MessageID', str)

#####################
"""Section MODELS"""
#####################
@dataclass
class FilterMode:
    '''Модель предназначена для управлением состояний фильтра'''
    NEUTRAL: str = 'neutral'
    POSITIVE: str = 'positive'
    NEGATIVE: str = 'negative'
    condition: str = NEUTRAL
    def set_neutral(self):
        self.condition = self.NEUTRAL
    def set_positive(self):
        self.condition = self.POSITIVE
    def set_negative(self):
        self.condition = self.NEGATIVE

@dataclass
class UserState:
    '''Модель предназначения для хранения пользовательских состояний'''
    running: bool = False
    minimum: float = 0.5 #%
    time_delay: int = 30 
    waiting_for_input: bool = False
    user_id_waiting: str = None
    cash: Dict[MessageID, dict] = field(default_factory=dict)
    filter_mode: FilterMode = field(default_factory=FilterMode)
    #running_event: threading.Event = threading.Event()

@dataclass
class TextChunk:
    '''модель предназначена для хранения части сообщения'''
    filter_value: float
    text: str
    
@dataclass
class CashLargeMessage:
    '''модель предназначена для хранения состовных сообщений'''
    messages: List[TextChunk] = field(default_factory=list)
    filter_mode: FilterMode = field(default_factory=FilterMode)
    def __post_init__(self):
        if isinstance(self.filter_mode, FilterMode):
            self.filter_mode = deepcopy(self.filter_mode)
            
    def load_cash(self, user_state) -> str:
        return "".join([str(item.text) for item in self.message if dataFilter(item, self.filter_mode, user_state)])

    
#####################
"""Section STORAGE"""
#####################
user_states: Dict[UserID, UserState] = {}


###############
"""Final MAP"""
###############
"""
user_states: Dict[UserID, UserState]
  └── UserState
        ├── running: bool
        ├── minimum: float
        ├── time_delay: int
        ├── waiting_for_input: bool
        ├── user_id_waiting: str
        ├── filter_mode: FilterMode
        │     ├── NEUTRAL: str
        │     ├── POSITIVE: str
        │     ├── NEGATIVE: str
        │     └── condition: str
        ├── running_event: threading.Event
        └── cash: Dict[MessageID, CashLargeMessage]
              └── CashLargeMessage
                      ├── messages: List[TextChunk]
                      │     ├── TextChunk
                      │     │     ├── filter_value: float
                      │     │     └── text: str
                      └── filter_mode: FilterMode
"""

if __name__ == '__main__':
    #####################
    """Section TESTING"""
    #####################
    from pprint import pprint
    
    user_states: Dict[UserID, UserState] = {}
    userID = UserID('User')
    
    
    def run_test(func):
        def wrapper():
            print(f">>> Running test: {func.__name__}")
            func()
        return wrapper()
     
    @run_test
    def test_UserState():
        '''Тестироварие хранилища UserState'''
        user_states[userID] = UserState()
        assert user_states[userID].running == False
        assert user_states[userID].minimum == 0.5
        assert user_states[userID].time_delay == 30
        assert user_states[userID].waiting_for_input == False
        assert user_states[userID].user_id_waiting is None
        assert user_states[userID].cash == {}
        pprint(user_states)
        userID1 = UserID('User1')
        userID2 = UserID('User2')
        user_states[userID1] = UserState()
        user_states[userID2] = UserState()
        assert user_states[userID1] is not user_states[userID2], 'Были созданы одинаковые классы UserState'
        
    @run_test
    def test_FilterMode():
        '''Тестирование смены режима FilterMode для нескольких пользователей'''
        
        # Создаем двух пользователей
        userID1 = UserID('User1')
        userID2 = UserID('User2')
        
        user_states[userID1] = UserState()
        user_states[userID2] = UserState()
        
        #Обьекты FilterMode не имеют общей ссылки
        assert user_states[userID1].filter_mode is not user_states[userID2].filter_mode, 'Были созданы одинаковые классы FilterMode'
        
        # Устанавливаем режим фильтра
        user_states[userID1].filter_mode.set_positive()
        assert user_states[userID1].filter_mode.condition == user_states[userID1].filter_mode.POSITIVE
        
        user_states[userID2].filter_mode.set_negative()
        assert user_states[userID2].filter_mode.condition == user_states[userID2].filter_mode.NEGATIVE
        
        user_states[userID].filter_mode.set_positive()
        user_states[userID].filter_mode.set_neutral()
        assert user_states[userID].filter_mode.condition == user_states[userID2].filter_mode.NEUTRAL
        
        # Состояния фильтров не совпадают
        assert user_states[userID1].filter_mode.condition != user_states[userID2].filter_mode.condition
        
        # Состояние фильтра для пользователей не изменилось
        assert user_states[userID1].filter_mode.condition == user_states[userID1].filter_mode.POSITIVE
        assert user_states[userID2].filter_mode.condition == user_states[userID2].filter_mode.NEGATIVE
        
        #pprint(user_states)
        
    @run_test
    def test__CashLargeMessage():
        userID1 = UserID('User1')
        user = user_states[userID1]
        
        messages = [
           MessageID('Message1'),
           MessageID('Message2')
        ]
        
        msg1 = user.cash[messages[0]] = CashLargeMessage(filter_mode=user.filter_mode)
        
        # У юзера и кеша одно состояние при инициализации
        assert msg1.filter_mode == user.filter_mode
        
        # У юзера и кеша разные обьекты FilterState
        msg1.filter_mode.set_negative()
        user.filter_mode.set_positive()
        #pprint(msg1)
        #pprint(user)
        assert msg1.filter_mode != user.filter_mode
        
        # У разных сообщений разный FilterState
        msg2 = user.cash[messages[1]] = CashLargeMessage(filter_mode=user.filter_mode)
        assert msg1.filter_mode is not msg2.filter_mode
        
    
    @run_test
    def test_TextChunk():
        userID1 = UserID('User1')
        user = user_states[userID1] 
        chunks = [TextChunk(text = f"Lorem Upsum Dollar {num} [{1/(num+1)}%]\n", filter_value = 1/(num+1)) for num in range(5)]
        
        msg = user.cash[MessageID('Message1')]
        msg.message = chunks
        
        # Тест фильтрации
        print(user.minimum)
        msg.filter_mode.set_neutral()
        print(msg.load_cash(user_states[userID1]))
        assert msg.load_cash(user_states[userID1]) == '\n'.join([
                    "Lorem Upsum Dollar 0 [1.0%]",
                    "Lorem Upsum Dollar 1 [0.5%]",
                    "Lorem Upsum Dollar 2 [0.3333333333333333%]",
                    "Lorem Upsum Dollar 3 [0.25%]",
                    "Lorem Upsum Dollar 4 [0.2%]",
                    ""
                ])
        
        msg.filter_mode.set_negative() 
        print(msg.load_cash(user_states[userID1]))
        assert msg.load_cash(user_states[userID1]) == '\n'.join([
                    "Lorem Upsum Dollar 2 [0.3333333333333333%]",
                    "Lorem Upsum Dollar 3 [0.25%]",
                    "Lorem Upsum Dollar 4 [0.2%]",
                    ""
                ])
        
        msg.filter_mode.set_positive()
        print(msg.load_cash(user_states[userID1]))
        assert msg.load_cash(user_states[userID1]) == '\n'.join([
                    "Lorem Upsum Dollar 0 [1.0%]",
                    "Lorem Upsum Dollar 1 [0.5%]",
                    ""
                ])
        
        
        
        
        
