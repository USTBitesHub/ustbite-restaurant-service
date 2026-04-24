from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.models import Restaurant, MenuCategory, MenuItem
from app.schemas import RestaurantCreate, RestaurantUpdate, AvailabilityUpdate

async def get_restaurants(db: AsyncSession, skip: int = 0, limit: int = 20):
    result = await db.execute(select(Restaurant).offset(skip).limit(limit))
    return result.scalars().all()

async def get_restaurant(db: AsyncSession, restaurant_id: str):
    result = await db.execute(select(Restaurant).filter(Restaurant.id == restaurant_id))
    return result.scalars().first()

async def create_restaurant(db: AsyncSession, payload: RestaurantCreate):
    db_obj = Restaurant(**payload.model_dump())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def update_restaurant(db: AsyncSession, restaurant_id: str, payload: RestaurantUpdate):
    db_obj = await get_restaurant(db, restaurant_id)
    if not db_obj:
        return None
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(db_obj, key, value)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def get_menu(db: AsyncSession, restaurant_id: str, skip: int = 0, limit: int = 100):
    result = await db.execute(select(MenuItem).filter(MenuItem.restaurant_id == restaurant_id).offset(skip).limit(limit))
    return result.scalars().all()

async def get_menu_categories(db: AsyncSession, restaurant_id: str):
    result = await db.execute(select(MenuCategory).filter(MenuCategory.restaurant_id == restaurant_id))
    return result.scalars().all()

async def update_item_availability(db: AsyncSession, restaurant_id: str, item_id: str, payload: AvailabilityUpdate):
    result = await db.execute(select(MenuItem).filter(MenuItem.id == item_id, MenuItem.restaurant_id == restaurant_id))
    db_obj = result.scalars().first()
    if not db_obj:
        return None
    db_obj.is_available = payload.is_available
    await db.commit()
    await db.refresh(db_obj)
    return db_obj
