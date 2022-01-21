import math

class Angle:
    def calculate_angles(a1, b1, c1, a2, b2, c2):
        """Calculates the angle between two planes:\n
        \ta1 * x + b1 * y + c1 * z + d1 = 0 \n
        and \n
        \ta2 * x + b2*y + c2 * z + d2 = 0"""
        temp = (a1 * a2 + b1 * b2 + c1 * c2)
        e1 = math.sqrt(a1 * a1 + b1 * b1 + c1 * c1)
        e2 = math.sqrt(a2 * a2 + b2 * b2 + c2 * c2)
        temp = temp / (e1 * e2)
        angle = math.degrees(math.acos(temp))

        # print(f'The angle is {angle} degrees')
        # print("")
        return angle