from flask import Flask, request
from flask_restful import Api, Resource
from datetime import datetime, timedelta

app = Flask(__name__)
api = Api(app)


def calculate_next_watering_date(purchase_date, watering_frequency):
    freq_map = {
        "daily": 1,
        "every 3 days": 3,
        "weekly": 7,
        "bi-weekly": 14,
        "monthly": 30,
    }
    if watering_frequency not in freq_map:
        return None

    purchase_date = datetime.strptime(purchase_date, "%Y-%m-%d")
    days_since_purchase = (datetime.utcnow().date() - purchase_date.date()).days
    if days_since_purchase < 0:
        return None
    days_to_next_watering = freq_map[watering_frequency] - (
        days_since_purchase % freq_map[watering_frequency]
    )
    return datetime.utcnow().date() + timedelta(days=days_to_next_watering)


def calculate_next_fertilizing_date(purchase_date, fertilizing_frequency):
    freq_map = {
        "never": None,
        "weekly": 7,
        "monthly": 30,
        "bi-monthly": 60,
        "seasonally": 90,
    }
    if fertilizing_frequency not in freq_map or fertilizing_frequency == "never":
        return None

    purchase_date = datetime.strptime(purchase_date, "%Y-%m-%d")
    days_since_purchase = (datetime.utcnow().date() - purchase_date.date()).days
    if days_since_purchase < 0:
        return None
    days_to_next_fertilizing = freq_map[fertilizing_frequency] - (
        days_since_purchase % freq_map[fertilizing_frequency]
    )
    return datetime.utcnow().date() + timedelta(days=days_to_next_fertilizing)


class WateringNotificationResource(Resource):
    def post(self):
        plants = request.json.get("plants", [])  # plants["plants"]にアクセス
        upcoming_watering_plants = []
        for plant in plants:
            watering_interval = {
                "daily": 1,
                "every 3 days": 3,
                "weekly": 7,
                "bi-weekly": 14,
                "monthly": 30,
            }.get(plant["watering_frequency"], 7)

            purchase_date = datetime.strptime(plant["purchase_date"], "%Y-%m-%d")
            days_since_purchase = (datetime.utcnow().date() - purchase_date.date()).days
            if days_since_purchase < 0:
                continue
            days_to_next_watering = watering_interval - (
                days_since_purchase % watering_interval
            )
            next_watering_date = datetime.utcnow().date() + timedelta(
                days=days_to_next_watering
            )

            if next_watering_date <= datetime.utcnow().date() + timedelta(
                days=7
            ):  # 次の7日以内に水やりが必要な植物をフィルタ
                upcoming_watering_plants.append(
                    {
                        "name": plant["name"],
                        "next_watering_date": next_watering_date.strftime("%Y-%m-%d"),
                    }
                )

        return {"upcoming_watering_plants": upcoming_watering_plants}, 200


class FertilizingNotificationResource(Resource):
    def post(self):
        plants = request.json.get("plants", [])  # plants["plants"]にアクセス
        upcoming_fertilizing_plants = []
        for plant in plants:
            fertilizing_interval = {
                "daily": 1,
                "every 3 days": 3,
                "weekly": 7,
                "bi-weekly": 14,
                "monthly": 30,
            }.get(plant["fertilizing_frequency"], 30)

            purchase_date = datetime.strptime(plant["purchase_date"], "%Y-%m-%d")
            days_since_purchase = (datetime.utcnow().date() - purchase_date.date()).days
            if days_since_purchase < 0:
                continue
            days_to_next_fertilizing = fertilizing_interval - (
                days_since_purchase % fertilizing_interval
            )
            next_fertilizing_date = datetime.utcnow().date() + timedelta(
                days=days_to_next_fertilizing
            )

            if next_fertilizing_date <= datetime.utcnow().date() + timedelta(
                days=7
            ):  # 次の7日以内に施肥が必要な植物をフィルタ
                upcoming_fertilizing_plants.append(
                    {
                        "name": plant["name"],
                        "next_fertilizing_date": next_fertilizing_date.strftime(
                            "%Y-%m-%d"
                        ),
                    }
                )

        return {"upcoming_fertilizing_plants": upcoming_fertilizing_plants}, 200


api.add_resource(WateringNotificationResource, "/watering_notifications")
api.add_resource(FertilizingNotificationResource, "/fertilizing_notifications")

if __name__ == "__main__":
    app.run()
