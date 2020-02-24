from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
Base=declarative_base()
class Account(Base):
    __table__='account'
    id=Column(Integer, primary_key=True)
    user_name=Column(String(50), nullable=False)
    def is_active(self):
        return True
    def get_id(self):
        return self.id
    def is_authenticated(self):
        return True
    def is_anonymous(self):
        return False


