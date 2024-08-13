from flask import Flask, request
from flask_restful import Api, Resource
from datetime import datetime, timedelta

app = Flask(__name__)
api = Api(app)


class WateringNotificationResource(Resource):
    def post(self):
        plants = request.json.get("plants", [])
        if not plants:
            return {"message": "Plants data is required"}, 400

        upcoming_watering_plants = []
        for plant in plants:
            watering_interval = {
                "daily": 1,
                "every 3 days": 3,
                "weekly": 7,
                "bi-weekly": 14,
                "monthly": 30,
            }.get(plant["watering_frequency"], 7)

            last_watering_date = datetime.strptime(
                plant["last_watering_date"], "%Y-%m-%d"
            )
            next_watering_date = last_watering_date + timedelta(days=watering_interval)

            if next_watering_date <= datetime.utcnow():
                upcoming_watering_plants.append(
                    {
                        "name": plant["name"],
                        "next_watering_date": next_watering_date.strftime("%Y-%m-%d"),
                    }
                )

        return {"upcoming_watering_plants": upcoming_watering_plants}, 200


class FertilizingNotificationResource(Resource):
    def post(self):
        plants = request.json.get("plants", [])
        if not plants:
            return {"message": "Plants data is required"}, 400

        upcoming_fertilizing_plants = []
        for plant in plants:
            fertilizing_interval = {
                "daily": 1,
                "every 3 days": 3,
                "weekly": 7,
                "bi-weekly": 14,
                "monthly": 30,
            }.get(plant["fertilizing_frequency"], 30)

            last_fertilizing_date = datetime.strptime(
                plant["last_fertilizing_date"], "%Y-%m-%d"
            )
            next_fertilizing_date = last_fertilizing_date + timedelta(
                days=fertilizing_interval
            )

            if next_fertilizing_date <= datetime.utcnow():
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
