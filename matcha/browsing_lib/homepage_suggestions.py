from flask import g, session
from matcha.common_lib.query import query_db


def browsing_lib_get_suggested_user_profiles(user):

    interests = query_db("SELECT * FROM interests WHERE username=?", (user['username'],))
    fame = user['fame']
    age = user['age']

    interest_profiles = interest_suggestions(interests)

    sex_profiles = sexual_suggestions(user)

    fame_profiles = fame_suggestions(user)

    all_profiles = all_suggestions(sex_profiles, fame_profiles, interest_profiles)

    return all_profiles, sex_profiles, fame_profiles, interest_profiles


def all_suggestions(sex_profiles, fame_profiles, interest_profiles):

    suggestions = []

    unique_name_list = []

    for profile in sex_profiles:
        if profile['username'] not in unique_name_list:
            unique_name_list.append(profile['username'])
            suggestions.append(profile)

    for profile in fame_profiles:
        if profile['username'] not in unique_name_list:
            unique_name_list.append(profile['username'])
            suggestions.append(profile)

    for profile in interest_profiles:
        if profile['username'] not in unique_name_list:
            unique_name_list.append(profile['username'])
            suggestions.append(profile)

    return suggestions


def sexual_suggestions(user):

    sex = user['sex_orientation']

    gender_filter = 'All'

    if sex == 'Homosexual':
        sex_filter = 'Homosexual'
        if user['gender'] == 'Male':
            gender_filter = 'Male'
        elif user['gender'] == 'Female':
            gender_filter = 'Female'

        if gender_filter == 'All':
            suggestions = query_db("SELECT * FROM users WHERE sex_orientation=? AND NOT username=?",
                                   (sex_filter, session['username']))
        else:
            suggestions = query_db("SELECT * FROM users WHERE gender=? AND sex_orientation=? AND NOT username=?",
                                   (gender_filter, sex_filter, session['username']))

    elif sex == 'Heterosexual':
        sex_filter = 'Heterosexual'
        if user['gender'] == 'Male':
            gender_filter = 'Female'
        elif user['gender'] == 'Female':
            gender_filter = 'Male'

        if gender_filter == 'All':
            suggestions = query_db("SELECT * FROM users WHERE sex_orientation=? AND NOT username=?",
                                   (sex_filter, session['username']))
        else:
            suggestions = query_db("SELECT * FROM users WHERE gender=? AND sex_orientation=? AND NOT username=?",
                                   (gender_filter, sex_filter, session['username']))

    else:

        suggestions = query_db("SELECT * FROM users AND NOT username=?", (session['username'],))

    return suggestions


def fame_suggestions(user):

    fame = user['fame']

    suggestions = query_db("SELECT * FROM users WHERE fame>=? AND NOT username=?", (fame, session['username']))

    return suggestions


def interest_suggestions(user_interests):

    suggestions = []

    interest_profiles = query_db("SELECT * FROM interests WHERE NOT username=?", (session['username'],))

    for user_interest in user_interests:
        for interest in interest_profiles:
            if parse_interest(user_interest, interest):
                user = query_db("SELECT * FROM users WHERE username=?", (interest['username'],))
                for v in user:
                    suggestions.append(v)

    return suggestions


def parse_interest(user, interest):


    interest_count = 0

    if interest['travelling'] == 1 and user['travelling'] == 1: interest_count += 1
    if interest['exercise'] == 1 and user['exercise'] == 1: interest_count += 1
    if interest['movies'] == 1 and user['movies'] == 1: interest_count += 1
    if interest['dancing'] == 1 and user['dancing'] == 1: interest_count += 1
    if interest['cooking'] == 1 and user['cooking'] == 1: interest_count += 1
    if interest['outdoors'] == 1 and user['outdoors'] == 1: interest_count += 1
    if interest['politics'] == 1 and user['politics'] == 1: interest_count += 1
    if interest['pets'] == 1 and user['pets'] == 1: interest_count += 1
    if interest['photography'] == 1 and user['photography'] == 1: interest_count += 1
    if interest['sports'] == 1 and user['sports'] == 1: interest_count += 1

    return True if interest_count >= 3 else False


