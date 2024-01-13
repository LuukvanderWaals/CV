%++++++++++++++++++++++++++++++++++++++++++++++++++++
% PSS − Homework assignment 5
% Tutor group G
% Luuk van der Waals, Bachelor Programme in Computer Science, 3rd year
% luuk.van.der.waals@student.uva.nl
  /*
   * I hereby declare I have actively participated
   * in solving every exercise. All solutions are
   * entirely my own work and no part has been
   * copied from other sources.
   */
% hours in lab: 4
% hours spent on homework assignment: 9
%++++++++++++++++++++++++++++++++++++++++++++++++++++
% Question 1
%++++++++++++++++++++++++++++++++++++++++++++++++++++



% Source: GraphHopper
distance(amsterdam, haarlem, 20).
distance(amsterdam, groningen, 183).
distance(amsterdam, leeuwarden, 134).
distance(amsterdam, rotterdam, 77).
distance(amsterdam, utrecht, 44).
distance(amsterdam, zwolle, 106).
distance(breda, eindhoven, 64).
distance(breda, hertogenbosch, 52).
distance(breda, rotterdam, 49).
distance(breda, utrecht, 72).
distance(eindhoven, hertogenbosch, 35).
distance(eindhoven, maastricht, 90).
distance(eindhoven, zwolle, 149).
distance(groningen, leeuwaren, 64).
distance(groningen, utrecht, 188).
distance(groningen, zwolle, 106).
distance(haarlem, leeuwarden, 143).
distance(haarlem, rotterdam, 72).
distance(haarlem, utrecht, 57).
distance(hertogenbosch, rotterdam, 81).
distance(hertogenbosch, utrecht, 54).
distance(hertogenbosch, zwolle, 131).
distance(leeuwarden, utrecht, 163).
distance(leeuwarden, zwolle, 97).
distance(maastricht, zwolle, 231).
distance(rotterdam, utrecht, 57).
distance(utrecht, zwolle, 90).

% Sourse: Google maps
coordinates(amsterdam, 52.367573/4.904139).
coordinates(breda, 51.571915/4.768323).
coordinates(eindhoven, 51.423142/5.46229).
coordinates(groningen, 53.219384/6.566502).
coordinates(haarlem, 52.387388/4.646219).
coordinates(hertogenbosch, 51.697816/5.303675).
coordinates(leeuwarden, 53.201233/5.799913).
coordinates(maastricht, 50.851368/5.690973).
coordinates(rotterdam, 51.92442/4.477733).
coordinates(utrecht, 52.090737/5.12142).
coordinates(zwolle, 52.516775/6.083022).



%++++++++++++++++++++++++++++++++++++++++++++++++++++
% Question 2
%++++++++++++++++++++++++++++++++++++++++++++++++++++



% --- move/3 ---
% Gives the next possible city to go to and the distance to that city.

move(City1, City2, Distance) :-
    distance(City1, City2, Distance);
    distance(City2, City1, Distance).



%++++++++++++++++++++++++++++++++++++++++++++++++++++
% Question 3
%++++++++++++++++++++++++++++++++++++++++++++++++++++



% --- estimate / 2 ---
% Estimates the distance between two cities by using the distance in one
% straight line between the two cities.

estimate(City1, Distance) :-
    coordinates(City1, Latitude1/Longitude1),
    goal(City2),
    coordinates(City2, Latitude2/Longitude2),
    AvgLatitude is (Latitude1 + Latitude2) / 2,
    X is abs(Longitude1 - Longitude2) * 111 * cos(AvgLatitude / 180 * pi),
    Y is abs(Latitude1 - Latitude2) * 111,
    Distance is sqrt(X * X + Y * Y).



%++++++++++++++++++++++++++++++++++++++++++++++++++++
% Question 4
%++++++++++++++++++++++++++++++++++++++++++++++++++++



solve_astar(Node, Path/Cost) :-
    estimate(Node, Estimate),
    astar([[Node]/0/Estimate], RevPath/Cost/_),
    reverse(RevPath, Path).



move_astar([Node|Path]/Cost/_, [NextNode, Node|Path]/NewCost/Est) :-
    move(Node, NextNode, StepCost),
    \+ member(NextNode, Path),
    NewCost is Cost + StepCost,
    estimate(NextNode, Est).



expand_astar(Path, ExpPaths) :-
    findall(NewPath, move_astar(Path, NewPath), ExpPaths).



get_best([Path], Path) :- !.

get_best([Path1/Cost1/Est1, _/Cost2/Est2 | Paths], BestPath) :-
    Cost1 + Est1 =< Cost2 + Est2, !,
    get_best([Path1/Cost1/Est1 | Paths], BestPath).

get_best([_ | Paths], BestPath) :-
    get_best(Paths, BestPath).



astar(Paths, Path) :-
    get_best(Paths, Path),
    Path = [Node|_]/_/_,
    goal(Node).

astar(Paths, SolutionPath) :-
    get_best(Paths, BestPath),
    select(BestPath, Paths, OtherPaths),
    expand_astar(BestPath, ExpPaths),
    append(OtherPaths, ExpPaths, NewPaths),
    astar(NewPaths, SolutionPath).



% --- route/4 ---
% Give a possible route to from one city to another, starting with the shortest
% route, using the A*-algorithm.
route(City1, City2, Route, Distance) :-
    retractall(goal(_)),
    asserta(goal(City2)),
    solve_astar(City1, Route/Distance).



%++++++++++++++++++++++++++++++++++++++++++++++++++++
% Question 5
%++++++++++++++++++++++++++++++++++++++++++++++++++++



% ?- route(breda, haarlem, Route, Distance).
% Route = [breda, rotterdam, haarlem],
% Distance = 121 ;
% Route = [breda, utrecht, haarlem],
% Distance = 129 ;
% Route = [breda, utrecht, amsterdam, haarlem],
% Distance = 136 .

% ?- route(amsterdam, groningen, Route, Distance).
% Route = [amsterdam, groningen],
% Distance = 183 ;
% Route = [amsterdam, zwolle, groningen],
% Distance = 212 ;
% Route = [amsterdam, utrecht, groningen],
% Distance = 232 .



%++++++++++++++++++++++++++++++++++++++++++++++++++++
% Question 6
%++++++++++++++++++++++++++++++++++++++++++++++++++++



% The addition: an animation!
% Example:
% ?- route(amsterdam, maastricht, Route, _), animate(Route).
%
% (Or to just draw the route without an animation:)
% ?- route(amsterdam, maastricht, Route, _), path(Route, Path), draw(Path).



% Coordinates of the cities on the map.
city(amsterdam, 31/21).
city(breda, 28/34).
city(eindhoven, 43/36).
city(groningen, 64/6).
city(haarlem, 26/19).
city(hertogenbosch, 40/31).
city(leeuwarden, 48/6).
city(maastricht, 47/46).
city(rotterdam, 20/28).
city(utrecht,37/25).
city(zwolle, 54/18).

% The map of The Netherlands.
map(["                                                               _",
     "                                                         ___  |_|",
     "                                         ___   ___      |___|    _______",
     "                                     ___|___| |___|_____________|       |",
     "                                   _|___|      ___|                     |___",
     "                               ___|_|        _|                             |",
     "                              |___|        _|                               |_",
     "                             ___          |                                   |",
     "                            |   |        _|                                   |",
     "                           _|  _|       |                                     |",
     "                          |  _|         |_                                    |",
     "                          |_|_   _       _|                                  _|",
     "                           _| |_| |_    |_____                              |",
     "                          |         |         |                             |",
     "                          |         |___     _|                             |",
     "                          |            _|   |                               |",
     "                          |        ___|     |_                       _______|",
     "                         _|       |        ___|                     |",
     "                        |         |      _|                         |",
     "                        |         |_   _|                           |_____",
     "                        |        ___|_|                                   |_",
     "                       _|       |___|                                      _|",
     "                      |                                                   |_",
     "                     _|                                                  ___|",
     "                   _|                                                   |",
     "                 _|                                                  ___|",
     "                |                                                   |_",
     "             ___|                                                     |",
     "            |_                                           _       _____|",
     "           ___|_                                     ___| |_____|",
     "          |   |_|_                                  |",
     "       ___|     |_|                                 |_",
     "      |___                                            |_",
     "   _______|_                                            |",
     "  |       |_|  _                                        |_",
     "  |_          |_|    ___   ___   ___                      |",
     " ___|___   _   ___  |_  |_|   |_|  _|                     |",
     "|   |___| |_| |_  |___|           |_                      |",
     "|    ___       _|                   |_     _             _|",
     "|___|   |_____|                       |___| |_         _|",
     "                                              |___    |___",
     "                                                  |    ___|",
     "                                                 _|  _|",
     "                                                |   |_",
     "                                               _|     |_",
     "                                              |        _|",
     "                                              |       |",
     "                                              |_______|"]).



% --- animate/1 ---
% Turnes the route into a path, which contains the coordinates of the path that
% has te be drawn on the map. Call animate/2 to start the animation.

animate(Route) :-
    path(Route, Path),
    animate([], Path).

% --- animate/2 ---
% Ad one of the coordinates of the path to the path that is drawn and repeat
% this using recursion. Each recursive step sleeps 0.1 second.

animate(_, []).

animate(Path1, [H | Path2]) :-
    draw([H | Path1]),
    sleep(0.1),
    animate([H | Path1], Path2).



% --- draw/1 ---
% Takes the map of The Netherlands. and calls draw/2 to start the drawing.

draw(Path) :-
    map(Map),
    strings_to_chars(Map, NewMap),
    draw(NewMap, Path, 0).

% --- draw/3 ---
% Call draw_row to draw a row of the map and repeat using recursing.

draw([], _, _).

draw([Row | Map], Path, Y) :-
    draw_row(Row, Path, 0, Y),
    NewY is Y + 1,
    draw(Map, Path, NewY).



% --- strings_to_chars/2 ---
% Convert all the string in a list to a list of characters.

strings_to_chars([], []).

strings_to_chars([H1 | T1], [H2 | T2]) :-
    string_chars(H1, H2),
    strings_to_chars(T1, T2).



% --- draw_row/4 ---
% Draws a row of map and puts the name of a city on the map if it is part of
% the route and a "#" for the rest of the route.

draw_row([], _, _, _) :- !,
    nl.

% Write the city name.
draw_row(Row, Path, X, Y) :-
    city(City, X/Y),
    member(X/Y, Path),
    !,
    write(City),
    string_length(City, L),
    skip_cells(Row, L, NewRow),
    NewX is X + L,
    draw_row(NewRow, Path, NewX, Y).

% Draw the path.
draw_row([_ | Row], Path, X, Y) :-
    member(X/Y, Path),
    !,
    write(#),
    NewX is X + 1,
    draw_row(Row, Path, NewX, Y).

% The the map.
draw_row([Cell | Row], Path, X, Y) :-
    write(Cell),
    NewX is X + 1,
    draw_row(Row, Path, NewX, Y).



% --- skip_cells/3 ---
% removes the first N elements from a list or returns an empty list if N is
% bigger than the length of the list.

skip_cells(Row, 0, Row) :- !.

skip_cells([], _, []).

skip_cells([_ | Row], N, NewRow) :-
    NewN is N - 1,
    skip_cells(Row, NewN, NewRow).



% --- path/2 ---
% Converts a route into a path, which contains the coordinates of the path on
% the map. It uses line to calculate the coordinates of a line between to
% cities in the route.

path([_], []) :- !.

path([City1, City2 | Route], NewPath) :-
    city(City1, X1/Y1),
    city(City2, X2/Y2),
    line(X1/Y1, X2/Y2, Line),
    path([City2 | Route], Path),
    append(Line, Path, NewPath).



% --- line/3 ---
% Calculate the coordinates of a line between the coordinates (X1, Y1) and
% (X2, Y2). This algorithm work from left to right where the correlation
% coefficient is between 0.5 and -0.5. If the is not the case of the line the
% Direction is changed or the X and Y are swapped and after the calculations
% this is reversed. Calls line/5 to do the calculations.

line(X1/Y1, X2/Y2, Line) :-
    abs(Y1 - Y2) > abs(X1 - X2),
    !,
    line(Y1/X1, Y2/X2, ReverseLine),
    swap_coordinates(ReverseLine, Line).

line(X1/Y1, X2/Y2, Line) :-
    X1 > X2,
    !,
    line(X2/Y2, X1/Y1, ReverseLine),
    reverse(ReverseLine, Line).

line(X1/Y1, X2/Y2, Line) :-
    D is (Y2 - Y1) / (X2 - X1),
    line(X1, Y1, X2, D, Line).

% --- line/5 ---
% Calculate the coordinates of a line between X and Xend, with starting value Y
% and correlation coefficient D.

line(X, Y, X, _, [X/Yround]) :- !,
    Yround is round(Y).

line(X, Y, Xend, D, [X/Yround | Line]) :-
    X < Xend,
    Yround is round(Y),
    NewX is X + 1,
    NewY is Y + D,
    line(NewX, NewY, Xend, D, Line).



% --- swap_coordinates/2 ---
% Swappes the X and Y values of the coordinates in the list.

swap_coordinates([], []) :- !.

swap_coordinates([Y/X | List], [X/Y | NewList]) :-
    swap_coordinates(List, NewList).



%++++++++++++++++++++++++++++++++++++++++++++++++++++
% Self-check passed!
