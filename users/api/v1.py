from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
from sqlalchemy.orm import Session

from app.database import get_db
from items.schemas import Item
from users import crud
from users.models import UserModel
from users.schemas import User, Token, UserCreate, TokenData
from users.auth_utils import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, decode_token, verify_password

router = APIRouter(
    prefix='/users',
    tags=['users'],
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users")


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UserModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode_token(token)
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = crud.get_user_by_email(db, token_data.username)
    if not user:
        raise credentials_exception

    return user


def authenticate_user(username: str, password: str, db: Session = Depends(get_db)) -> bool | UserModel:
    user: UserModel = db.query(UserModel).filter(UserModel.email == username).first()
    if not user:
        # todo: add login
        user = crud.create_user(db, UserCreate(email=username, login=username, password=password))
        return user
    if not verify_password(password, user.hashed_password):
        return False
    return user


@router.post('', response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(username=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={'sub': user.email}, expires_delta=access_token_expires)
    return {'access_token': access_token, 'token_type': 'bearer'}


# TODO: вернуть создание пользователя
# @router.post('', response_model=User, status_code=status.HTTP_201_CREATED)
# def create_user(user: UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail='Email already registered')
#     return crud.create_user(db=db, user=user)


@router.get('', response_model=list[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip, limit)


@router.get('/me', response_model=User)
def read_current_user(user: User = Depends(get_current_user)):
    return user


@router.get('/{user_id}', response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)

    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')

    return db_user


@router.get('/{user_id}/items/{item_id}', response_model=Item)
def read_user_item(user_id: int, item_id: int, q: str | None = None, short: bool = False):
    item = {'item_id': item_id, 'owner_id': user_id}
    if q:
        item.update({'q': q})
    if not short:
        item.update({'description': 'this is long description'})
    return item
