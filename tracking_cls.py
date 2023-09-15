import os
import pickle


class Tracking:
    TRACKING_PATH_DIR = os.path.join(os.getcwd(), 'tracking')
    TRACKING_PATH_FILE_categories = os.path.join(TRACKING_PATH_DIR, 'categories_url.pickle')
    TRACKING_PATH_FILE_products = os.path.join(TRACKING_PATH_DIR, 'products_url.pickle')

    @classmethod
    def check_tracking_categories(cls):
        # create folder
        if not os.path.exists(cls.TRACKING_PATH_DIR):
            os.mkdir(cls.TRACKING_PATH_DIR)

        return os.path.exists(cls.TRACKING_PATH_FILE_categories)

    @classmethod
    def write_categories(cls, categories_url):
        with open(cls.TRACKING_PATH_FILE_categories, 'wb') as f:
            pickle.dump(categories_url, f)


    @classmethod
    def pull_categories(cls):
        with open(cls.TRACKING_PATH_FILE_categories, 'rb') as f:
            data = pickle.load(f)

        return data

    @classmethod
    def del_first_item_categories(cls):
        with open(cls.TRACKING_PATH_FILE_categories, 'rb') as f:
            data = pickle.load(f)
        if len(data) > 1:
            data.pop(0)
            with open(cls.TRACKING_PATH_FILE_categories, 'wb') as f:
                pickle.dump(data, f)
        elif len(data) == 1:
            os.remove(cls.TRACKING_PATH_FILE_categories)

    @classmethod
    def check_tracking_products(cls):
        return os.path.exists(cls.TRACKING_PATH_FILE_products)

    @classmethod
    def write_products(cls, products_url):
        with open(cls.TRACKING_PATH_FILE_products, 'wb') as f:
            pickle.dump(products_url, f)

    @classmethod
    def pull_products(cls):
        with open(cls.TRACKING_PATH_FILE_products, 'rb') as f:
            data = pickle.load(f)

        return data

    @classmethod
    def del_first_item_products(cls):
        with open(cls.TRACKING_PATH_FILE_products, 'rb') as f:
            data = pickle.load(f)
        if len(data) > 1:
            data.pop(0)
            with open(cls.TRACKING_PATH_FILE_products, 'wb') as f:
                pickle.dump(data, f)
        elif len(data) == 1:
            os.remove(cls.TRACKING_PATH_FILE_products)

