import json

from app import db
from app.models.models import SeasonModel, PlayerModel
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

        # make sure new season is in the database
        retrieved_season = SeasonModel.query.first()
        self.assertEqual(retrieved_season.name, "New season")

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

    def test_create_player(self):
        resp = self.client.post(
            "/api/admin/players/",
            json={
                "age": 21,
                "country": "UK",
                "email": "test1@example.com",
                "name": "Test Player1",
            },
        )
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data.decode())
        self.assertEqual(
            data,
            {
                "age": 21,
                "country": "UK",
                "email": "test1@example.com",
                "id": 1,
                "name": "Test Player1",
            },
        )

        # make sure player is in the database
        retrieved_player = PlayerModel.query.first()
        self.assertEqual(retrieved_player.email, "test1@example.com")

    def test_list_players(self):
        player1 = PlayerModel(
            name="Test Player1",
            email="test1@example.com",
            age=21,
            country="UK",
        )
        player2 = PlayerModel(
            name="Test Player2",
            email="test2@example.com",
            age=22,
            country="US",
        )
        db.session.add_all([player1, player2])
        db.session.commit()

        resp = self.client.get("/api/admin/players/")
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data.decode())
        self.assertEqual(
            data,
            [
                {
                    "links": {
                        "collection": "/api/admin/players/",
                        "self": "/api/admin/players/1",
                    },
                    "name": "Test Player1",
                },
                {
                    "links": {
                        "collection": "/api/admin/players/",
                        "self": "/api/admin/players/2",
                    },
                    "name": "Test Player2",
                },
            ],
        )

    def test_get_player(self):
        player = PlayerModel(
            name="Test Player",
            email="test@example.com",
            age=21,
            country="UK",
        )
        db.session.add(player)
        db.session.commit()

        resp = self.client.get(f"/api/admin/players/{player.id}")
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data.decode())
        self.assertEqual(
            data,
            {
                "age": 21,
                "country": "UK",
                "email": "test@example.com",
                "id": 1,
                "name": "Test Player",
            },
        )

    def test_delete_player(self):
        player = PlayerModel(
            name="Test Player",
            email="test@example.com",
            age=21,
            country="UK",
        )
        db.session.add(player)
        db.session.commit()

        resp = self.client.delete(f"/api/admin/players/{player.id}")
        self.assertEqual(resp.status_code, 204)

        # make sure players is removed from the database
        retrieved_player = PlayerModel.query.first()
        self.assertIsNone(retrieved_player)
