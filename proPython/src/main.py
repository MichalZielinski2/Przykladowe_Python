import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from src.driver import Robot


def set_distance_types(plot=False):
    distance = np.arange(0, 10, 0.1)
    far = fuzz.trapmf(distance, [4.5, 5.5, 10, float('inf')])
    medium = fuzz.trapmf(distance, [2.5, 3.5, 4.5, 5.5])
    close = fuzz.trapmf(distance, [0.8, 1.1, 2.5, 3.5])
    v_close = fuzz.trapmf(distance, [float('-inf'), 0, 1, 1.5])

    if (plot):
        plt.plot(distance, far)
        plt.plot(distance, medium)
        plt.plot(distance, close)
        plt.plot(distance, v_close)
        plt.show()

    return distance, far, medium, close, v_close


def set_speed_types(plot=False):
    speed = np.arange(0, 5, 0.1)
    fast = fuzz.trapmf(speed, [2.5, 3, 5, float('inf')])
    medium_fast = fuzz.trimf(speed, [0.5, 2.5, 3])
    slow = fuzz.trimf(speed, [0, 1, 2.5])
    stop = fuzz.trimf(speed, [0, 0, 0])

    if (plot):
        plt.plot(speed, medium_fast)
        plt.plot(speed, fast)
        plt.plot(speed, slow)
        plt.plot(speed, stop)
        print(stop)
        plt.show()

    return speed, fast, medium_fast, slow, stop


def calculate_target_speed(distance_to_go):
    distance, far, medium, close, v_close = set_distance_types()

    speed, fast, medium_fast, slow, stop = set_speed_types()

    # jeżeli daleko to szybko
    distance_level_far = fuzz.interp_membership(distance, far, distance_to_go)
    speed_activation_fast = np.fmin(distance_level_far, fast)

    # jeżeli średnio daleko to średnio szybko
    distance_level_medium = fuzz.interp_membership(distance, medium, distance_to_go)
    speed_activation_medium = np.fmin(distance_level_medium, medium_fast)

    # jeżeli blisko to wolno
    distance_level_close = fuzz.interp_membership(distance, close, distance_to_go)
    speed_activation_slow = np.fmin(distance_level_close, slow)

    # jeżeli bardzo blisko to stop
    distance_level_v_close = fuzz.interp_membership(distance, v_close, distance_to_go)
    speed_activation_stop = np.fmin(distance_level_v_close, stop)

    # agregacja
    aggregated = np.fmax(speed_activation_fast, np.fmax(speed_activation_medium, np.fmax(speed_activation_stop,
                                                                                         speed_activation_slow)))

    # obliczenie zdyskretyzowanego wyniku
    return fuzz.defuzz(speed, aggregated, 'mom')


if __name__ == "__main__":

    robot = Robot(pos_x=0, pos_x_wall=6)
    # do wyrysowania zborów
    # distance, far, medium, close, v_close = set_distance_types(plot=False)
    # speed, fast, medium_fast, slow, stop = set_speed_types(plot=False)


    speed_arr = np.empty([0])
    dist_arr = np.empty([0])


    speedn = 1

    while speedn != 0 and robot.get_distance()<8 :
        dist = robot.get_distance()
        t_speed = calculate_target_speed(dist)
        robot.set_target_speed(t_speed)

        robot.next_step()
        speedn = robot.speed
        speed_arr = np.append(speed_arr, speedn)
        dist_arr = np.append(dist_arr, dist)

    plt.plot(dist_arr, speed_arr)
    plt.show()


    # do wyświetlenia odległości oraz prędkości w zalerzności od czasu
    # time = np.arange(0, len(speed_arr)/10, 0.1)
    #
    # plt.plot(time, speed_arr)
    # plt.plot(time, dist_arr)
    # plt.show()
