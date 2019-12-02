# peer_review_assignments
Given a set of groups of people, assign each person a set of teams whose work they will review.

## Usage
`python team_assignments.py [team_sizes] [num_reviews] [output_file]`

Use the `-h` flag for more details

Arguments:
  * `team_sizes`:  Filename whose contents are the sizes of the teams, one size per line.
  * `num_reviews`:  Integer number of reviews per person.
  * `output_file`:  Filename to write the results.  File format has a row for each person (0-indexed!), each of which contains their team, and then then teams they need to review, in order.

## Algorithm overview
We order the teams 0,...,_n_-1, where _n_ is the number of teams and each member of the team 0,...,_m_-1, where _m_ is the size of the team.  Suppose we want 5 reviews.
  * Person 0 of team 0 reviews teams \[1, 2, 3, 4, 5\]
  * Person 1 of team 0 reviews teams \[1, 3, 5, 7, 9\]
  * Person 2 of team 0 reviews teams \[1, 4, 7, 10, 13\]
  * Person 0 of team 1 reviews teams \[2, 3, 4, 5, 6\]
  * etc.
