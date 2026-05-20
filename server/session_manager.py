import os

import flask, scrypt

from database import Database

class SessionManager:

    def __init__(self, db: Database):
        self.db = db

    def _hash(self, password: str, datalength: int = 64) -> bytes:
        return scrypt.encrypt(
            os.urandom(datalength),
            password.encode('utf-8')
        )
    
    def _check_hash(self, hashed_password: bytes, guess: str) -> bool:
        try:
            scrypt.decrypt(hashed_password, guess, encoding = None) # type: ignore
            return True
        except scrypt.error:
            return False
        
    def user(self) -> str:
        if not self.is_logged_in():
            raise ValueError("No user is currently logged in")
        return flask.session['user']
        
    def is_logged_in(self) -> bool:
        return 'user' in flask.session

    def login(self, username: str, password: str) -> None:
        try:
            _, stored_hash = self.db.select('select_player', {'player_name': username})[0]
        except IndexError:
            raise ValueError("Invalid username or password")
        if not self._check_hash(stored_hash, password):
            raise ValueError("Invalid username or password")
        flask.session['user'] = username

    def logout(self) -> None:
        if 'user' in flask.session:
            flask.session.pop('user')

    def register(self, username: str, password: str) -> None:
        hashed = self._hash(password)
        try:
            self.db.exec('insert_player', [{'player_name': username, 'password': hashed}])
        except Exception as e:
            raise ValueError("Username already exists") from e
    