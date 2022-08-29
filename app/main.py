import aiofiles
from fastapi import FastAPI, UploadFile
from fastapi.staticfiles import StaticFiles

from app.admin import setup_admin
from app.database import setup_db, setup_engine
from users.api import v1 as users
from categories.api import v1 as categories
from items import router as items
from offers.router import offers_router
from pharmacies.api import v1 as pharmacies
from products.api import v1 as products

app = FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.mount('/files', StaticFiles(directory='files'), name='static')
app.include_router(products.router)
app.include_router(categories.router)
app.include_router(pharmacies.router)
app.include_router(items.router)
app.include_router(users.router)
app.include_router(offers_router)


@app.post('/files/upload')
async def create_file(file: UploadFile):
    path = f'files/{file.filename}'
    async with aiofiles.open(path, 'wb+') as out_file:
        content = await file.read()
        await out_file.write(content)

    return {
        'filename': file.filename,
        'path': path
    }


engine = setup_engine()
SessionLocal = setup_db(engine)
setup_admin(app, engine)
