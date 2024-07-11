from matplotlib import pyplot as plt
from collections import defaultdict
from collections import Counter
############################
## Finding Key connectors ##
############################
users = [
    {"id":0, "name":"Hero"},
    {"id":1, "name":"Dunn"},
    {"id":2, "name":"Sue"},
    {"id":3, "name":"Thor"},
    {"id":4, "name":"Clive"},
    {"id":5, "name":"Hicks"},
    {"id":6, "name":"Devin"},
    {"id":7, "name":"Kate"},
    {"id":8, "name":"Klein"},
    {"id":9, "name":"Chi"},
]

friendships = [ (0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4), (4, 5), (5, 6), (5, 7), (6, 8), (7, 8), (8, 9)]

# first give each user an empty list
for user in users:
    user['friends'] = []
# then populate the lists with friendships
for i,j in friendships:
    users[i]["friends"].append(users[j])
    users[j]["friends"].append(users[i])
def number_of_friends(user):
    """how many friends does _user_ have?"""
    return len(user["friends"])
total_connections = sum(number_of_friends(user) for user in users)
num_users = len(users)
avg_connections = total_connections / num_users
# get number of friends by users
num_friends_by_id = [(user["id"], number_of_friends(user)) for user in users]
# sort by asc order of count of friends
num_friends_by_id.sort(
    key=lambda id_and_friends: id_and_friends[1],
    reverse=True
)
print('numb_fr_id', num_friends_by_id)

interests = [
    (0, "Hadoop"), (0, "Big Data"), (0, "HBase"), (0, "Java"),
    (0, "Spark"), (0, "Storm"), (0, "Cassandra"),
    (1, "NoSQL"), (1, "MongoDB"), (1, "Cassandra"), (1, "HBase"),
    (1, "Postgres"), (2, "Python"), (2, "scikit-learn"), (2, "scipy"),
    (2, "numpy"), (2, "statsmodels"), (2, "pandas"), (3, "R"), (3, "Python"),
    (3, "statistics"), (3, "regression"), (3, "probability"),
    (4, "machine learning"), (4, "regression"), (4, "decision trees"),
    (4, "libsvm"), (5, "Python"), (5, "R"), (5, "Java"), (5, "C++"),
    (5, "Haskell"), (5, "programming languages"), (6, "statistics"),
    (6, "probability"), (6, "mathematics"), (6, "theory"),
    (7, "machine learning"), (7, "scikit-learn"), (7, "Mahout"),
    (7, "neural networks"), (8, "neural networks"), (8, "deep learning"),
    (8, "Big Data"), (8, "artificial intelligence"), (9, "Hadoop"),
    (9, "Java"), (9, "MapReduce"), (9, "Big Data")
]

def data_scientists_who_like(target_interest):
    return [
        user_id
        for user_id, user_interest in interests
        if user_interest == target_interest
    ]
# keys are id-s, values are interests
user_id_by_interest = defaultdict(list)
for user_id, interest in interests:
    user_id_by_interest[user_id].append(interest)
interests_by_user_id = defaultdict(list)
for user_id, interest in interests:
    interests_by_user_id[interest].append(user_id)
# Get the most common interest
def most_common_interests_with(user_id):
    return Counter(interested_user_id
        for interest in interests_by_user_id["user_id"]
        for interested_user_id in user_ids_by_interest[interest]
        if interested_user_id != user_id)


##############################
#   Salaries and Experience  #
##############################

salaries_and_tenures = [
    (83000, 8.7), (88000, 8.1),
    (48000, 0.7), (76000, 6),
    (69000, 6.5), (76000, 7.5),
    (60000, 2.5), (83000, 10),
    (48000, 1.9), (63000, 4.2)
]

def make_chart_salaries_by_tenure():
    tenures = [tenure for salary, tenure in salaries_and_tenures]
    salaries = [ salary for salary, tenure in salaries_and_tenures]
    plt.scatter(tenures, salaries)
    plt.xlabel("years of experience")
    plt.ylabel("salary")
    plt.show()
# Take the average of the salary by tenures
# first show salaries by tenures
salary_by_tenure = defaultdict(list)
for salary, tenure in salaries_and_tenures:
    salary_by_tenure[tenure].append(salary)
# get average salary by years of experience
average_salary_by_tenure = {
    tenure : sum(salaries) / len(salaries)
    for tenure, salaries in salary_by_tenure.items()
}
print("average_salary_by_tenure", average_salary_by_tenure)
# all employes have different tenures, need grouping
def tenure_backet(tenure):
    if tenure<2:
        return "less than 2"
    elif tenure < 5:
        return "between 2 and 5"
    else:
        return "more than 5"
salary_by_tenure_bucket = defaultdict(list)
for salary, tenure in salaries_and_tenures:
    bucket = tenure_backet(tenure)
    salary_by_tenure_bucket[bucket].append(salary)
average_salary_by_bucket = {
    tenure_backet: sum(salaries) / len(salaries)
    for tenure_backet, salaries in salary_by_tenure_bucket.items()
}
print("average_salary_by_bucket", average_salary_by_bucket)

variance = [1,2,4,8,16,32,64,128,256]
bias_squared=[256, 128, 64, 32, 16, 8,4,2,1]
total_error = [x+y for x,y in zip(variance, bias_squared)]
sx = [i for i, _ in enumerate(variance)]

print('total_error', sx)