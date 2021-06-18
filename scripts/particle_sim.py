import logging
import numpy as np
from multi_uuv import leaderless_circle
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.collections import LineCollection

# TODO: https://matplotlib.org/gallery/animation/subplots.html

logging.basicConfig(format="[%(asctime)s] [%(levelname)s] %(message)s",
                    level=logging.INFO,
                    file="test.log")


class Particle(object):
    def __init__(self, uuv_id, n_uuvs, pos=None, yaw=0, omega_0=1.0, gain=1.0):
        self.uuv_id = uuv_id
        self.n_uuvs = n_uuvs

        if pos is not None:
            self.pos = pos
        else:
            self.pos = np.array([0.0, 0.0])

        self.vel = 1.0
        self.yaw = yaw
        self.yaw_rate = 0.0
        self.omega_0 = omega_0
        self.gain = gain

        self.poses = self.create_poses()

    def create_poses(self):
        poses = {}
        for i in range(self.n_uuvs):
            poses[i] = dict(position=np.array([0.0, 0.0]), yaw=0.0)
        return poses

    def update_poses(self, uuv_ids, positions, yaws):
        logging.info("ID[%s] is updating poses of vehicles %s", self.uuv_id,
                     len(uuv_ids))
        for i, uuv_id in enumerate(uuv_ids):
            if uuv_id not in self.poses:
                logging.info("ID[%s] adding new pose entry for ID[%s]",
                             self.uuv_id, uuv_id)
            self.poses[uuv_id] = dict(position=positions[i], yaw=yaws[i])
            logging.debug("ID[%s] adding pose entry: %s", self.uuv_id,
                          self.poses[uuv_id])

    def get_pose(self):
        return dict(position=self.pos, yaw=self.yaw)

    def move(self, dt):
        if self.uuv_id % 1 == 0:
            yaw_delta = self.yaw_rate * dt
        else:
            yaw_delta = self.yaw_rate * dt * 1.5
        logging.debug("ID[%s] changing yaw by %s", self.uuv_id, yaw_delta)
        self.yaw = self.yaw + yaw_delta
        dx = self.vel * dt * np.cos(self.yaw)
        dy = self.vel * dt * np.sin(self.yaw)
        pos_delta = np.array([dx, dy])
        logging.debug("ID[%s] moving delta: %s", self.uuv_id, pos_delta)
        self.pos = self.pos + pos_delta
        logging.debug("ID[%s] new position: %s", self.uuv_id, self.pos)

    def apply_control(self):
        r_vecs = [self.poses[i]["position"] for i in range(self.n_uuvs)]
        yaws = [self.poses[i]["yaw"] for i in range(self.n_uuvs)]

        yaw_rate = leaderless_circle.compute_control_output(
            vehicle_id=self.uuv_id,
            omega_0=self.omega_0,
            gain=self.gain,
            n_vehicles=self.n_uuvs,
            vel_abs=self.vel,
            r_vecs=r_vecs,
            yaws=yaws)
        logging.info("ID[%s] Changing yaw rate from %.2f to %.2f", self.uuv_id,
                     self.yaw_rate, yaw_rate)
        self.yaw_rate = yaw_rate


def main():
    n_particles = 4

    dt = 0.02
    t0 = 0
    te = 15
    t = np.linspace(t0, te, int((te - t0) / dt))

    particles = []
    positions = {}
    for i in range(n_particles):
        particles.append(
            Particle(i, n_particles, pos=np.array([i, 0.0]), yaw=i * 3.14))
        positions[i] = np.zeros((len(t), 2), dtype=np.float)
    for i in range(len(t)):
        poses = {}
        for j in range(n_particles):
            particles[j].move(dt)
            poses[j] = particles[j].get_pose()
            positions[j][i, :] = poses[j]["position"]
            particles[j].apply_control()

        new_positions = [poses[x]["position"] for x in range(n_particles)]
        new_yaws = [poses[x]["yaw"] for x in range(n_particles)]
        ids = range(n_particles)
        for j in range(n_particles):
            particles[j].update_poses(ids, new_positions, new_yaws)

    animator = Animator(positions, n_particles, 100)
    animator.ax.set_aspect('equal', adjustable='box')
    plt.grid(True)
    animator.auto_limits()
    fps = 30
    duration = (te - t0) * 0.5
    n_frames = int(fps * duration)
    frame_index_step = int(len(t) / n_frames)
    frame_index = range(0, len(t), frame_index_step)
    anim = animation.FuncAnimation(animator.fig,
                                   animator.update,
                                   init_func=animator.init_lines,
                                   blit=True,
                                   frames=frame_index,
                                   interval=int(1.0 / fps * 1000))
    # plt.plot(positions[0][:, 0], positions[0][:, 1], positions[1][:, 0],
    #          positions[1][:, 1], "--")
    plt.show()


class Animator(object):
    def __init__(self, positions, n_lines, keep_n):
        self.positions = positions
        self.n_lines = n_lines
        self.keep_n = keep_n
        fig, ax = plt.subplots()
        self.fig = fig
        self.ax = ax
        self.lines = []
        self.cmaps = [
            'Blues', 'Oranges', 'Greens', 'YlGn', 'Reds', 'YlOrBr', 'YlOrRd',
            'OrRd', 'PuRd', 'RdPu', 'BuPu', 'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn',
            'BuGn'
        ]

        self.create_lines()

    def create_lines(self):
        for i in range(self.n_lines):
            # self.lines.append(self.ax.plot([], [], "-")[0])
            norm = plt.Normalize(0, self.keep_n)
            self.lines.append(
                LineCollection(np.array([]), cmap=self.cmaps[i], norm=norm))
            self.ax.add_collection(self.lines[i])

    def init_lines(self):
        for line in self.lines:
            line.set_segments(np.array([]))
            # line.set_data([], [])
        return self.lines

    def update(self, index):
        for i in range(self.n_lines):
            if index == 0:
                break
            start = index - self.keep_n
            if start < 0:
                start = 0
            x = self.positions[i][start:index, 0]
            y = self.positions[i][start:index, 1]
            n_points = len(x)

            points = np.array([x, y]).T.reshape(-1, 1, 2)
            segments = np.concatenate([points[:-1], points[1:]], axis=1)
            color_array = np.arange(0, self.keep_n)
            color_array = color_array[-n_points:]
            self.lines[i].set_array(color_array)
            self.lines[i].set_segments(segments)
            # self.lines[i].set_data(x, y)
        return self.lines

    def auto_limits(self):
        max_x = -np.Inf
        min_x = np.Inf
        max_y = -np.Inf
        min_y = np.Inf
        for i in range(self.n_lines):
            line_max_x = np.max(self.positions[i][:, 0])
            line_min_x = np.min(self.positions[i][:, 0])
            max_x = line_max_x if line_max_x > max_x else max_x
            min_x = line_min_x if line_min_x < min_x else min_x

            line_max_y = np.max(self.positions[i][:, 1])
            line_min_y = np.min(self.positions[i][:, 1])
            max_y = line_max_y if line_max_y > max_y else max_y
            min_y = line_min_y if line_min_y < min_y else min_y
        margin_x = (max_x - min_x) * 0.1
        margin_y = (max_y - min_y) * 0.1
        xlim = [min_x - margin_x, max_x + margin_x]
        xspan = xlim[1] - xlim[0]
        ylim = [min_y - margin_y, max_y + margin_y]
        yspan = ylim[1] - ylim[0]
        xcenter = (xlim[0] + xlim[1]) / 2.0
        ycenter = (ylim[0] + ylim[1]) / 2.0
        logging.info("xlim: %s, ylim: %s", xlim, ylim)
        self.ax.set(xlim=xlim, ylim=ylim)


def create_animation(positions, fps, t, n_particles):
    tspan = t[-1] - t[0]
    frames = int(tspan * fps)
    interval = int(len(t) / frames)
    fig = plt.figure()
    ax = plt.axes(xlim=(-5, 5), ylim=(-5, 5))
    lines = []
    for i in range(n_particles):
        lines.append(ax.plot([], [], "--")[0])

    def update(index):
        for j in range(n_particles):
            lines[j].set_data(positions[j][:index, 0], positions[j][:index, 1])
        return lines

    ani = animation.FuncAnimation(fig,
                                  update,
                                  frames=frames,
                                  interval=interval,
                                  blit=True)

    return fig, ax


if __name__ == "__main__":
    main()
