import enum, json, os, sqlite3, typing

import dotenv

env = dotenv.dotenv_values('.env')
keys = [
    'KDH_DATABASE'
]
for k in keys:
    assert env[k], f'{k} must be set in .env file'

class Database:
    class Tables(enum.Enum):
        PLAYERS = 'players'
        ROUNDS = 'rounds'
        ROOMS = 'rooms'
        ROOM_ROUNDS = 'room_rounds'
        ROUND_RESULTS = 'round_results'

    def __init__(self):
        self.path: str = env['KDH_DATABASE'] # type: ignore

    def select(self, query: str, params: typing.Optional[list[tuple]]) -> list[tuple]:
        return self._exec('execute', query, params)
    
    def insert(self, query: str, params: typing.Optional[list[tuple]]) -> list[tuple]:
        return self._exec('executemany', query, params)
    
    def update(self, query: str, params: typing.Optional[list[tuple]]) -> list[tuple]:
        return self._exec('executemany', query, params)
    
    def delete(self, query: str, params: typing.Optional[list[tuple]]) -> list[tuple]:
        return self._exec('executemany', query, params)

    def _exec(self,
        executor: str,
        query: str,
        params: typing.Optional[list[tuple]]
    ) -> list[tuple]:
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            if params is None:
                getattr(cursor, executor)(query)
            else:
                getattr(cursor, executor)(query, params)
            conn.commit()
            return cursor.fetchall()

class RoomManager:
    class RoomState(enum.Enum):
        WAITING = 'waiting'
        ONGOING = 'ongoing'
        FINISHED = 'finished'

    def __init__(self):
        self.db = Database()
        self.ongoing_rooms = {}
        self.next_room_id = 1

    def create_room(self) -> int:
        room_id = self.next_room_id
        self.next_room_id += 1
        self.ongoing_rooms[room_id] = {
            "players": [],
            "rounds": [],
            "game_state": self.RoomState.WAITING
        }
        return room_id

    def get_room(self, room_id) -> dict:
        try:
            return self.ongoing_rooms[room_id]
        except KeyError:
            raise ValueError(f'Room with id {room_id} does not exist')

    def delete_room(self, room_id: int) -> None:
        try:
            del self.ongoing_rooms[room_id]
        except KeyError:
            raise ValueError(f'Room with id {room_id} does not exist')