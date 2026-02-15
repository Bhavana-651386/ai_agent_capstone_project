import pandas as pd
import numpy as np
import os


def generate_cpg_data(output_path="data/cpg_sales_sample_5000.csv", num_rows=5000):
    np.random.seed(42)

    # Parameters
    date_range = pd.date_range("2022-01-01", "2024-12-31")
    stores = list(range(1, 11))
    regions = ["North", "South", "East"]
    skus = list(range(101, 151))
    categories = ["Beverages", "Snacks", "Dairy", "Household", "Personal Care"]
    promo_types = ["Discount", "BuyOneGetOne", "FlashSale"]
    store_sizes = ["Small", "Medium", "Large"]

    data = []

    for _ in range(num_rows):

        date = np.random.choice(date_range)
        store = np.random.choice(stores)
        region = np.random.choice(regions)
        sku = np.random.choice(skus)
        category = np.random.choice(categories)

        base_price = np.round(np.random.uniform(2, 10), 2)

        promo_flag = np.random.choice([0, 1], p=[0.8, 0.2])
        promo_type = np.random.choice(promo_types) if promo_flag else None

        price = base_price * (0.8 if promo_flag else 1.0)

        # Seasonality logic (weekends higher sales)
        seasonal_multiplier = 1.2 if pd.Timestamp(date).weekday() >= 5 else 1.0

        units_sold = np.random.poisson(15) * seasonal_multiplier
        revenue = units_sold * price

        inventory_level = np.random.randint(100, 1000)
        store_size = np.random.choice(store_sizes)

        holiday_flag = 1 if pd.Timestamp(date).weekday() >= 5 else 0

        data.append([
            date, store, region, sku, category,
            int(units_sold), revenue, promo_flag,
            promo_type, price, inventory_level,
            store_size, holiday_flag
        ])

    df = pd.DataFrame(data, columns=[
        "date", "store_id", "store_region", "sku_id", "category",
        "units_sold", "revenue", "promo_flag", "promo_type",
        "price", "inventory_level", "store_size", "holiday_flag"
    ])

    os.makedirs("data", exist_ok=True)
    df.to_csv(output_path, index=False)

    print(f"Dataset generated successfully at {output_path}")


if __name__ == "__main__":
    generate_cpg_data()
