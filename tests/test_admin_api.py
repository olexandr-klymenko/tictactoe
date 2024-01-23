import json

from app import db
from app.models.models import SeasonModel
from tests.utils.base import BaseTestCase


class TestAdminBlueprint(BaseTestCase):
    def test_start_season(self):
        """Test starting new league season"""
        resp = self.client.post(
            "/api/admin/seasons/",
            json={
                "name": "New season",
            },
        )
        self.assertEqual(resp.status_code, 201)
        retrieved_season = SeasonModel.query.first()
        data = json.loads(resp.data.decode())
        self.assertEqual(retrieved_season.id, data["season_id"])

    def test_list_seasons(self):
        season1 = SeasonModel(name="Test season 1")
        season2 = SeasonModel(name="Test season 2")
        season3 = SeasonModel(name="Test season 3")
        db.session.add_all([season1, season2, season3])
        resp = self.client.get("/api/admin/seasons/")
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data.decode())
        self.assertEqual(
            data,
            [
                {"name": "Test season 3", "season_id": 3},
                {"name": "Test season 2", "season_id": 2},
                {"name": "Test season 1", "season_id": 1},
            ],
        )
