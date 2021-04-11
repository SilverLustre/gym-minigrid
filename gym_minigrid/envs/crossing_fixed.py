from gym_minigrid.minigrid import *
from gym_minigrid.register import register

import itertools as itt


class CrossingFixedEnv(MiniGridEnv):
    """
    Environment with wall or lava obstacles, sparse reward.
    """

    def __init__(self, size=9, num_crossings=1, obstacle_type=Lava, seed=None, wall_verticle=True, x=4, y=4,
                 random_door=False, random_all=False):
        self.num_crossings = num_crossings
        self.obstacle_type = obstacle_type
        self.wall_verticle = wall_verticle
        self.x = x
        self.y = y
        self.random_door = random_door
        self.random_all = random_all
        # if self.random_all:
        #     self.random_door = True
        #     self.wall_verticle = self.np_random.choice([True, False])
        #     self.x = self.np_random.choice([3, 5])
        #     self.y = self.np_random.choice([3, 5])
        super().__init__(
            grid_size=size,
            max_steps=4 * size * size, # default: max_steps=4 * size * size
            # Set this to True for maximum speed
            see_through_walls=False,
            seed=None
        )

    def _gen_grid(self, width, height):
        assert width % 2 == 1 and height % 2 == 1  # odd size

        if self.random_all:
            self.random_door = True
            self.wall_verticle = self.np_random.choice([True, False])
            self.x = self.np_random.choice([3, 5])
            self.y = self.np_random.choice([3, 5])

        # Create an empty grid
        self.grid = Grid(width, height)

        # Generate the surrounding walls
        self.grid.wall_rect(0, 0, width, height)

        # Place the agent in the top-left corner
        self.agent_pos = (1, 1)
        self.agent_dir = 0

        # Place a goal square in the bottom-right corner
        self.put_obj(Goal(), width - 2, height - 2)

        # Place obstacles (lava or walls)
        v, h = object(), object()  # singleton `vertical` and `horizontal` objects

        # Lava rivers or walls specified by direction and position in grid
        # rivers = [(v, i) for i in range(2, height - 2, 2)]
        # rivers += [(h, j) for j in range(2, width - 2, 2)]
        rivers = []
        if self.wall_verticle:
            # rivers = [(v,4)]
            rivers.append((v, self.x))
        else:
            rivers.append((h, self.y))

        # self.np_random.shuffle(rivers)
        rivers = rivers[:self.num_crossings]  # sample random rivers
        rivers_v = sorted([pos for direction, pos in rivers if direction is v])
        rivers_h = sorted([pos for direction, pos in rivers if direction is h])
        obstacle_pos = itt.chain(
            itt.product(range(1, width - 1), rivers_h),
            itt.product(rivers_v, range(1, height - 1)),
        )
        for i, j in obstacle_pos:
            self.put_obj(self.obstacle_type(), i, j)

        # To set a block as empty(path)
        # self.grid.set(i,j,None)
        # To put a block as designated obstacle
        # self.put_obj(self.obstacle_type(), i, j)

        if self.random_door:
            door_pos = self.np_random.choice(range(1, self.width - 1))
            if self.wall_verticle:
                self.grid.set(self.x, door_pos, None)
            else:
                self.grid.set(door_pos, self.y, None)
        else:
            self.grid.set(self.x, self.y, None)
        self.mission = (
            "avoid the lava and get to the green goal square"
            if self.obstacle_type == Lava
            else "find the opening and get to the green goal square"
        )


class SimpleCrossingS9N1P44VEnv(CrossingFixedEnv):
    def __init__(self):
        super().__init__(size=9, num_crossings=1, obstacle_type=Wall)


class SimpleCrossingS9N1P3VREnv(CrossingFixedEnv):
    def __init__(self):
        super().__init__(size=9, num_crossings=1, obstacle_type=Wall, wall_verticle=True, x=3, random_door=True)


class SimpleCrossingS9N1P5VREnv(CrossingFixedEnv):
    def __init__(self):
        super().__init__(size=9, num_crossings=1, obstacle_type=Wall, wall_verticle=True, x=5, random_door=True)


class SimpleCrossingS9N1P3HREnv(CrossingFixedEnv):
    def __init__(self):
        super().__init__(size=9, num_crossings=1, obstacle_type=Wall, wall_verticle=False, y=3, random_door=True)


class SimpleCrossingS9N1P5HREnv(CrossingFixedEnv):
    def __init__(self):
        super().__init__(size=9, num_crossings=1, obstacle_type=Wall, wall_verticle=False, y=5, random_door=True)


class SimpleCrossingS9N1P3V3H5V5HREnv(CrossingFixedEnv):
    def __init__(self):
        super().__init__(size=9, num_crossings=1, obstacle_type=Wall, wall_verticle=False, y=5, random_door=True, random_all=True)


register(
    id='MiniGrid-SimpleCrossingS9N1P44V-v0',
    entry_point='gym_minigrid.envs:SimpleCrossingS9N1P44VEnv'
)

register(
    id='MiniGrid-SimpleCrossingS9N1P3VREnv-v0',
    entry_point='gym_minigrid.envs:SimpleCrossingS9N1P3VREnv'
)

register(
    id='MiniGrid-SimpleCrossingS9N1P5VREnv-v0',
    entry_point='gym_minigrid.envs:SimpleCrossingS9N1P5VREnv'
)

register(
    id='MiniGrid-SimpleCrossingS9N1P3HREnv-v0',
    entry_point='gym_minigrid.envs:SimpleCrossingS9N1P3HREnv'
)

register(
    id='MiniGrid-SimpleCrossingS9N1P5HREnv-v0',
    entry_point='gym_minigrid.envs:SimpleCrossingS9N1P5HREnv'
)

register(
    id='MiniGrid-SimpleCrossingS9N1P3V3H5V5HREnv-v0',
    entry_point='gym_minigrid.envs:SimpleCrossingS9N1P3V3H5V5HREnv'
)
