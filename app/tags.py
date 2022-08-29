from enum import Enum


class Tags(str, Enum):
    categories = 'categories'
    offers = 'offers'
    products = 'products'
    pharmacies = 'pharmacies'
    users = 'users'
    favorites = 'favorites'
    profile = 'profile'
