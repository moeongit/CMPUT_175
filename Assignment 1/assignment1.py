# This program reads text files (data) from the 2022 World Cup and generates text files based on that data.
# The players function goes through the footballers text function and finds the info of the player
# The same is done for the matches function and the cards function
# I stuck to simple programming here so comments werent really necessary in most spots. I used split and strip and appended things to a list and made most things clean

import codecs

def players(filename):
    players = []
    with codecs.open(filename, "r", "utf-8") as file:
        for line in file:
            stats = line.strip().split(";")
            country_number = stats[0].rsplit(" ", 1)
            country = " ".join(country_number[:-1])
            number = country_number[-1]
            position = stats[1]
            name = stats[2]
            dob, age = stats[3].split(" (")
            age = age.strip("aged ").strip(")")
            players.append({
                "country": country, "number": number, "position": position,
                "name": name, "dob": dob, "age": age})
    return players

def matches(filename):
    matches = []
    with codecs.open(filename, "r", "utf-8") as file:
        for line in file:
            stats = line.strip().split(";")
            if stats[0] and stats[1] and stats[2] and stats[3] and stats[4]:
                group = stats[0]
                team1 = stats[1]
                team2 = stats[2]
                scores = stats[3]
                date = stats[4]
                team1_scores = scores.split(")(")[0].strip("(")
                team2_scores = scores.split(")(")[1].strip(")")
                matches.append({"group": group, "team1": team1, "team2": team2, 
                    "team1_scores": team1_scores, "team2_scores": team2_scores, "date": date})
    return matches

def cards(filename):
    cards = []
    with codecs.open(filename, "r", "utf-8") as file:
        for i, line in enumerate(file):
            stats = line.strip().split(";")
            if len(stats) == 5:
                match, country, name, card_type, time = stats
                cards.append({"match": match, "country": country, "name": name, "type": card_type, "time": time})
    return cards

def write_groups(filename, matches):
    groups = {} # made this a dictionary (easier)
    for match in matches:
        group = match["group"]
        team1 = match["team1"]
        team2 = match["team2"]
        if group not in groups:
            groups[group] = set()
        groups[group].add(team1)
        groups[group].add(team2)
    with open(filename, "w") as file:
        for group, countries in sorted(groups.items()):
            file.write("Group {}\n".format(group))
            print("Group {}".format(group)) # Used the format function to make everything alphabetical
            for country in sorted(countries):
                file.write("{}\n".format(country))
                print("{}".format(country))
            file.write("\n")
            print("")

def average_age(players_function):
    teams = {}
    for player in players_function:
        team = player["country"]
        age = int(player["age"])
        if team not in teams:
            teams[team] = {"players": 0, "age": 0}
        teams[team]["players"] += 1
        teams[team]["age"] += age
    for team in teams.keys():
        teams[team]["average_age"] = round(teams[team]["age"] / teams[team]["players"], 2)
    with open("ages.txt", "w", encoding="utf-8") as f:
        total_players = 0
        total_age = 0
        for team, values in sorted(teams.items()):
            players = values["players"]
            age = values["average_age"]
            total_players += players
            total_age += age * players
            f.write("{:<12}".format(team) + "{:.2f}".format(age) + " years\n") 
            print("{:<12}".format(team) + "{:.2f}".format(age) + " years") 
        f.write("\nAverage Overall " + "{:.2f}".format(total_age/total_players) + " years")
        print("\nAverage Overall " + "{:.2f}".format(total_age/total_players) + " years\n")

def histogram(players_function):
    ages = {}
    for player in players_function:
        age = int(player["age"])
        if age not in ages:
            ages[age] = 0
        ages[age] += 1
    with open("histogram.txt", "w", encoding="utf-8") as file:
        for age in range(18, 41): # Age range 18-40, 41 not exclusive
            if age in ages:
                stars = round(ages[age]/5)
                if stars == 0:
                    stars = 1
                file.write("{} years ({:2d}){}\n".format(age, ages[age],'*' * stars))
                print("{} years ({:2d}){}".format(age, ages[age],'*' * stars))

def most_player_goals():
    players = codecs.open("WC22Footballers.txt", "r", "utf-8")
    goals = {}
    top_scorers = {}
    with codecs.open("WC22GroupMatches.txt", "r", "utf-8") as file:
        for line in file:
            stats = line.strip().split(";")
            if stats[0] and stats[1] and stats[2] and stats[3] and stats[4]:
                group = stats[0].upper()
                team1 = stats[1]
                team2 = stats[2]
                position = stats[3].find(")")
                score1 = stats[3][1:position]
                score2 = stats[3][position + 2:-1]
                score1 = score1.split(",")
                score2 = score2.split(",")
                for number in score1:
                    person = " ".join([team1, number])
                    goals[person] = goals.get(person, 0) + 1
                for number in score2:
                    person = " ".join([team2, number])
                    goals[person] = goals.get(person, 0) + 1
    top_goals = 0
    for player, goal in goals.items():  # this loop finds the maximum goal scored
        if goal > top_goals:
            top_goals = goal
    for player, goal in goals.items():  # this loop finds if others scored the same amout
        if goal == top_goals:
            top_scorers[player] = goal
    for person in players:
        stats = person.split(";")
        player = stats[0]
        name = stats[2]
        if player in top_scorers.keys():
            top_scorers[player] = name
    with open("scorers.txt", "w", encoding="utf-8") as file:
        file.write("+ ------------ + ----------------- + ---------------------------------- +\n")
        print("+ ------------ + ----------------- + ---------------------------------- +")
        for player, name in top_scorers.items():
            player = player.split()
            team = player[0]
            number = player[1]
            file.write(f"|  {top_goals} goals     | {team: <13}     |{number: >3} {name: <32}|\n")
            print(f"|  {top_goals} goals     | {team: <13}     |{number: >3} {name: <32}|")
        file.write("+ ------------ + ----------------- + ---------------------------------- +\n")
        print("+ ------------ + ----------------- + ---------------------------------- +")
        
def most_yellow_cards(cards):
    match_card_count = {}
    for card in cards:
        match = card["match"]
        country = card["country"]
        if match not in match_card_count:
            match_card_count[match] = {}
        if country not in match_card_count[match]:
            match_card_count[match][country] = 0
        match_card_count[match][country] += 1
    max_cards = 0
    max_match = ""
    for match, card_count in match_card_count.items():
        if sum(card_count.values()) > max_cards:
            max_cards = sum(card_count.values())
            max_match = match
    match_name = max_match.split("-")
    match_name = " vs ".join(match_name)
    with open("yellow.txt", "w") as file:
        file.write(match_name + "\n")
        print(f"\n{match_name}")
        for country, count in match_card_count[max_match].items():
            file.write(f"{country}: {count} YC\n")
            print(f"{country}: {count} YC")

def main():
    players_function = players("WC22Footballers.txt")
    matches_function = matches("WC22GroupMatches.txt")
    cards_function = cards("WC22-YellowCards.txt")
    groups = write_groups("groups.txt", matches_function)
    ages = average_age(players_function)
    stars = histogram(players_function)
    most_player_goals()
    most_yellow_cards(cards_function)
main()