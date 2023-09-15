from spider_cls import Spider
from tracking_cls import Tracking
from save_to_json import save

if __name__ == "__main__":

    if Tracking.check_tracking_categories():
        categories_url = Tracking.pull_categories()
    else:
        categories_url = Spider.get_categories_links()
        Tracking.write_categories(categories_url)

    for category in categories_url:
        if Tracking.check_tracking_products():
            products_url = Tracking.pull_products()
        else:
            products_url = Spider.get_products_links(category)
            Tracking.write_products(products_url)

        for product_url in products_url:
            product_content = Spider.get_product_content(product_url)
            save(product_content)
            Tracking.del_first_item_products()
        Tracking.del_first_item_categories()
