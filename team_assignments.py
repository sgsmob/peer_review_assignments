import argparse as ap


# Read the team sizes file into a list of team sizes.
def read_team_sizes(input_file):
    with open(input_file) as f:
        size_of_team = []
        for line in f:
            size_of_team.append(int(line.strip()))
        return size_of_team


# Create an index mapping a team size to all teams larger than that size, as
# well as an index indicating the position of each team in the size-indexed
# lists.
def get_teams_of_size(teams_list):
    teams_of_size = [list() for _ in range(max(teams_list))]
    teams_of_size_index = [dict() for _ in teams_of_size]
    for team, size in enumerate(teams_list):
        for i in range(size):
            teams_of_size_index[i][team] = len(teams_of_size[i])
            teams_of_size[i].append(team)
    return teams_of_size, teams_of_size_index


# Compute the list of review assignments that each person will do.
def compute_assignments_of_person(team_of_person, member_idx_of_person,
                                  teams_of_size, teams_of_size_index, offsets):
    assignments_of_person = [list() for _ in team_of_person]
    for assignment, (offset, teams_of_same_size, teams_of_same_size_index) in\
            enumerate(zip(offsets, teams_of_size, teams_of_size_index)):
        for person, (team, member_idx) in\
                enumerate(zip(team_of_person, member_idx_of_person)):
            idx_ahead_to_review = ((member_idx + 1) * (assignment + 1)) %\
                (len(teams_of_same_size) - 1)
            team_to_review = teams_of_same_size[(teams_of_same_size_index[team]
                                                + idx_ahead_to_review) %
                                                len(teams_of_same_size)]
            assignments_of_person[person].append(team_to_review)
    return assignments_of_person


# Validate that a given assignment of reviews to people satisfies the
# constraints.
def validate(assignments_of_person, team_of_person, num_reviews, size_of_team):
    reviews_of_team_in_round = [[list() for __ in range(num_reviews)]
                                for _ in size_of_team]
    for person, assignments in enumerate(assignments_of_person):
        assert len(assignments) == num_reviews,\
            "Person {} has insufficient assignments:  {}"\
            .format(person, assignments)
        assert len(set(assignments)) == len(assignments),\
            "Person {} has duplicate assignments:  {}"\
            .format(person, assignments)
        assert len(assignments) == num_reviews,\
            "Person {} is assigned to their own team:  {}"\
            .format(person, assignments)
        for i, t in enumerate(assignments):
            reviews_of_team_in_round[t][i].append(person)

    # TODO: Fix the issue so the team size equals the number of reviewers in
    # each round.
    # for s, rs in zip(size_of_team, reviews_of_team_in_round):
    #     print(s, rs)
    # for team, (size, counts) in\
    #         enumerate(zip(size_of_team, reviews_of_team_in_round)):
    #     for r, c in enumerate(counts):
    #         assert size == len(c),\
    #             "Team {} has size {} but reviewers {} from teams {} in round {}"\
    #             .format(team, size, c, [team_of_person[x] for x in c], r)


# Write the review assignments to file.
def write(assignments_of_person, output_file):
    with open(output_file, 'w') as f:
        for person, assignments in enumerate(assignments_of_person):
            line = str(person)
            for assignment in assignments:
                line += ",{}".format(assignment)
            f.write(line + "\n")


def main(args):
    size_of_team = read_team_sizes(args.team_sizes)
    num_reviews = args.num_reviews
    output_file = args.output_file

    #
    # Initialize lookup tables
    #
    # Team that a person belongs to.
    team_of_person = []
    # Ordinal rank of person among members of their team.
    member_idx_of_person = []
    for i, team_size in enumerate(size_of_team):
        for j in range(team_size):
            team_of_person.append(i)
            member_idx_of_person.append(j)
    # Number of teams that the i-th member of the team should skip to find
    # their next assignment.
    # TODO:  select offsets that avoid collisions when wrapping around
    offsets = range(1, 6)
    teams_of_size, teams_of_size_index = get_teams_of_size(size_of_team)

    assignments_of_person = compute_assignments_of_person(team_of_person,
                                                          member_idx_of_person,
                                                          teams_of_size,
                                                          teams_of_size_index,
                                                          offsets)
    write(assignments_of_person, output_file)
    validate(assignments_of_person, team_of_person, num_reviews, size_of_team)


if __name__ == "__main__":
    parser = ap.ArgumentParser()
    parser.add_argument("team_sizes", help="filename with team sizes")
    parser.add_argument("num_reviews", type=int,
                        help="number of reviews per person")
    parser.add_argument("output_file",
                        help="filename where the output will be written")
    main(parser.parse_args())
