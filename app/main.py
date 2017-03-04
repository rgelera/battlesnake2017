import bottle
import os
import random


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')

@bottle.get('/')
def index():
    head_url = '%s://%s/static/head.jpeg' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    return {
        'color': '#746876',
        'head': head_url
    }


@bottle.post('//start')
def start():
    data = bottle.request.json
    game_id = data['game_id']
    board_width = data['width']
    board_height = data['height']

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # TODO: Do things with data

    return {
        'color': '#00FF00',
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': head_url,
        'name': 'battlesnake-python'
    }


@bottle.post('//move')
def move():
    data = bottle.request.json
    up = {'move': 'up', 'taunt': 'battlesnake-python'}
    down = {'move': 'down', 'taunt': 'battlesnake-python'}
    right = {'move': 'right', 'taunt': 'battlesnake-python'}
    left = {'move': 'left', 'taunt': 'battlesnake-python'}

    possible, me = check_around(data)

    # Choose direction out of possible directions
    choice = random.choice(possible)

    # Translate choice to directional command
    choice = [choice[0] - me[0], choice[1] - me[1]]
    d = {'up':[0,-1], 'down':[0,1], 'left':[-1,0], 'right':[1,0]}

    if choice == [0,-1]:
        return up
    elif choice == [0,1]:
        return down
    elif choice == [-1,0]:
        return left
    elif choice == [1,0]:
        return right

def find_food():
    pass

def check_around(data):
    filled_blocks = []

    snakes = data['snakes']
    for s in snakes:
        if s['id'] == data['you']:
            me = s
        filled_blocks.extend(s['coords'])
    me_head = me['coords'][0]
    x = me_head[0]
    y = me_head[1]

    board_width = data['width']
    board_height = data['height']

    # walls
    walls = []
    if x == 0:
        walls.append([-1, y])
    if x == board_width-1:
        walls.append([board_width, y])
    if y == 0:
        walls.append([x, -1])
    if y == board_height-1:
        walls.append([x, board_height])
    filled_blocks.extend(walls)

    possible = [[x, y-1],[x+1, y],[x, y+1],[x-1, y]]
    remove_common_elements(possible, filled_blocks)
    return possible, me_head

# Removes common elements between a and b from a
def remove_common_elements(a, b):
    for e in a[:]:
        if e in b:
            a.remove(e)


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
