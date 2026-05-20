import enum

from .database import Database

class RoomManager:
    class RoomState(enum.Enum):
        WAITING = 'waiting'
        ONGOING = 'ongoing'
        FINISHED = 'finished'

    def __init__(self, db: Database):
        self.db = db
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

    def get_room(self, room_id: int) -> dict:
        try:
            return self.ongoing_rooms[room_id]
        except KeyError:
            raise ValueError(f'Room with id {room_id} does not exist')

    def delete_room(self, room_id: int) -> None:
        try:
            del self.ongoing_rooms[room_id]
        except KeyError:
            raise ValueError(f'Room with id {room_id} does not exist')