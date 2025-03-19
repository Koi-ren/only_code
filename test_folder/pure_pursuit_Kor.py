import numpy as np
import math
import matplotlib.pyplot as plt

# 파라미터 설정
k = 0.1  # 순수 추적 제어기의 전방 감도
Lfc = 2.0  # [m] 전방 거리
Kp = 1.0  # 속도 비례 제어 이득
dt = 0.1  # [s] 시뮬레이션 시간 간격
WB = 2.9  # [m] 차량의 축간 거리

show_animation = True  # 시뮬레이션 중 애니메이션을 표시할지 여부

class State:

    """
    차량의 상태를 나타내는 클래스입니다.
    """

    def __init__(self, x=0.0, y=0.0, yaw=0.0, v=0.0):
        self.x = x  # 차량의 X 좌표
        self.y = y  # 차량의 Y 좌표
        self.yaw = yaw  # 차량의 요각
        self.v = v  # 차량의 속도
        self.rear_x = self.x - ((WB / 2) * math.cos(self.yaw))  # 후축의 X 좌표
        self.rear_y = self.y - ((WB / 2) * math.sin(self.yaw))  # 후축의 Y 좌표

    def update(self, a, delta):
        """
        가속도와 조향각에 따라 차량의 상태를 업데이트합니다.
        """
        self.x += self.v * math.cos(self.yaw) * dt
        self.y += self.v * math.sin(self.yaw) * dt
        self.yaw += self.v / WB * math.tan(delta) * dt
        self.v += a * dt
        self.rear_x = self.x - ((WB / 2) * math.cos(self.yaw))
        self.rear_y = self.y - ((WB / 2) * math.sin(self.yaw))

    def calc_distance(self, point_x, point_y):
        """
        후축에서 주어진 점까지의 거리를 계산합니다.
        """
        dx = self.rear_x - point_x
        dy = self.rear_y - point_y
        return math.hypot(dx, dy)
    
class States:
    """
    차량의 상태 이력을 저장하는 클래스입니다.
    """

    def __init__(self):
        self.x = []  # X 좌표 리스트
        self.y = []  # Y 좌표 리스트
        self.yaw = []  # 요각 리스트
        self.v = []  # 속도 리스트
        self.t = []  # 시간 리스트

    def append(self, t, state):
        """
        현재 상태와 시간을 이력에 추가합니다.
        """
        self.x.append(state.x)
        self.y.append(state.y)
        self.yaw.append(state.yaw)
        self.v.append(state.v)
        self.t.append(t)

def proportional_control(target, current):
    """
    비례 제어를 사용하여 제어 입력(가속도)을 계산합니다.
    """
    a = Kp * (target - current)
    return a

class TargetCourse:
    """
    목표 경로를 나타내는 클래스입니다.
    """

    def __init__(self, cx, cy):
        self.cx = cx  # 경로의 X 좌표
        self.cy = cy  # 경로의 Y 좌표
        self.old_nearest_point_index = None  # 가장 가까운 점의 인덱스

    def search_target_index(self, state):
        """
        현재 상태를 기반으로 경로에서 목표 인덱스를 검색합니다.
        """
        if self.old_nearest_point_index is None:
            # 경로에서 가장 가까운 점의 인덱스를 찾습니다.
            dx = [state.rear_x - icx for icx in self.cx]
            dy = [state.rear_y - icy for icy in self.cy]
            d = np.hypot(dx, dy)
            ind = np.argmin(d)
            self.old_nearest_point_index = ind
        else:
            ind = self.old_nearest_point_index
            distance_this_index = state.calc_distance(self.cx[ind], self.cy[ind])
            while True:
                distance_next_index = state.calc_distance(self.cx[ind + 1], self.cy[ind + 1])
                if distance_this_index < distance_next_index:
                    break
                ind = ind + 1 if (ind + 1) < len(self.cx) else ind
                distance_this_index = distance_next_index
            self.old_nearest_point_index = ind

        Lf = k * state.v + Lfc  # 차량 속도에 기반한 전방 거리 업데이트

        # 전방 거리가 목표 점까지의 거리보다 클 때까지 목표 점 인덱스를 찾습니다.
        while Lf > state.calc_distance(self.cx[ind], self.cy[ind]):
            if (ind + 1) >= len(self.cx):
                break  # 목표를 초과하지 않도록 함
            ind += 1

        return ind, Lf

def pure_pursuit_steer_control(state, trajectory, pind):
    """
    순수 추적 제어를 사용하여 조향각을 계산합니다.
    """
    ind, Lf = trajectory.search_target_index(state)

    if pind >= ind:
        ind = pind

    if ind < len(trajectory.cx):
        tx = trajectory.cx[ind]
        ty = trajectory.cy[ind]
    else:  # 목표 방향으로
        tx = trajectory.cx[-1]
        ty = trajectory.cy[-1]
        ind = len(trajectory.cx) - 1

    alpha = math.atan2(ty - state.rear_y, tx - state.rear_x) - state.yaw
    delta = math.atan2(2.0 * WB * math.sin(alpha) / Lf, 1.0)

    return delta, ind

def plot_arrow(x, y, yaw, length=1.0, width=0.5, fc="r", ec="k"):
    """
    차량의 방향을 나타내는 화살표를 그립니다.
    """
    if not isinstance(x, float):
        for ix, iy, iyaw in zip(x, y, yaw):
            plot_arrow(ix, iy, iyaw)
    else:
        plt.arrow(x, y, length * math.cos(yaw), length * math.sin(yaw),
                  fc=fc, ec=ec, head_width=width, head_length=width)
        plt.plot(x, y)

def main():
    """
    순수 추적 경로 추적 시뮬레이션을 실행하는 메인 함수입니다.
    """
    # 목표 경로를 사인 파형으로 정의합니다.
    cx = np.arange(0, 70, 0.5)
    cy = [math.sin(ix / 5.0) * ix / 2.0 for ix in cx]

    target_speed = 10.0 / 3.6  # [m/s] 목표 속도

    T = 100.0  # 최대 시뮬레이션 시간 [s]

    # 차량의 초기 상태 설정
    state = State(x=0.0, y=-0.0, yaw=0.0, v=4.0)

    lastIndex = len(cx) - 1
    time = 0.0
    states = States()
    states.append(time, state)
    target_course = TargetCourse(cx, cy)
    target_ind, _ = target_course.search_target_index(state)

    while T >= time and lastIndex > target_ind:
        # 제어 입력 계산
        ai = proportional_control(target_speed, state.v)
        di, target_ind = pure_pursuit_steer_control(state, target_course, target_ind)

        state.update(ai, di)  # 제어 입력에 따라 차량 상태 업데이트

        time += dt
        states.append(time, state)

        if show_animation:  # 시뮬레이션 애니메이션 표시
            plt.cla()
            plt.gcf().canvas.mpl_connect('key_release_event', lambda event: [exit(0) if event.key == 'escape' else None])
            plot_arrow(state.x, state.y, state.yaw)
            plt.plot(cx, cy, "-r", label="경로")
            plt.plot(states.x, states.y, "-b", label="경로 추적")
            plt.plot(cx[target_ind], cy[target_ind], "xg", label="목표")
            plt.axis("equal")
            plt.grid(True)
            plt.title("속도[km/h]:" + str(state.v * 3.6)[:4])
            plt.pause(0.001)

    # 테스트
    assert lastIndex >= target_ind, "목표에 도달하지 못함"

    if show_animation:  # 최종 결과 표시
        plt.cla()
        plt.plot(cx, cy, ".r", label="경로")
        plt.plot(states.x, states.y, "-b", label="경로 추적")
        plt.legend()
        plt.xlabel("x[m]")
        plt.ylabel("y[m]")
        plt.axis("equal")
        plt.grid(True)

        plt.subplots(1)
        plt.plot(states.t, [iv * 3.6 for iv in states.v], "-r")
        plt.xlabel("시간[s]")
        plt.ylabel("속도[km/h]")
        plt.grid(True)
        plt.show()


if __name__ == '__main__':
    print("순수 추적 경로 추적 시뮬레이션 시작")
    main()
