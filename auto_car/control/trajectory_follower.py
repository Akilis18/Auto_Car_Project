# trajectory_follower.py
'''
Input: vehicle_state (from localizer), trajectory (from decision_maker)
Output: steering_angle (float, rad)
'''

import math
import numpy as np

class PurePursuit:
    def __init__(self, wheelbase: float, lookahead_m: float, ploty, leftx, rightx, lefty, righty, center_offset, YM_PER_PIX, XM_PER_PIX):
        self.ploty = ploty
        self.leftx = leftx
        self.rightx = rightx
        self.lefty = lefty
        self.righty = righty
        self.center_offset = center_offset
        self.YM_PER_PIX = YM_PER_PIX
        self.XM_PER_PIX = XM_PER_PIX

        self.wheelbase = wheelbase
        self.lookahead_m = lookahead_m
        self.max_steer_deg = 30.0
        self.deg_deadband = 1.0
        self.offset_gain = 0.05
    
    def compute_turn_command(self):
        """
        根據偵測到的車道線，計算轉向建議。

        回傳: (direction, steer_deg, signed_radius_m)
        - direction: 'left' | 'right' | 'straight'
        - steer_deg: 推薦方向盤角度（度，左正右負，已限幅）
        - signed_radius_m: 有號曲率半徑（m），左彎為正，右彎為負；直線回傳 inf
        """
        if (
            self.ploty is None
            or self.leftx is None
            or self.rightx is None
            or self.lefty is None
            or self.righty is None
        ):
            return None

        left_fit_cr = np.polyfit(self.lefty * self.YM_PER_PIX, self.leftx * self.XM_PER_PIX, 2)
        right_fit_cr = np.polyfit(self.righty * self.YM_PER_PIX, self.rightx * self.XM_PER_PIX, 2)

        a_c = 0.5 * (left_fit_cr[0] + right_fit_cr[0])
        b_c = 0.5 * (left_fit_cr[1] + right_fit_cr[1])

        y_eval_m = float(np.max(self.ploty)) * self.YM_PER_PIX
        denom = (1.0 + (2.0 * a_c * y_eval_m + b_c) ** 2) ** 1.5
        if denom < 1e-6:
            return None
        kappa = 2.0 * a_c / denom

        steer_rad = math.atan(self.wheelbase * kappa)
        offset_m = (self.center_offset or 0.0) / 100.0
        steer_rad += math.atan2(self.offset_gain * offset_m, max(self.lookahead_m, 1e-3))

        steer_deg = float(np.degrees(steer_rad))
        steer_deg = float(np.clip(steer_deg, -self.max_steer_deg, self.max_steer_deg))

        direction = (
            "left" if steer_deg > self.deg_deadband else "right" if steer_deg < -self.deg_deadband else "straight"
        )
        signed_radius_m = float("inf") if abs(kappa) < 1e-6 else 1.0 / kappa

        return direction, steer_deg, signed_radius_m