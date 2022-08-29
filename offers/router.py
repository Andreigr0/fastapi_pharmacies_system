from fastapi import APIRouter

from offers.schemas import Offer, OfferDetails

offers_router = APIRouter(
    prefix='/offers',
    tags=['offers'],
)


@offers_router.get('', response_model=list[Offer])
def get_offers():
    return []


@offers_router.get('/{id}', response_model=OfferDetails)
def get_offer(id: int):
    return None
