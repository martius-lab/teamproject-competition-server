# import comprl.server.user_database as user_db
# import logging
# import uuid

# # run with python -m tests.user_database_test

# logging.basicConfig(level=logging.DEBUG)


# def user_database_tests():
#     tokens = [uuid.uuid4() for _ in range(4)]
#     userID1 = user_db.add_user(user_name="player_1", user_token=tokens[0])
#     userID2 = user_db.add_user(user_name="player_2", user_token=tokens[1])
#     userID3 = user_db.add_user(user_name="player_3", user_token=tokens[2])
#     userID4 = user_db.add_user(user_name="player_4", user_token=tokens[3])
#     print(userID1, userID2, userID3, userID4)

#     assert (
#           userID1 % 4 == 1 and
#           userID2 % 4 == 2 and
#           userID3 % 4 == 3 and
#           userID4 % 4 == 0
#     )
#     all_users = user_db.get_all_users()
#     print(all_users)
#     assert len(all_users) == 4
#     assert user_db.verify_user(tokens[0]) == userID1

#     user = user_db.get_user(id=userID1)
#     print(
#         f"User ID: {user[0]}, Name: {user[1]}, \
#           Token: {user[2]}, Mu: {user[3]}, Sigma: {user[4]}"
#     )

#     user_db.update_matchmaking_parameters(id=userID3, new_mu=24.000, new_sigma=9.333)
#     (mu, sigma) = user_db.get_matchmaking_parameters(id=userID3)
#     assert mu == 24.000 and sigma == 9.333

#     user_db.delete_user(userID4)
#     all_users = user_db.get_all_users()
#     assert len(all_users) == 3

#     # print(user_db.verify_user(uuid.uuid4()))


# def insert_users():
#     token1 = "e3a0222f-2b8b-49e2-8305-7c5a3c9b48c6"
#     token2 = "1a11abc1-774d-4582-9519-4ae28c5ae4d3"
#     user_db.add_user(user_name="hallo", user_token=token1)
#     user_db.add_user(user_name="hey", user_token=token2)


# if __name__ == "__main__":
#     insert_users()
#     # user_database_tests()  # only enable for manual testing
#     pass
