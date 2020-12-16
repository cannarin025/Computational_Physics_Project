import numpy as np


def H_Natural(surf_temp, amb_temp):
    if surf_temp - amb_temp >= 0:
        return np.abs(1.31 * ((float(surf_temp) - amb_temp) ** (1 / 3)))
    else:
        return -1 * np.abs(1.31 * ((float(surf_temp) - amb_temp) ** (1 / 3)))


def H_Forced(wind_speed):
    return 11.4 + 5.7 * wind_speed


def Neumann_Boundaries(initial_state, hx, hy, amb_temp, wind_speed, k, natural=True):
    # setting boundary conditions

    initial_x_dim = np.shape(initial_state)[1]
    initial_y_dim = np.shape(initial_state)[0]

    for i in range(initial_y_dim):
        for j in range(initial_x_dim):
            if natural:
                # if i == 0:  # bottom boundary
                #     surf_temp = initial_state[i + 1, j]
                #     H = H_Natural(surf_temp, amb_temp)
                #     initial_state[i, j] = surf_temp - 2 * hx * H_Natural(surf_temp, amb_temp) * (surf_temp - amb_temp)
                # if i == initial_y_dim - 1:  # top boundary
                #     surf_temp = initial_state[i - 1, j]
                #     initial_state[i, j] = surf_temp - 2 * hx * H_Natural(surf_temp, amb_temp) * (surf_temp - amb_temp)
                # if j == 0:  # left boundary
                #     surf_temp = initial_state[i, j + 1]
                #     initial_state[i, j] = surf_temp - 2 * hx * H_Natural(surf_temp, amb_temp) * (surf_temp - amb_temp)
                # if j == initial_x_dim - 1:  # right boundary
                #     surf_temp = initial_state[i, j - 1]
                #     initial_state[i, j] = surf_temp - 2 * hx * H_Natural(surf_temp, amb_temp) * (surf_temp - amb_temp)

                if i == 0:  # bottom boundary
                    surf_temp = initial_state[i + 1, j]
                    H = H_Natural(surf_temp, amb_temp)
                    initial_state[i, j] = surf_temp - ((2 * hx * H_Natural(surf_temp, amb_temp) * (amb_temp - surf_temp)) / -k)
                if i == initial_y_dim - 1:  # top boundary
                    surf_temp = initial_state[i - 1, j]
                    initial_state[i, j] = surf_temp - ((2 * hx * H_Natural(surf_temp, amb_temp) * (amb_temp - surf_temp)) / -k)
                if j == 0:  # left boundary
                    surf_temp = initial_state[i, j + 1]
                    initial_state[i, j] = surf_temp - ((2 * hy * H_Natural(surf_temp, amb_temp) * (amb_temp - surf_temp)) / -k)
                if j == initial_x_dim - 1:  # right boundary
                    surf_temp = initial_state[i, j - 1]
                    initial_state[i, j] = surf_temp - ((2 * hy * H_Natural(surf_temp, amb_temp) * (amb_temp - surf_temp)) / -k)

                # if i == 0:  # bottom boundary
                #     surf_temp = initial_state[i + 1, j]
                #     H = H_Natural(surf_temp, amb_temp)
                #     initial_state[i, j] = surf_temp - ((2 * hx * H_Natural(surf_temp, amb_temp) * (surf_temp - amb_temp)) / -k)
                # if i == initial_y_dim - 1:  # top boundary
                #     surf_temp = initial_state[i - 1, j]
                #     initial_state[i, j] = surf_temp - ((2 * hx * H_Natural(surf_temp, amb_temp) * (surf_temp - amb_temp)) / -k)
                # if j == 0:  # left boundary
                #     surf_temp = initial_state[i, j + 1]
                #     initial_state[i, j] = surf_temp - ((2 * hy * H_Natural(surf_temp, amb_temp) * (surf_temp - amb_temp)) / -k)
                # if j == initial_x_dim - 1:  # right boundary
                #     surf_temp = initial_state[i, j - 1]
                #     initial_state[i, j] = surf_temp - ((2 * hy * H_Natural(surf_temp, amb_temp) * (surf_temp - amb_temp)) / -k)

            elif not natural:
                if i == 0:  # bottom boundary
                    surf_temp = initial_state[i + 1, j]
                    initial_state[i, j] = surf_temp - 2 * hx * H_Forced(wind_speed) * (surf_temp - amb_temp)
                if i == initial_y_dim - 1:  # top boundary
                    surf_temp = initial_state[i - 1, j]
                    initial_state[i, j] = surf_temp - 2 * hx * H_Forced(wind_speed) * (surf_temp - amb_temp)
                if j == 0:  # left boundary
                    surf_temp = initial_state[i, j + 1]
                    initial_state[i, j] = surf_temp - 2 * hx * H_Forced(wind_speed) * (surf_temp - amb_temp)
                if j == initial_x_dim - 1:  # right boundary
                    surf_temp = initial_state[i, j - 1]
                    initial_state[i, j] = surf_temp - 2 * hx * H_Forced(wind_speed) * (surf_temp - amb_temp)

    return initial_state

def Jacobi_Solve(x_range, y_range, x_points = 10, y_points = 10, initial_guess = 0, natural = True):
    #definitions
    hx = x_range / x_points
    hy = y_range / y_points

    initial_x_dim = x_points + 2
    initial_y_dim = y_points + 2
    initial_state = np.full((initial_y_dim, initial_x_dim), initial_guess)

    #initial boundary conditions
    amb_temp = 20
    wind_speed = 30

    for iteration in range(10000):
        final_state = np.zeros((initial_y_dim, initial_x_dim))
        initial_state = Neumann_Boundaries(initial_state, hx, hy, amb_temp, wind_speed, 150000,natural)

        #solving iteration of Jacobi method
        for i in range(1, initial_y_dim - 1): #y
            for j in range(1, initial_x_dim - 1): #x
                # s = #this formula is incomplete without the S. What is S?
                updated_value = (((1/(hx**2)) * initial_state[i+1, j]) + ((1/(hx**2)) * initial_state[i-1, j]) + ((1/(hy**2)) * initial_state[i, j-1]) + ((1/(hy**2)) * initial_state[i, j+1])) / ((2/(hx**2)) + (2/(hy**2)))
                final_state[i,j] = updated_value

        initial_state = final_state


    #tidies up array
    final_state = np.delete(final_state, 0, 0)
    final_state = np.delete(final_state, 0, 1)
    final_state = np.delete(final_state, initial_y_dim - 2, 0)
    final_state = np.delete(final_state, initial_x_dim - 2, 1)

    print()
    print(final_state)
            

Jacobi_Solve(0.014,0.002, x_points= 10, y_points=10, initial_guess=8600)



#Poisson_Solve(5, 5)

a = np.matrix([[0.1,0.2,0.3,0.4],[0.5,0.6,0.7,0.8],[0.9,0.111,0.11,0.12],[0.13,0.14,0.15,0.16]])
b = np.matrix([[5,-2,3],[-3,9,1],[2,-1,-7]])
c = np.matrix([[-1],[2],[3]])
