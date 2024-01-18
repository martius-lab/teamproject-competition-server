import teamprojekt_competition_server.server.user_database as user_db
import logging

# run with python -m tests.user_database_test

logging.basicConfig(level=logging.DEBUG)


def user_database_tests():
    userID1 = user_db.add_user(user_name = "player_1", user_token= 123)
    userID2 = user_db.add_user(user_name = "player_2", user_token= 456)
    userID3 = user_db.add_user(user_name = "player_3", user_token= 789)
    userID4 = user_db.add_user(user_name = "player_4", user_token= 444)
    print(userID1, userID2, userID3, userID4)
    
    assert userID1 % 3 == 1 and userID2 % 3 == 2 and userID3 % 3 == 0 and userID4 % 3 == 1
    all_users = user_db.get_all_users()
    print(all_users)
    assert len(all_users) == 4

    user = user_db.get_user(id = userID1)
    print(f"User ID: {user[0]}, Name: {user[1]}, Token: {user[2]}, Mu: {user[3]}, Sigma: {user[4]}")

    user_db.update_user_TS(id=userID3, new_mu= 24.000, new_sigma=9.333)
    user = user_db.get_user(id = userID3)
    assert user[3] == 24.000 and user[4] == 9.333

    user_db.delete_user(userID4)
    all_users = user_db.get_all_users()
    assert len(all_users) == 3



if __name__ == "__main__":
    # user_database_tests()  # only enable for manual testing
    pass