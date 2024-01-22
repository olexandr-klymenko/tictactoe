from flask_restx import Resource

from .service import UserService
from .dto import UserDto

api = UserDto.api
data_resp = UserDto.data_resp


@api.route("/<string:username>")
class UserGet(Resource):
    @api.doc(
        "Get a specific user",
        responses={
            200: ("User data successfully sent", data_resp),
            404: "User not found!",
        },
    )
    def get(self, username):
        """Get a specific user's data by their username"""
        return UserService.get_user_data(username)
