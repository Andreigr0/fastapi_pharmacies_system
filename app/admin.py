from sqladmin import Admin
from sqladmin import ModelAdmin
from sqlalchemy import inspect

from app.models import *


class UserAdmin(ModelAdmin, model=UserModel):
    column_exclude_list = [UserModel.hashed_password]
    form_excluded_columns = [UserModel.hashed_password]


class CategoryAdmin(ModelAdmin, model=CategoryModel):
    column_list = inspect(CategoryModel).columns.keys()


class ProductAdmin(ModelAdmin, model=ProductModel):
    column_list = inspect(ProductModel).columns.keys()
    form_excluded_columns = [ProductModel.min_price, ProductModel.price]


class PharmaciesAdmin(ModelAdmin, model=PharmacyModel):
    column_list = inspect(PharmacyModel).columns.keys()


class BrandAdmin(ModelAdmin, model=BrandModel):
    column_list = inspect(BrandModel).columns.keys()


class FormAdmin(ModelAdmin, model=FormModel):
    column_list = inspect(FormModel).columns.keys()


class ActiveSubstanceAdmin(ModelAdmin, model=ActiveSubstanceModel):
    column_list = inspect(ActiveSubstanceModel).columns.keys()


class DosageAdmin(ModelAdmin, model=DosageModel):
    column_list = inspect(DosageModel).columns.keys()


class ManufacturerAdmin(ModelAdmin, model=ManufacturerModel):
    column_list = inspect(ManufacturerModel).columns.keys()


class CountryAdmin(ModelAdmin, model=CountryModel):
    column_list = inspect(CountryModel).columns.keys()


class ProductImageAdmin(ModelAdmin, model=ProductImageModel):
    column_list = inspect(ProductImageModel).columns.keys()


def setup_admin(app, engine):
    admin = Admin(app, engine)
    admin.register_model(CategoryAdmin)
    admin.register_model(BrandAdmin)
    admin.register_model(FormAdmin)
    admin.register_model(ActiveSubstanceAdmin)
    admin.register_model(DosageAdmin)
    admin.register_model(ManufacturerAdmin)
    admin.register_model(CountryAdmin)
    admin.register_model(ProductImageAdmin)
    admin.register_model(UserAdmin)
    admin.register_model(ProductAdmin)
    admin.register_model(PharmaciesAdmin)
