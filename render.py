"""
Window creation
Texture loading, positioning and scaling
"""

from threading import Thread

import math
import random
import pyglet
from pyglet.gl import (
    glClearColor, glClear, glEnable, glBlendFunc,
    GL_BLEND, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_COLOR_BUFFER_BIT
)


from board import Board
from board_config import TILE_ADJACENCY, BUILDING_COSTS, Building
from texture_enums import Resource, Card
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
    DICE_SCALE = 0.025

    def __init__(self, window, board=None):
        self.window = window

        # test_player.resources = [Resource.ore, Resource.sheep, Resource.wheat,
        #                          Resource.brick, Resource.wood]

        if board is None:
            self.board = Board()
        else:
            self.board = board

        self.board.players[0].dev_cards = [Card.knight, Card.knight, Card.knight, Card.monopoly]

        self.load_images()
        self.tiles_batch = pyglet.graphics.Batch()
        self.gen_num_batch = pyglet.graphics.Batch()
        self.load_tiles_batch()
        self.load_card_sprites()
        self.load_bank_sprites()
        self.load_player_info(self.window.width*.85, self.window.height*.40)

        self.load_background()

        self.load_building_sprites()

        self.buttons = []
        self.load_buttons()

        self.dice_sprites = []
        self.load_dice_sprites()

        self.road_sprites = []
        self.building_sprites = {index:None for index in range(54)}


    def update(self):
        """Function to update the screen"""
        # clear screen
        glClearColor(0.55, 0.45, 0.33, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        # draw background
        self.background_sprite.draw()

        # enable blending
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # draw tiles
        self.tiles_batch.draw()
        # draw gen nums
        self.gen_num_batch.draw()
        # draw the cards in player 0's hand #TODO render the actual current player's stuff
        self.draw_player_cards(0)
        # draw the bank
        self.draw_bank_cards()

        self.draw_player_info()
        self.draw_buttons()
        self.draw_dice()
        self.draw_roads()
        self.draw_buildings()


    def draw_player_cards(self, player_id):
        """Draw resource, development, and victory point cards in a player's hand""" 
        player = self.board.players[player_id]
        # integer quantity of each of the five resources in the resource list
        card_counts = [0 for _ in range(14)]
        for resource in player.resources:
            card_counts[resource.value] += 1

        for card in player.dev_cards:
            card_counts[card.value] += 1

        for i in range(14):
            if card_counts[i] > 0:
                limit = min(card_counts[i], 5)
                offset = self.card_sprites[i].width / 28
                self.card_sprites[i].x += limit * offset
                self.card_sprites[i].y += limit * offset
                for _ in range(limit):    
                    self.card_sprites[i].x -= offset
                    self.card_sprites[i].y -= offset
                    self.card_sprites[i].draw()
                #self.card_sprites[i].draw()
                x = self.card_sprites[i].x
                y = self.card_sprites[i].y
                width = self.card_sprites[i].width
                height = self.card_sprites[i].height
                label = pyglet.text.Label(str(card_counts[i]),
                          font_name='Times New Roman',
                          font_size=40,
                          x=x+(width*.75), y=y+(height*.85),
                          anchor_x='center', anchor_y='center')
                label.draw()

    def draw_bank_cards(self) -> list[pyglet.text.Label]:
        """Draw resource and development cards still in the bank"""
        resource_bank = self.board.resource_bank
        # integer quantity of each of the five resources in the resource list
        resource_counts = [0 for _ in range(5)]
        for resource in resource_bank.keys():
            resource_counts[resource.value] = len(resource_bank[resource])

        for i in range(5):
            label = pyglet.text.Label()
            self.bank_sprites[i].draw()
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
                longest_road = str(self.board.calculate_player_longest_road(player))
                self.player_info_sprites[(p_num * 14) + 13].text = longest_road
            sprite.draw()

    def draw_buttons(self):
        """draw each button on the screen"""
        for button in self.buttons:
            button.draw()
        for button in self.board.get_clickable_vertices():
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
                self.road_sprites.append(
                    pyglet.shapes.Line(
                        v1_x,
                        v1_y,
                        v2_x,
                        v2_y,
                        thickness=10.0,
                        color=owner.color.value)
                )

        # render all roads in road_sprites
        for road in self.road_sprites:
            road.draw()

    def draw_buildings(self):
        """Draw cities and settlements on the board"""
        for vertex_index, vertex in enumerate(self.board.vertices):
            if self.building_sprites[vertex_index] is None:
                added = False
                vertex_button = self.vertex_buttons[vertex_index]
                x_pos = vertex_button.center[0] - (vertex_button.radius) # center the building
                y_pos = vertex_button.center[1]
                size = vertex_button.radius * 2
                sprite = pyglet.shapes.Rectangle(x_pos, y_pos, size, size, color=(0,0,0))
                if vertex.building is Building.SETTLEMENT:
                    color = vertex.owner.color.value
                    sprite = pyglet.shapes.Rectangle(x_pos, y_pos, size, size, color=color)
                    added = True
                elif vertex.building is Building.CITY:
                    color = vertex.owner.color.value
                    sprite = pyglet.shapes.Rectangle(x_pos, y_pos, size, size*1.5, color=color)
                    added = True
                # add the new building to the building_sprites dict
                if added:
                    self.building_sprites[vertex_index] = Button(
                        False,
                        vertex_button.center,
                        sprite)

        for vertex_index in self.building_sprites:
            if self.building_sprites[vertex_index] is not None:
                self.building_sprites[vertex_index].draw()

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
            "assets/resource_back.png", 
            "assets/development_back.png", 
            "assets/dice1.png", # 47
            "assets/dice2.png",
            "assets/dice3.png",
            "assets/dice4.png",
            "assets/dice5.png",
            "assets/dice6.png",
            "assets/woodgrain.png", # 53
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
        image_height = card_imgs[0].height

        # hexagon tile dimensions
        card_width = self.CARD_SCALE * self.window.width
        card_height = (image_height / image_width) * card_width

        # factor to scale tile images by
        scale = card_width / image_width

        self.card_sprites = []

        # just a little spacing to make things look more normal
        padding = card_width / 30
        x_offset = 0
        y_offset = 0
        for i, image in enumerate(card_imgs):
            if (i > 0 and i % 5 == 0):
                x_offset = 0
                y_offset += card_height + padding * 5

            x = padding + x_offset
            y = padding + y_offset
            x_offset += card_width
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

        roll_button = self.buttons[1]

        dice_width = min(roll_button.width / 2, roll_button.height) * 0.8

        scale = dice_width / image_width

        x_pad = (roll_button.width - (dice_width * 2)) / 3
        y_pad = (roll_button.height - dice_width) / 2

        x_1 = roll_button.top_left[0] + x_pad
        y_1 = roll_button.bottom_right[1] + y_pad

        x_2 = roll_button.top_left[0] + (roll_button.width + x_pad) / 2
        y_2 = roll_button.bottom_right[1] + y_pad

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
        knight_img = self.images[34]
        resource_card_back_img = self.images[45]
        dev_card_back_img = self.images[46]
        card_width = (self.CARD_SCALE * self.window.width / 2) / 2 # looks more natural
        image_width = knight_img.width
        scale = card_width / image_width
        padding = card_width / 30

        y_offset = (self.window.height * self.CARD_SCALE * 1.5) + padding

        self.player_info_sprites = []

        for p_num, player in enumerate(self.board.players):
            # display player color, VPs, #cards, #dev cards, #knights played, longest road
            y_pos = y - ((p_num)*y_offset)
            player_sprite = pyglet.shapes.Rectangle(
                x,
                y_pos + card_width,
                card_width,
                card_width,
                color=player.color.value)
            self.player_info_sprites.append(player_sprite)

            # display vp total inside the player's color box
            vp_label = pyglet.text.Label(str(player.vps),
                    font_name='Times New Roman',
                    font_size=25,
                    x=player_sprite.x + (player_sprite.width / 2),
                    y=player_sprite.y + (player_sprite.height / 2),
                    anchor_x='center', anchor_y='center')
            self.player_info_sprites.append(vp_label)

            # position the graphic that shows the card icon
            x_pos = x + card_width + padding*3 # add extra padding
            card_sprite = pyglet.sprite.Sprite(resource_card_back_img, x=x_pos, y=y_pos)
            card_sprite.scale = scale*2
            self.player_info_sprites.append(card_sprite)
            label_background, label = self.label_from_sprite(
                card_sprite,
                str(len(player.resources)))

            self.player_info_sprites.append(label_background)
            self.player_info_sprites.append(label)

            # position the graphic that shows the dev card count
            x_pos = x + (card_width*3) + padding*6
            dev_card_sprite = pyglet.sprite.Sprite(dev_card_back_img, x=x_pos, y=y_pos)
            dev_card_sprite.scale = scale*2
            self.player_info_sprites.append(dev_card_sprite)

            label_background, label = self.label_from_sprite(
                dev_card_sprite,
                str(len(player.dev_cards)))

            self.player_info_sprites.append(label_background)
            self.player_info_sprites.append(label)

            # position the graphic that shows the knight count
            x_pos = x + (card_width*5) + padding*9

            knight_sprite = pyglet.sprite.Sprite(knight_img, x=x_pos, y=y_pos)
            knight_sprite.scale = scale*2
            self.player_info_sprites.append(knight_sprite)

            label_background, label = self.label_from_sprite(
                knight_sprite,
                str(len(player.dev_cards)))

            self.player_info_sprites.append(label_background)
            self.player_info_sprites.append(label)

            # position the graphic that shows the longest road count
            x_pos = x + (card_width*7) + padding*12

            road_sprite = pyglet.sprite.Sprite(knight_img, x=x_pos, y=y_pos)
            road_sprite.scale = scale*2
            self.player_info_sprites.append(road_sprite)

            label_background, label = self.label_from_sprite(
                road_sprite,
                str(len(player.dev_cards)))

            self.player_info_sprites.append(label_background)
            self.player_info_sprites.append(label)

    def load_building_sprites(self):
        """Load building sprites"""
        self.building_sprites = []

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

    def load_buttons(self):
        """Load button objects"""
        width = self.window.width
        height = self.window.height * 0.1
        x = 0
        y = 0
        #end_turn_label = Label(
        end_turn_button = Button(
            False,
            center=(x, y),
            width=width,
            height=height,
            button_name="end_turn",
            button_label=pyglet.text.Label("End Turn"))

        self.buttons.append(end_turn_button)

        self.buttons.append(
            Button(False,
                   (self.window.width/2 + 60, 100),
                   width=50, height=50, button_name="run_ai_turn"))
        self.buttons.append(
            Button(False,
                   (self.window.width/20 * 19, self.window.height/20 * 19),
                   width=200, height=100, button_name="roll_dice"))
        self.buttons.append(
            Button(False,
                   (self.window.width/2, self.window.height/8),
                   width=50, height=50, button_name="build_settlement"))
        self.buttons.append(
            Button(False,
                   (self.window.width/2 + 60, self.window.height/8),
                   width=50, height=50, button_name="build_city"))
        self.buttons.append(
            Button(False,
                   (self.window.width / 2, 100),
                   width=50, height=50, button_name="end_turn"))
        self.buttons.append(
            Button(False,
                   (self.window.width/2 + 120, self.window.height/8),
                   width=50, height=50, button_name="build_road"))

        #width = self.window.width
        #height = window.height * 0.1
        #end_turn_button = Button(False, (x, y), width=width, height=height, button_name="end_turn")

        self.vertex_buttons = [None for _ in range(54)]

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
                    self.vertex_buttons[vertex_index] = Button(
                        True,
                        (x_pos, y_pos),
                        radius=20,
                        button_name="vertex",
                        button_sprite=sprite)


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


    def load_background(self):
        """Load the background image"""
        background_img = self.images[53]
        self.background_sprite = pyglet.sprite.Sprite(background_img, x=0, y=0)
        self.background_sprite.scale = self.window.height / background_img.height

    def get_clickables(self):
        """return list of clickable elements on the board"""
        clickables = self.buttons
        return clickables
