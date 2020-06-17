https://cs50.harvard.edu/ai/2020/projects/0/degrees/

Code almost ran without exceptions the first time I tried to run it, except for 2 minor data type / syntax errors that were easily fixed.

Later realised I neglected to skip visited neighours. Also easily fixed with one statement.

• I use a Set() to track visited nodes. Much faster than using a List(). Apparently 8 degrees of separation (Juliane Banse - Julian Acosta) takes 2 seconds for me, but 3 minutes for someone else! (https://us.edstem.org/courses/176/discussion/43314?answer=191752)

---

My comment on https://us.edstem.org/courses/176/discussion/47373?comment=221905

Took 20 minutes.

Frontier size went up to >150k, then dropped to 20173 when the target was found.

370206 nodes visited.

8 degrees of separation.

1: Julian Acosta and Randall Batinkoff starred in True Love

2: Randall Batinkoff and Bruce Davison starred in Touched

3: Bruce Davison and Bono starred in Hero with a Thousand Faces

4: Bono and Angela Gheorghiu starred in Pavarotti

5: Angela Gheorghiu and Alessandro Corbelli starred in Adriana Lecouvreur

6: Alessandro Corbelli and Ramón Vargas starred in The Elixir of Love

7: Ramón Vargas and Regula Mühlemann starred in Of the Voice

8: Regula Mühlemann and Juliane Banse starred in Hunter's Bride

--

In comparison, Emma Watson -> Marilyn Monroe (no connection) takes my program 21 minutes to completely exhaust the frontier and return output that there is no connection.

--

It's amazing how Julian Acosta -> Juliane Banse takes almost as long as a case with no connection.

(I use a visited = set() to track visited nodes. I did not modify the given code at all, but my program does not use contains_state(). My program simply takes the output from neighbors_for_person() and filters out those already in visited . )

--

Juliane Banse -> Julian Acosta takes 3 seconds.

---

Cases with no connection:

• Rene Van Sambeek - Brahma Kumbhar

Searched through around 300k persons, frontier had max size of around 155k persons. Code ran for <30 minutes. I used a Set() to track visited nodes (which should be much faster performance than using List()).

• Emma Watson - Marilyn Monroe

Searched through 377k persons, frontier had max size of around 157k persons. Code ran for 21 minutes.

• {person} - {person}

For my implementation, because the source is set as already visited right from the start, the search algorithm will never visit it again. Hence if source == target, there will be no connection.
