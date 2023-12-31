import matplotlib.pyplot as plt

class CubicSplineSegment:
    def __init__(self, x, x_val, y_val, M_val):
        self.x = x
        self.x_val = x_val
        self.y_val = y_val
        self.M_val = M_val

    def eval(self):
        i = 1
        while self.x > self.x_val[i]:
            i += 1

        h_i = self.x_val[i] - self.x_val[i - 1]

        res_1 = (1 / 6) * self.M_val[i - 1] * ((self.x_val[i] - self.x) ** 3)
        res_2 = (1 / 6) * self.M_val[i] * ((self.x - self.x_val[i - 1]) ** 3)
        res_3 = (self.y_val[i - 1] - (1 / 6) * self.M_val[i - 1] * (h_i ** 2)) * (self.x_val[i] - self.x)
        res_4 = (self.y_val[i] - (1 / 6) * self.M_val[i] * (h_i ** 2)) * (self.x - self.x_val[i - 1])
        result = (h_i ** (-1)) * (res_1 + res_2 + res_3 + res_4)
        return result

class DifferenceQuotient:
    @staticmethod
    def calculate(xs, ys):
        n = len(xs)
        if n == 1:
            return ys[0]
        return (DifferenceQuotient.calculate(xs[1:], ys[1:]) - 
                DifferenceQuotient.calculate(xs[:n - 1], ys[:n - 1])) / (xs[n - 1] - xs[0])

class CubicSplineInterpolator:
    def __init__(self, x_val, y_val):
        self.x_val = x_val
        self.y_val = y_val
        self.M_val = self.calculate_M_values(x_val, y_val)

    def calculate_M_values(self, x_val, y_val):
        def h(k):
            return x_val[k] - x_val[k - 1]

        def lambda_k(k):
            return h(k) / (h(k) + h(k + 1))

        p, q, u = [0], [0], [0]

        for k in range(1, len(x_val) - 1):
            p.append((lambda_k(k) * q[k - 1]) + 2)
            q.append((lambda_k(k) - 1) / p[k])
            u.append(
                (6 * DifferenceQuotient.calculate([x_val[k - 1], x_val[k], x_val[k + 1]],
                                                  [y_val[k - 1], y_val[k], y_val[k + 1]]) -
                                                  lambda_k(k) * u[k - 1]) / p[k])

        M_values = [0]
        for k in range(len(x_val) - 2, 0, -1):
            M_values.append(u[k] + q[k] * M_values[len(x_val) - 2 - k])
        M_values.append(0)
        M_values.reverse()
        return M_values

    def interpolate(self, x):
        segment = CubicSplineSegment(x, self.x_val, self.y_val, self.M_val)
        return segment.eval()

plt.figure(figsize=(1140/80, 180/80), dpi=80)

with open("./dane/dane.txt") as data:
    num_segments = len(data.readlines()) // 4  
    data.seek(0)

    for i in range(num_segments):
        x_val = eval(data.readline())
        xs_val = eval(data.readline())
        ys_val = eval(data.readline())
        u_val = eval(data.readline())

        inter_xs = CubicSplineInterpolator(x_val, xs_val)
        inter_ys = CubicSplineInterpolator(x_val, ys_val)
        
        plt.plot([inter_xs.interpolate(u) for u in u_val], 
                 [inter_ys.interpolate(u) for u in u_val], 
                 linewidth=2.1,
                 color="red")

plt.show()
