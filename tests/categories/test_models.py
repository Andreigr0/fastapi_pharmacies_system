from categories.models import CategoryModel


def test_create_category_with_children(db_test):
    category = CategoryModel(title='Category 1')
    subcategory = CategoryModel(title='Subcategory 1')
    category.children.append(subcategory)
    db_test.add(category)
    db_test.commit()
    assert subcategory.parent_id == category.id


def test_create_subcategory_with_parent(db_test):
    subcategory = CategoryModel(title='Subcategory 2')
    category = CategoryModel(title='Category 2')
    subcategory.parent = category
    db_test.add(subcategory)
    db_test.commit()
    assert subcategory.parent_id == category.id
