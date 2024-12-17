import matplotlib
matplotlib.use('TkAgg')  # Ensure correct backend for animations
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

class PolygonCollision:
    def __init__(self, P, Q):
        self.P = P
        self.Q = Q

    @staticmethod
    def edges(vertices):
        """Generate edges of a polygon from its vertices."""
        return [(vertices[i], vertices[(i + 1) % len(vertices)]) for i in range(len(vertices))]

    @staticmethod
    def line_intersection(p1, p2, q1, q2):
        """Check for intersection between two line segments."""
        def ccw(a, b, c):
            return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])

        return ccw(p1, q1, q2) != ccw(p2, q1, q2) and ccw(p1, p2, q1) != ccw(p1, p2, q2)

    def detect_collision(self):
        """Detect the first collision point between polygons P and Q."""
        P_edges = self.edges(self.P)
        Q_edges = self.edges(self.Q)

        for dx in np.linspace(0, 100, 500):
            translated_P = [(x + dx, y) for x, y in self.P]
            translated_P_edges = self.edges(translated_P)

            for (p1, p2) in translated_P_edges:
                for (q1, q2) in Q_edges:
                    if self.line_intersection(p1, p2, q1, q2):
                        return dx, p1, p2, q1, q2  # Return translation and colliding edges

        return None

    def visualize(self):
        """Visualize the translation and collision detection."""
        fig, ax = plt.subplots()

        def plot_polygon(vertices, color, label):
            x, y = zip(*vertices + [vertices[0]])
            ax.plot(x, y, color=color, label=label)

        collision = self.detect_collision()

        def update(frame):
            ax.clear()
            plot_polygon(self.Q, 'blue', 'Polygon Q')
            translated_P = [(x + frame, y) for x, y in self.P]
            plot_polygon(translated_P, 'green', 'Polygon P')

            if collision and frame >= collision[0]:
                dx, p1, p2, q1, q2 = collision
                ax.scatter(*p1, color='red', zorder=5, label='Collision Point')
                ax.plot(*zip(*[p1, p2]), color='red', linestyle='--', label='Colliding Edge (P)')
                ax.plot(*zip(*[q1, q2]), color='orange', linestyle='--', label='Colliding Edge (Q)')

            ax.legend()
            ax.set_xlim(-10, 120)
            ax.set_ylim(-10, 50)
            ax.set_aspect('equal')
            ax.set_title("Polygon Collision Animation")
            ax.set_xlabel("X")
            ax.set_ylabel("Y")

        ani = animation.FuncAnimation(fig, update, frames=np.linspace(0, 100, 100), interval=50, repeat=False)

        try:
            ani.save("polygon_collision.gif", writer="pillow")
            print("Animation saved as 'polygon_collision.gif'.")
        except Exception as e:
            print(f"Could not save animation: {e}")
        plt.show()

# Example Usage
P = [(0, 0), (10, 0), (10, 10), (0, 10)]
Q = [(30, 5), (40, 0), (40, 10), (50, 60), (40, 65)]

collision_detector = PolygonCollision(P, Q)
collision_detector.visualize()
