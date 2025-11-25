import pandas as pd
import os

def load_data(data_path = "data/raw"):
    try:
        # 1. Chargement des tables
        orders = pd.read_csv(os.path.join(data_path, "olist_orders_dataset.csv"))
        items = pd.read_csv(os.path.join(data_path, "olist_order_items_dataset.csv"))
        products = pd.read_csv(os.path.join(data_path, "olist_products_dataset.csv"))
        customers = pd.read_csv(os.path.join(data_path, "olist_customers_dataset.csv"))
        geo = pd.read_csv(os.path.join(data_path, "olist_geolocation_dataset.csv"))
        trans = pd.read_csv(os.path.join(data_path, "product_category_name_translation.csv"))
        
        # Chargement des Reviews (Notes 1 à 5 étoiles)
        reviews = pd.read_csv(os.path.join(data_path, "olist_order_reviews_dataset.csv"))

        # 2. Préparation des Dates & Calcul du Délai Logistique
        orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
        orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'])
        
        # Calcul du "Lead Time" (Temps entre achat et réception réelle) + On stocke le résultat en jours (float)
        orders['delivery_days'] = (orders['order_delivered_customer_date'] - orders['order_purchase_timestamp']).dt.days

        # 3. Optimisation Géo
        geo_agg = geo.groupby("geolocation_zip_code_prefix").agg({
            "geolocation_lat": "mean",
            "geolocation_lng": "mean"
        }).reset_index()
        
        # 4. Merges
        df = items.merge(orders, on = "order_id", how = "left")
        df = df.merge(products, on = "product_id", how = "left")
        df = df.merge(customers, on = "customer_id", how = "left")
        df = df.merge(geo_agg, left_on = "customer_zip_code_prefix", right_on = "geolocation_zip_code_prefix", how = "left")
        df = df.merge(trans, on = "product_category_name", how = "left")
        
        # On attache la note (score) à la commande
        # Disclaimer !! Une commande peut avoir plusieurs reviews, on prend la première pour simplifier
        reviews_agg = reviews.groupby("order_id")['review_score'].mean().reset_index()
        df = df.merge(reviews_agg, on = "order_id", how = "left")

        # 5. Nettoyage final
        df['product_category_name_english'] = df['product_category_name_english'].fillna("Others").str.replace('_', ' ').str.title()
        df['total_sales'] = df['price'] + df['freight_value']
        
        # On supprime les délais aberrants (bugs de date ou retours en 1970) pour ne pas fausser le graphique
        df = df[df['delivery_days'] > 0] 

        return df

    except Exception as e:
        print(f"Erreur loader : {e}")
        return None