import praw
from collections import Counter, OrderedDict
import matplotlib.pyplot as plt

# Setup reddit stuff
reddit = praw.Reddit(client_id="QjIlbNE2QgZvlA",
                     client_secret="1gK5fam-65K1twGEBQ3Cw_BoFEQ",
                     username="scraper__bot",
                     password="Archie12",
                     user_agent="scraper_user1")

# The post in Q
submission = reddit.submission(url="https://www.reddit.com/r/CasualUK/comments/dz5t3z/its_gotta_be_4c/")
# Make sure it gets it all (Effectivyl clicks show more)
submission.comments.replace_more(limit=0)

# Everything I want to count. 1A, 2A, ...
to_count = [num + char for num in "123456" for char in "ABCDEF"]
backwards_pairs = [char + num for num in "123456" for char in "ABCDEF"]
to_count += backwards_pairs

# Put all of the the words from comments into a list
all_comments = []
for comment in submission.comments.list():
    for word in comment.body.split():
        for x in range(0, comment.score):
            all_comments.append(word.upper())


# Count everything and make it into a list of tuples. [("A1", 2), ("word", 2)...]
counter_obj = list(Counter(all_comments).most_common())

# Make final data from the CHAR/NUM combos
final_data = []
for pair in counter_obj:
    # If they're the wrong way round flip them before adding them
    if pair[0] in backwards_pairs:
        final_data.append((pair[0][::-1], pair[1]))
    elif pair[0] in to_count:
        final_data.append(pair)

# Make a list of the names
numchars = [pair[0] for pair in final_data]

# Make a list of all of the values
values = [pair[1] for pair in final_data]

# Get the positioning right for the x axis
x_pos = [i for i, _ in enumerate(numchars)]


# Draw the bar chart
plt.bar(x_pos, values, color='green')
plt.xlabel("Tea/Toast combination")
plt.ylabel("Number of occurrences multiplied by upvotes")
plt.title("/r/casualuk's favourite tea/toast combination")
plt.xticks(x_pos, numchars)

# Now do similar but just for toast (nums)
# Make a list of all of the characters in the words in the list of all words
all_chars = []
for word in all_comments:
    for char in list(word):
        all_chars.append(char)

# Make the counter obj for toast. Sorted by most common
all_chars_counter_obj = Counter(all_chars).most_common()

toast_data = []
for pair in all_chars_counter_obj:
    # If the first [0] of the ("9", 128) pair is in list 1,2,3,4,5,6 then add to list
    if str(pair[0]) in [str(num) for num in range(1, 7)]:
        toast_data.append(pair)

# Do the toast bar chart
num_occ = dict(toast_data)
r = range(0, len(num_occ))
plt.figure()
# Plot bars
plt.bar(r, num_occ.values())
# Label axis
plt.xticks(r, num_occ.keys())
plt.title("Toast")


# Get the data for toast
tea_data = {"A": 0,
            "B": 0,
            "C": 0,
            "D": 0,
            "E": 0,
            "F": 0}
for pair in final_data:
    if pair[0][1] in tea_data.keys():
        tea_data[pair[0][1]] += pair[1]


# Do the toast bar chart
print(type(tea_data))
char_occ = OrderedDict(sorted(tea_data.items(), key=lambda kv: kv[1], reverse=True))

r = range(0, len(char_occ))
plt.figure()
# Plot bars
plt.bar(r, char_occ.values())
# Label axis
plt.xticks(r, char_occ.keys())
# Title
plt.title("Tea")
plt.show()
