import numpy


def calc_center(r_vec, omega_0, yaw, v_abs):
    return r_vec + numpy.array([-numpy.sin(yaw),
                                numpy.cos(yaw)]) * v_abs / omega_0


def calc_all_centers(r_vecs, omega_0, yaws, v_abs):
    n_vecs = len(r_vecs)
    n_dims = len(r_vecs[0])
    c = numpy.zeros([n_vecs, n_dims], dtype=numpy.float)
    for i in range(n_vecs):
        c[i] = calc_center(r_vec=r_vecs[i],
                           omega_0=omega_0,
                           yaw=yaws[i],
                           v_abs=v_abs)
    return c


def calc_yaw_rate(omega_0, K, N, v_abs, c, yaw, k):
    P = numpy.eye(N) - numpy.ones([N, N], dtype=numpy.float) / N
    Pk = P[k]
    r_dot = numpy.array([numpy.cos(yaw) * v_abs,
                         numpy.sin(yaw) * v_abs]).reshape(2, 1)
    tmp = numpy.matmul(K * Pk, c)
    tmp = numpy.matmul(tmp, r_dot)
    return float(omega_0 * (1.0 + tmp))


def compute_control_output(vehicle_id, omega_0, gain, n_vehicles, vel_abs,
                           r_vecs, yaws):
    centers = calc_all_centers(r_vecs=r_vecs,
                               omega_0=omega_0,
                               yaws=yaws,
                               v_abs=vel_abs)
    yaw_rate = calc_yaw_rate(omega_0=omega_0,
                             K=gain,
                             N=n_vehicles,
                             v_abs=vel_abs,
                             c=centers,
                             yaw=yaws[vehicle_id],
                             k=vehicle_id)
    return yaw_rate


def calc_all_yaw_rates(omega_0, K, N, v_abs, c, yaws):
    pass
