"""
Window creation
Texture loading, positioning and scaling
"""

from threading import Thread

import pyglet
from pyglet.gl import (
    glClearColor, glClear, glEnable, glBlendFunc,
    GL_BLEND, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_COLOR_BUFFER_BIT
)
import math
import random

from board import Board
from board_config import TILE_ADJACENCY, BUILDING_COSTS, Building
from texture_enums import Resource
from button import Button


class Renderer():
    """
    Object used to load and draw the game on screen
    """
    # TODO(eli) replace this crude scale factors with rectangles that define areas in the layout
    # these will have a bottom-left corner, and width and height
    # scale will be computed based on the bounds of these boxes

    # ratio of tile width to screen width
    TILE_SCALE = 0.075
    # ratio of card width to screen width
    CARD_SCALE = 0.06
    # ratio of dice width to screen width
    DICE_SCALE = 0.05

    def __init__(self, window, board=None):
        self.window = window

        # test_player.resources = [Resource.ore, Resource.sheep, Resource.wheat,
        #                          Resource.brick, Resource.wood]

        if board is None:
            self.board = Board()

        self.load_images()
        self.tiles_batch = pyglet.graphics.Batch()
        self.gen_num_batch = pyglet.graphics.Batch()
        self.load_tiles_batch()
        self.load_card_sprites()
        self.load_bank_sprites()
        self.load_player_info(self.window.width*.85, self.window.height*.40)

        self.buttons = []
        self.vertex_buttons = {index:None for index in range(54)}
        self.init_buttons()

        self.dice_sprites = []
        self.load_dice_sprites()

        self.road_sprites = []


    def update(self):
        """Function to update the screen"""
        # clear screen
        glClearColor(0.7, 0.8, 1.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        # enable blending
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # draw tiles
        self.tiles_batch.draw()
        # draw gen nums
        self.gen_num_batch.draw()
        # draw the cards in player 0's hand
        self.draw_player_cards(0)
        # draw the bank
        self.draw_bank_cards()

        self.draw_player_info()
        self.draw_buttons()
        self.draw_dice()
        self.draw_roads()




    def draw_player_cards(self, player_id):
        """Draw resource, development, and victory point cards in a player's hand""" 
        resources = self.board.players[player_id].resources
        # integer quantity of each of the five resources in the resource list
        resource_counts = [0 for _ in range(5)]
        for resource in resources:
            resource_counts[resource.value] += 1

        for i in range(5):
            if resource_counts[i] > 0:
                # TODO maybe add x scaling to fill from left, rather than have fixed places
                self.card_sprites[i].draw()
                # TODO draw number over card representing resource_counts[i]
                x = self.card_sprites[i].x
                y = self.card_sprites[i].y
                width = self.card_sprites[i].width
                height = self.card_sprites[i].height
                label = pyglet.text.Label(str(resource_counts[i]),
                          font_name='Times New Roman',
                          font_size=40,
        #                  weight=5,
                          x=x+(width*.75), y=y+(height*.85),
                          anchor_x='center', anchor_y='center')
                label.draw()


        # TODO draw development cards


    def draw_bank_cards(self) -> list[pyglet.text.Label]:
        """Draw resource and development cards still in the bank"""
        resource_bank = self.board.resource_bank
        # integer quantity of each of the five resources in the resource list
        resource_counts = [0 for _ in range(5)]
        for resource in resource_bank.keys():
            resource_counts[resource.value] = len(resource_bank[resource])

        for i in range(5):
            label = pyglet.text.Label()
            # TODO maybe add x scaling to fill from left, rather than have fixed places
            self.bank_sprites[i].draw()
            # TODO draw number over card representing resource_counts[i]
            x = self.bank_sprites[i].x
            y = self.bank_sprites[i].y
            width = self.bank_sprites[i].width
            height = self.bank_sprites[i].height
            label = pyglet.text.Label(str(resource_counts[i]),
                        font_name='Times New Roman',
                        font_size=25,
    #                  weight=5,
                        x=x+(width*.75), y=y+(height*.85),
                        anchor_x='center', anchor_y='center')
            label.draw()


    def draw_player_info(self):
        """Draw each sprite in the player_info_sprites"""
        for sprite in self.player_info_sprites:
            for p_num, player in enumerate(self.board.players):
                self.player_info_sprites[(p_num * 14) + 1].text = str(player.vps)
                self.player_info_sprites[(p_num * 14) + 4].text = str(len(player.resources))
                self.player_info_sprites[(p_num * 14) + 7].text = str(len(player.dev_cards))
                self.player_info_sprites[(p_num * 14) + 10].text = str("-1")
                self.player_info_sprites[(p_num * 14) + 13].text = str(self.board.calculate_player_longest_road(player))
            sprite.draw()

    def draw_buttons(self):
        """draw each button on the screen"""
        for button in self.buttons:
            button.draw()
        for button in self.get_vertex_buttons():
            if self.vertex_buttons[button] is not None:
                self.vertex_buttons[button].draw()

    def draw_dice(self):
        """draw the current value of the dice roll on screen"""
        roll = self.board.die_roll
        index_1 = (roll[0]-1)*2
        index_2 = (roll[1]-1)*2 + 1
        self.dice_sprites[index_1].draw()
        self.dice_sprites[index_2].draw()

    def draw_roads(self):
        """render the roads on the screen.
           Also adds new road sprites if new roads have been placed"""
        roads = self.board.roads
        if len(roads) != len(self.road_sprites):
            # if there is a new road to create...
            new_roads = roads[len(self.road_sprites):]
            for road in new_roads:
                # for each road create and position a line between its two vertices
                v1 = self.vertex_buttons[road.vertex1]
                v2 = self.vertex_buttons[road.vertex2]
                v1_x = v1.center[0]
                v1_y = v1.center[1]
                v2_x = v2.center[0]
                v2_y = v2.center[1]
                owner = road.owner
                self.road_sprites.append(pyglet.shapes.Line(v1_x, v1_y, v2_x, v2_y, thickness=10.0, color=owner.color.value))

        # render all roads in road_sprites
        for road in self.road_sprites:
            road.draw()
                



    def load_images(self):
        """Multithreaded image loading for all textures used in rendering"""
        self.image_names = [
            "assets/mountains1.png",
            "assets/mountains2.png",
            "assets/mountains3.png",
            "assets/fields1.png",
            "assets/fields2.png",
            "assets/fields3.png",
            "assets/fields4.png",
            "assets/pasture1.png",
            "assets/pasture2.png",
            "assets/pasture3.png",
            "assets/pasture4.png",
            "assets/hills1.png",
            "assets/hills2.png",
            "assets/hills3.png",
            "assets/forest1.png",
            "assets/forest2.png",
            "assets/forest3.png",
            "assets/forest4.png",
            "assets/desert.png",
            "assets/gennum2.png",
            "assets/gennum3.png",
            "assets/gennum4.png",
            "assets/gennum5.png",
            "assets/gennum6.png",
            "assets/gennum8.png",
            "assets/gennum9.png",
            "assets/gennum10.png",
            "assets/gennum11.png",
            "assets/gennum12.png",
            "assets/ore.png", # 29
            "assets/wheat.png", # 30
            "assets/sheep.png",
            "assets/brick.png",
            "assets/wood.png",
            "assets/knight.png",
            "assets/roadbuilding.png",
            "assets/yearofplenty.png",
            "assets/monopoly.png",
            "assets/library.png",
            "assets/market.png",
            "assets/chapel.png", # 40
            "assets/university.png",
            "assets/palace.png",
            "assets/palace.png", # longest_road place holder
            "assets/palace.png", # largest army place holder
            "assets/palace.png", # place holder for resource card back
            "assets/palace.png", # Dev card back place holder
            "assets/dice1.png", # 47
            "assets/dice2.png",
            "assets/dice3.png",
            "assets/dice4.png",
            "assets/dice5.png",
            "assets/dice6.png"
        ]
        image_count = len(self.image_names)
        self.images = [None for _ in range(image_count)]
        threads = [None for _ in range(image_count)]
        for i in range(image_count):
            threads[i] = Thread(target=self.load_image, args=(i,))
            threads[i].start()

        for thread in threads:
            thread.join()


    def load_image(self, image_index):
        """This is a helper function only to be used by load_images"""
        self.images[image_index] = pyglet.image.load(self.image_names[image_index])

    def load_card_sprites(self):
        """Create and scale sprites corresponding to sprite images for each card image"""
        card_imgs = self.images[29:45]

        # assume all card images are the same size
        image_width = card_imgs[0].width
        #image_height = resource_imgs[0].height

        # hexagon tile dimensions
        card_width = self.CARD_SCALE * self.window.width
        #card_height = (image_height / image_width) * card_width

        # factor to scale tile images by
        scale = card_width / image_width

        self.card_sprites = []

        # TODO the spacing and position needs work to actually look good
        # what is here is mainly just something to get the imgs up on screen

        # just a little spacing to make things look more normal
        padding = card_width / 30

        for i, image in enumerate(card_imgs):
            x = padding + card_width * i
            y = padding
            sprite = pyglet.sprite.Sprite(image, x=x, y=y)
            sprite.scale = scale
            self.card_sprites.append(sprite)

    def load_bank_sprites(self):
        """Create and scale sprites corresponding to sprite images for each card image"""
        resource_imgs = self.images[29:34]

        # assume all card images are the same size
        image_width = resource_imgs[0].width
        #image_height = resource_imgs[0].height

        # These will be about half as small as the regular resource cards
        card_width = self.CARD_SCALE * self.window.width / 2
        #card_height = (image_height / image_width) * card_width

        # factor to scale tile images by
        scale = card_width / image_width

        self.bank_sprites = []

        # TODO the spacing and position needs work to actually look good
        # what is here is mainly just something to get the imgs up on screen

        # just a little spacing to make things look more normal
        padding = card_width / 30

        # from 5 --> 1
        for i in range(5):
            x = self.window.width - (padding + card_width * (5-i))
            y = padding + self.window.height / 2
            sprite = pyglet.sprite.Sprite(resource_imgs[i], x=x, y=y)
            sprite.scale = scale
            self.bank_sprites.append(sprite)


    def load_dice_sprites(self):
        """Load dice images"""
        dice_imgs = self.images[47:53]

        image_width = dice_imgs[0].width

        dice_width = self.DICE_SCALE * self.window.width / 2

        scale = dice_width / image_width

        width = self.buttons[1].width
        x_1 = self.buttons[1].top_left[0]
        y_1 = self.buttons[1].bottom_right[1]

        # TODO - make this dynamically sized
        x_2 = self.buttons[1].top_left[0] + (width / 2)
        y_2 = self.buttons[1].bottom_right[1]


        self.dice_sprites = []
        for i in range(6):
            sprite = pyglet.sprite.Sprite(dice_imgs[i], x=x_1, y=y_1)
            sprite.scale = scale
            self.dice_sprites.append(sprite)

            # same sprite but positioned to the right.
            sprite_2 = pyglet.sprite.Sprite(dice_imgs[i], x=x_2, y=y_2)
            sprite_2.scale = scale
            self.dice_sprites.append(sprite_2)


    def load_player_info(self, x, y):
        """Load/position images used to display every player's data on the side of the screen.
           x, y are the top-left coordinates where the data should be displayed on screen."""
        imgs = self.images[34]
        card_width = (self.CARD_SCALE * self.window.width / 2) / 2 # looks more natural
        image_width = imgs.width
        scale = card_width / image_width
        padding = card_width / 30

        y_offset = (self.window.height * self.CARD_SCALE * 1.5) + padding

        self.player_info_sprites = []

        for p_num, player in enumerate(self.board.players):
            # display player color, VPs, #cards, #dev cards, #knights played, longest road
            y_pos = y - ((p_num)*y_offset)
            player_sprite = pyglet.shapes.Rectangle(x, y_pos + card_width, card_width, card_width, color=player.color.value)
            self.player_info_sprites.append(player_sprite)

            # display vp total inside the player's color box
            vp_label = pyglet.text.Label(str(player.vps),
                    font_name='Times New Roman',
                    font_size=25,
                    x=player_sprite.x + (player_sprite.width / 2), y=player_sprite.y + (player_sprite.height / 2),
                    anchor_x='center', anchor_y='center')
            self.player_info_sprites.append(vp_label)

            # position the graphic that shows the card icon
            x_pos = x + card_width + padding*3 # add extra padding
            # TODO - Jeb: use a different image
            card_sprite = pyglet.sprite.Sprite(imgs, x=x_pos, y=y_pos)
            card_sprite.scale = scale*2
            self.player_info_sprites.append(card_sprite)
            label_background, label = self.label_from_sprite(card_sprite, str(len(player.resources)))

            self.player_info_sprites.append(label_background)
            self.player_info_sprites.append(label)

            # position the graphic that shows the dev card count
            x_pos = x + (card_width*3) + padding*6
            # TODO - Jeb: use a different image
            dev_card_sprite = pyglet.sprite.Sprite(imgs, x=x_pos, y=y_pos)
            dev_card_sprite.scale = scale*2
            self.player_info_sprites.append(dev_card_sprite)

            label_background, label = self.label_from_sprite(dev_card_sprite, str(len(player.dev_cards)))

            self.player_info_sprites.append(label_background)
            self.player_info_sprites.append(label)

            # position the graphic that shows the knight count
            x_pos = x + (card_width*5) + padding*9

            # TODO - Jeb: use a different image
            knight_sprite = pyglet.sprite.Sprite(imgs, x=x_pos, y=y_pos)
            knight_sprite.scale = scale*2
            self.player_info_sprites.append(knight_sprite)

            # TODO: get the number of knight cards from each player
            label_background, label = self.label_from_sprite(knight_sprite, str(len(player.dev_cards)))

            self.player_info_sprites.append(label_background)
            self.player_info_sprites.append(label)

            # position the graphic that shows the longest road count
            x_pos = x + (card_width*7) + padding*12

            # TODO - Jeb: use a different image
            road_sprite = pyglet.sprite.Sprite(imgs, x=x_pos, y=y_pos)
            road_sprite.scale = scale*2
            self.player_info_sprites.append(road_sprite)

            # TODO: get the longest road for each player
            label_background, label = self.label_from_sprite(road_sprite, str(len(player.dev_cards)))

            self.player_info_sprites.append(label_background)
            self.player_info_sprites.append(label)

    def label_from_sprite(self, sprite, text):
        """returns a background box and label in the upper right corner of the given sprite"""
        width = sprite.width
        height = sprite.height
        x_pos = sprite.x
        y_pos = sprite.y
        label = pyglet.text.Label(text,
                font_name='Times New Roman',
                font_size=25,
                color=(255,255,255),
                x=x_pos+(width*.75), y=y_pos+(height*.85),
                anchor_x='center', anchor_y='center')
        l_x = x_pos+(width*.5)
        l_y = y_pos+(height*.7)
        l_w = width * .5
        l_h = height * .3
        label_background = pyglet.shapes.Rectangle(l_x, l_y, l_w, l_h, color=(0, 0, 0))

        return label_background, label

    def init_buttons(self):
        """Initialize buttons. placeholder for now."""
        self.buttons.append(Button(False, (self.window.width/2 + 60, 100), width=50, height=50, button_name="run_ai_turn"))
        self.buttons.append(Button(False, (self.window.width/20 * 19, self.window.height/20 * 19), width=200, height=100, button_name="roll_dice"))
        self.buttons.append(Button(False, (self.window.width/2, self.window.height/8), width=50, height=50, button_name="build_settlement"))
        self.buttons.append(Button(False, (self.window.width/2 + 60, self.window.height/8), width=50, height=50, button_name="build_city"))
        self.buttons.append(Button(False, (self.window.width / 2, 100), width=50, height=50, button_name="end_turn"))
        self.buttons.append(Button(False, (self.window.width/2 + 120, self.window.height/8), width=50, height=50, button_name="build_road"))

        # initialize vertex buttons:
        for index, tile_sprite in enumerate(self.tile_sprites):
            tile_width = tile_sprite.width * 1.05 # positions the vertices in a more suitable manner
            tile_height = tile_sprite.height

            x_center = tile_sprite.x + (tile_width/2)
            y_center = tile_sprite.y + (tile_height/2)

            for i in range(6):
                x_pos = x_center + (tile_width/2) * math.cos((i * math.pi / 3) - math.pi/2)
                y_pos = y_center + (tile_height/2) * math.sin((i * math.pi / 3) - math.pi/2)

                vertex_index = TILE_ADJACENCY[index][i]
                if self.vertex_buttons[vertex_index] is None:
                    sprite = pyglet.shapes.Circle(x_pos,y_pos, 20, color=(0,0,int(255/(i+1))))
                    self.vertex_buttons[vertex_index] = Button(True, (x_pos, y_pos), radius=20, button_name="vertex", button_sprite=sprite)


    def load_tiles_batch(self):
        """Create, position, and scale sprites for tiles and gen nums"""
        mountains_imgs = self.images[0:3]
        fields_imgs = self.images[3:7]
        pasture_imgs = self.images[7:11]
        hills_imgs = self.images[11:14]
        forest_imgs = self.images[14:18]
        desert_img = self.images[18]
        gen_num_imgs = self.images[19:29]

        mountains_index = 0
        fields_index = 0
        pasture_index = 0
        hills_index = 0
        forest_index = 0

        # assume all tile images are the same size
        tile_image_width = desert_img.width
        tile_image_height = desert_img.height

        # hexagon tile dimensions
        tile_width = self.TILE_SCALE * self.window.width
        tile_height = (tile_image_height / tile_image_width) * tile_width

        # factor to scale tile images by
        tile_scale = tile_width / tile_image_width

        gen_num_image_width = gen_num_imgs[0].width

        # gen nums are sized relative to the tiles that contain them
        gen_num_width = tile_width / 3
        gen_num_height = tile_height / 3

        # scale factor to adjust image by
        gen_num_scale = gen_num_width / gen_num_image_width

        # used to position gen num relevent to corresponding tile
        gen_num_x_offset = (tile_width - gen_num_width) / 2
        gen_num_y_offset = (tile_height - gen_num_height) / 2

        # store tile and gen num sprites
        self.tile_sprites = []
        self.gen_num_sprites = []

        # coordinates of where to position central tile
        center_x = self.window.width / 2 - tile_width / 2
        center_y = self.window.height / 2 - tile_height / 2

        for tile in self.board.tiles:
            match tile.resource:
                case Resource.ore:
                    tile_image = mountains_imgs[mountains_index % len(mountains_imgs)]
                    mountains_index += 1
                case Resource.wheat:
                    tile_image = fields_imgs[fields_index % len(fields_imgs)]
                    fields_index += 1
                case Resource.sheep:
                    tile_image = pasture_imgs[pasture_index % len(pasture_imgs)]
                    pasture_index += 1
                case Resource.brick:
                    tile_image = hills_imgs[hills_index % len(hills_imgs)]
                    hills_index += 1
                case Resource.wood:
                    tile_image = forest_imgs[forest_index % len(forest_imgs)]
                    forest_index += 1
                case _: # none
                    tile_image = desert_img

            # axial coordinates specify a signed integer x, y offset from a (0, 0) center
            axial_x, axial_y = tile.coords

            # Tiles above the midline need to be shifted right, likewise below shifted left.
            # the axial_y / 2 term accounts for this shift. The reason for dividing by two is that
            # the hexagon grid is staggered row to row for tesselation.
            x = center_x + tile_width * (axial_x + axial_y / 2)

            # If you picture the largest rectangle you could draw within a hexagon,
            # the height of that rectangle is 1/2 the height of the whole shape
            # the pointed section above this rectangle fits into the above row of hexagons.
            # the height of this upper section is 1/4 of the shape's height, meaning
            # the row coordinate must be scaled by 3/4
            y = center_y + tile_height * (axial_y * 0.75)

            tile_sprite = pyglet.sprite.Sprite(tile_image, batch=self.tiles_batch, x=x, y=y)
            tile_sprite.scale = tile_scale
            self.tile_sprites.append(tile_sprite)

            x += gen_num_x_offset
            y += gen_num_y_offset
            gen_num_image = None
            if tile.gen_num >= 2 and tile.gen_num <= 6:
                gen_num_image = gen_num_imgs[tile.gen_num - 2]
            elif tile.gen_num >= 8 and tile.gen_num <= 12:
                gen_num_image = gen_num_imgs[tile.gen_num - 3]
            if gen_num_image:
                gen_num_sprite = pyglet.sprite.Sprite(gen_num_image,
                    batch=self.gen_num_batch, x=x, y=y)
                gen_num_sprite.scale = gen_num_scale
                self.gen_num_sprites.append(gen_num_sprite)

    def get_clickables(self):
        """return list of clickable elements on the board"""
        clickables = self.buttons
        # TODO get all buttons from the renderer
        return clickables
    
    def get_vertex_buttons(self):
        """returns the dictionary containing the vertex buttons that are active in the current game state"""
        # Vertex buttons are only shown after the build buttons are pressed:
        state = self.board.game_state
        valid_buttons = {}
        if state.tags['settlement']:
            # show valid places to place a settlement
            for vertex_index in self.vertex_buttons:
                if vertex_index is not None:
                    if self.board.is_valid_settle_spot(state.get_current_player(), vertex_index):
                        # only add valid settle spots
                        valid_buttons[vertex_index] = self.vertex_buttons[vertex_index]
        elif state.tags['city']:
            # show valid places to place a city
            for vertex_index in self.vertex_buttons:
                if vertex_index is not None:
                    if self.board.is_valid_city_spot(state.get_current_player(), vertex_index):
                        # only add valid city spots
                        valid_buttons[vertex_index] = self.vertex_buttons[vertex_index]
        elif state.tags['road']:
            if state.tags['road_v1'] is None:
                # show valid places to start a road
                for vertex_index in self.vertex_buttons:
                    if vertex_index is not None:
                        for vertex_neighbor_index in self.vertex_buttons:
                            if self.board.is_valid_road_spot(state.get_current_player(), vertex_index, vertex_neighbor_index):
                                # only add valid road starts
                                valid_buttons[vertex_index] = self.vertex_buttons[vertex_index]
            else:
                # show valid places to end a road
                for vertex_index in self.vertex_buttons:
                    if vertex_index is not None:
                        if self.board.is_valid_road_spot(state.get_current_player(), state.tags['road_v1'], vertex_index):
                            # only add valid road ends
                            valid_buttons[vertex_index] = self.vertex_buttons[vertex_index]
        return valid_buttons

    def ai_start_turn(self, player):
        """The current player takes a turn (during the start phase) automatically"""
        state = self.board.game_state
        # Look for settle spot
        state.tags['settlement'] = True
        cost = BUILDING_COSTS[Building.settlement]
        self.board.add_resources(state.get_current_player(), cost)
        valid_spots = list(self.get_vertex_buttons().keys())

        # Choose random index and build settlement there
        random.shuffle(valid_spots)
        self.board.place_building(Building.settlement, player, valid_spots[0])
        state.tags['settlement_pos'] = valid_spots[0]
        state.tags['settlement'] = False

        # Look for road spot
        state.tags['road'] = True
        cost = BUILDING_COSTS[Building.road]
        self.board.add_resources(player, cost)
        valid_spots = list(self.get_vertex_buttons().keys())

        # Choose a random index and place first road vertex there
        random.shuffle(valid_spots)
        v1 = valid_spots[0]
        state.tags['road_v1'] = v1

        # Choose the second vertex
        valid_spots = list(self.get_vertex_buttons().keys())
        random.shuffle(valid_spots)
        v2 = valid_spots[0]
        self.board.place_road(player, v1, v2)
        state.tags['road_v1'] = None
        state.tags['road'] = False

        # Call end turn start phase from gamestate
        previous_player = state.get_current_player()
        second_settle = state.end_turn_start_phase()
        if second_settle:
            # give resources to previous player
            resources = self.board.get_resources_from_vertex(state.tags['settlement_pos'])
            self.board.add_resources(previous_player, resources)

    def ai_turn(self, player):
        """The current player takes a turn automatically"""
        state = self.board.game_state
        # Call start turn
        state.roll_dice()
        self.board.start_turn(player)

        # move the game_state
        state.start_building_phase()

        # Look for legal settle spots
        state.tags['settlement'] = True
        cost = BUILDING_COSTS[Building.settlement]
        valid_spots = list(self.get_vertex_buttons().keys())

        # Choose random index and build settlement there
        random.shuffle(valid_spots)
        if len(valid_spots) > 0:
            self.board.place_building(Building.settlement, player, valid_spots[0])
        state.tags['settlement'] = False

        # Look for legal road spots
        state.tags['road'] = True
        cost = BUILDING_COSTS[Building.road]

        valid_spots = list(self.get_vertex_buttons().keys())

        # Choose a random index and place first road vertex there
        random.shuffle(valid_spots)
        if len(valid_spots) > 0:
            v1 = valid_spots[0]
            state.tags['road_v1'] = v1

            # Choose the second vertex
            valid_spots = list(self.get_vertex_buttons().keys())
            random.shuffle(valid_spots)
            v2 = valid_spots[0]
            self.board.place_road(player, v1, v2)
            state.tags['road_v1'] = None

        state.tags['road'] = False

        # End turn
        state.end_turn()
