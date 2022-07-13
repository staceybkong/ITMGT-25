'''Module 4: Individual Programming Assignment 1

Parsing Data

This assignment covers your ability to manipulate data in Python.
'''

def relationship_status(from_member, to_member, social_graph):
    '''Relationship Status.
    20 points.

    Let us pretend that you are building a new app.
    Your app supports social media functionality, which means that users can have
    relationships with other users.

    There are two guidelines for describing relationships on this social media app:
    1. Any user can follow any other user.
    2. If two users follow each other, they are considered friends.

    This function describes the relationship that two users have with each other.

    Please see "assignment-4-sample-data.py" for sample data. The social graph
    will adhere to the same pattern.

    Parameters
    ----------
    from_member: str
        the subject member
    to_member: str
        the object member
    social_graph: dict
        the relationship data    

    Returns
    -------
    str
        "follower" if fromMember follows toMember,
        "followed by" if fromMember is followed by toMember,
        "friends" if fromMember and toMember follow each other,
        "no relationship" if neither fromMember nor toMember follow each other.
    '''
    # Replace `pass` with your code. 
    # Stay within the function. Only use the parameters as input. The function should return your answer.
    if to_member in social_graph[from_member]["following"]:
        if from_member in social_graph[to_member]["following"]:
            return "Friends"
        else:
            return "Follower"
    
    elif to_member not in social_graph:
        if to_member in social_graph[from_member]["following"]:
            return "Follower"
        else:
            return "No Relationship"
    
    else:
        if from_member in social_graph[to_member]["following"]:
            return "Followed"
        else:
            return "No Relationship"

def tic_tac_toe(board):
    '''Tic Tac Toe. 
    25 points.

    Tic Tac Toe is a common paper-and-pencil game. 
    Players must attempt to successfully draw a straight line of their symbol across a grid.
    The player that does this first is considered the winner.

    This function evaluates a tic tac toe board and returns the winner.

    Please see "assignment-4-sample-data.py" for sample data. The board will adhere
    to the same pattern. The board may by 3x3, 4x4, 5x5, or 6x6. The board will never
    have more than one winner. The board will only ever have 2 unique symbols at the same time.

    Parameters
    ----------
    board: list
        the representation of the tic-tac-toe board as a square list of lists

    Returns
    -------
    str
        the symbol of the winner or "NO WINNER" if there is no winner
    '''
    # Replace `pass` with your code. 
    # Stay within the function. Only use the parameters as input. The function should return your answer.
    dimension = len(board)
    horizontal = [x for x in board]
    vertical = [x for x in zip(*board)]
    up_down_diagonal = [board[a][a] for a,v in enumerate(board)]
    down_up_diagonal = [board[(dimension-1)-a][a] for a,v in enumerate(board)]
    
    for h in horizontal:
        if len(set(h)) == 1:
            return h[0]
        else:
            for v in vertical:
                if len(set(v)) == 1:
                    return v[0]
                else:
                    if len(set([board[i][i] for i in range(len(board))])) == 1:
                        return board[0][0]
                    else:
                        if len(set([board[i][dimension-i-1] for i in range(dimension)])) == 1:
                            return board[0][dimension-1]
    
    return "NO WINNER"

def eta(first_stop, second_stop, route_map):
    '''ETA. 
    25 points.

    A shuttle van service is tasked to travel along a predefined circlar route.
    This route is divided into several legs between stops.
    The route is one-way only, and it is fully connected to itself.

    This function returns how long it will take the shuttle to arrive at a stop
    after leaving another stop.

    Please see "mod-4-ipa-1-sample-data.py" for sample data. The route map will
    adhere to the same pattern. The route map may contain more legs and more stops,
    but it will always be one-way and fully enclosed.

    Parameters
    ----------
    first_stop: str
        the stop that the shuttle will leave
    second_stop: str
        the stop that the shuttle will arrive at
    route_map: dict
        the data describing the routes

    Returns
    -------
    int
        the time it will take the shuttle to travel from first_stop to second_stop
    '''
    # Replace `pass` with your code. 
    # Stay within the function. Only use the parameters as input. The function should return your answer.
    length = len(route_map)
    stops = list(route_map.keys())
    first = 0
    second = 0
    time = 0
    
    for r in range(length):
        if first_stop == stops[r][0]:
            first = r      
    for r in range(length):
        if second_stop == stops[r][1]:
            second = r
    if first <= second:
        for s in range(length):
            if s >= first and s <= second:
                if (first == second or first < second):
                    final = route_map[stops[s]]
                    time += final['travel_time_mins']     
    if first > second:
        for t in range(length):
            if t >= first or t <= second:
                final = route_map[stops[t]]
                time += final['travel_time_mins']
    
    return time