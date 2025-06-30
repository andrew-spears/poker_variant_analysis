from game_utils.utils import *
from game_utils.ContinuousPokerVariants.ContinousPokerTemplate import ContinuousPokerTemplate
from scipy.optimize import root_scalar

# L, U LIMIT CONTINUOUS POKER

class LCP_utils:
    _cache = {}
    _last_game_params = None

    @staticmethod
    def clear_cache():
        LCP_utils._cache.clear()
        LCP_utils._last_game_params = None

    @staticmethod
    def check_and_clear_cache(game_params):
        if LCP_utils._last_game_params != game_params:
            LCP_utils.clear_cache()
            LCP_utils._last_game_params = game_params

    @staticmethod
    def compute_A0(game_params):
        L, U = game_params['L'], game_params['U']
        LCP_utils.check_and_clear_cache(game_params)
        if 'A0' not in LCP_utils._cache:
            LCP_utils._cache['A0'] = U**2 + 3 * U + 3
        return LCP_utils._cache['A0']

    @staticmethod
    def compute_A1(game_params):
        L, U = game_params['L'], game_params['U']
        LCP_utils.check_and_clear_cache(game_params)
        if 'A1' not in LCP_utils._cache:
            LCP_utils._cache['A1'] = 7 * U**3 + 21 * U**2 + 21 * U + 6
        return LCP_utils._cache['A1']

    @staticmethod
    def compute_A2(game_params):
        L, U = game_params['L'], game_params['U']
        LCP_utils.check_and_clear_cache(game_params)
        if 'A2' not in LCP_utils._cache:
            LCP_utils._cache['A2'] = 6 * U**3 + 18 * U**2 + 18 * U + 5
        return LCP_utils._cache['A2']

    @staticmethod
    def compute_A3(game_params):
        L, U = game_params['L'], game_params['U']
        LCP_utils.check_and_clear_cache(game_params)
        if 'A3' not in LCP_utils._cache:
            LCP_utils._cache['A3'] = 7 * U**3 + 21 * U**2 + 18 * U + 3
        return LCP_utils._cache['A3']

    @staticmethod
    def compute_A4(game_params):
        L, U = game_params['L'], game_params['U']
        LCP_utils.check_and_clear_cache(game_params)
        if 'A4' not in LCP_utils._cache:
            A1 = LCP_utils.compute_A1(game_params)
            A2 = LCP_utils.compute_A2(game_params)
            LCP_utils._cache['A4'] = 3 * A1 * L**2 + 3 * A1 * L + A1 + A2 * L**3
        return LCP_utils._cache['A4']

    @staticmethod
    def compute_A5(game_params):
        L, U = game_params['L'], game_params['U']
        LCP_utils.check_and_clear_cache(game_params)
        if 'A5' not in LCP_utils._cache:
            A0 = LCP_utils.compute_A0(game_params)
            LCP_utils._cache['A5'] = 3 * A0 * L**2 * U + 3 * A0 * L * U + A0 * U - L**3
        return LCP_utils._cache['A5']

    @staticmethod
    def compute_x0(game_params):
        L, U = game_params['L'], game_params['U']
        LCP_utils.check_and_clear_cache(game_params)
        if 'x0' not in LCP_utils._cache:
            A4 = LCP_utils.compute_A4(game_params)
            LCP_utils._cache['x0'] = (3 * (L + 1)**3 * U) / A4
        return LCP_utils._cache['x0']

    @staticmethod
    def compute_x1(game_params):
        L, U = game_params['L'], game_params['U']
        LCP_utils.check_and_clear_cache(game_params)
        if 'x1' not in LCP_utils._cache:
            A0 = LCP_utils.compute_A0(game_params)
            A4 = LCP_utils.compute_A4(game_params)
            LCP_utils._cache['x1'] = (3 * A0 * L * U + A0 * U - L**3 - 3 * L**2) / A4
        return LCP_utils._cache['x1']

    @staticmethod
    def compute_x2(game_params):
        L, U = game_params['L'], game_params['U']
        LCP_utils.check_and_clear_cache(game_params)
        if 'x2' not in LCP_utils._cache:
            A5 = LCP_utils.compute_A5(game_params)
            A4 = LCP_utils.compute_A4(game_params)
            LCP_utils._cache['x2'] = A5 / A4
        return LCP_utils._cache['x2']

    @staticmethod
    def compute_x3(game_params):
        L, U = game_params['L'], game_params['U']
        LCP_utils.check_and_clear_cache(game_params)
        if 'x3' not in LCP_utils._cache:
            A2 = LCP_utils.compute_A2(game_params)
            A4 = LCP_utils.compute_A4(game_params)
            LCP_utils._cache['x3'] = (A2 * L**3 + 3 * A2 * L**2 + 3 * L * (5 * U**3 + 15 * U**2 + 15 * U + 4) +
                                        4 * U**3 + 12 * U**2 + 12 * U + 3) / A4
        return LCP_utils._cache['x3']

    @staticmethod
    def compute_x4(game_params):
        L, U = game_params['L'], game_params['U']
        LCP_utils.check_and_clear_cache(game_params)
        if 'x4' not in LCP_utils._cache:
            A1 = LCP_utils.compute_A1(game_params)
            A2 = LCP_utils.compute_A2(game_params)
            A4 = LCP_utils.compute_A4(game_params)
            LCP_utils._cache['x4'] = (3 * A1 * L**2 + A2 * L**3 + 3 * A2 * L + 4 * U**3 + 12 * U**2 + 12 * U + 3) / A4
        return LCP_utils._cache['x4']

    @staticmethod
    def compute_x5(game_params):
        L, U = game_params['L'], game_params['U']
        LCP_utils.check_and_clear_cache(game_params)
        if 'x5' not in LCP_utils._cache:
            A3 = LCP_utils.compute_A3(game_params)
            A4 = LCP_utils.compute_A4(game_params)
            LCP_utils._cache['x5'] = (3 * A3 * L**2 + 3 * A3 * L + A3 + L**3 * (6 * U**3 + 18 * U**2 + 15 * U + 2)) / A4
        return LCP_utils._cache['x5']

    @staticmethod
    def compute_b0(game_params):
        L, U = game_params['L'], game_params['U']
        LCP_utils.check_and_clear_cache(game_params)
        if 'b0' not in LCP_utils._cache:
            A4 = LCP_utils.compute_A4(game_params)
            LCP_utils._cache['b0'] = -(L + 1)**3 / A4
        return LCP_utils._cache['b0']
    
    @staticmethod
    def v_of_s(s, x2):
        return (x2 + 2*s**2 + 4*s + 1)/(2*(1 + s)**2)
    
    @staticmethod
    def b_of_s(s, b0, x2):
        return b0 - ((1 + 3*s)*(x2 - 1)) / (6*(1 + s)**3)
    
    @staticmethod
    def inverse_c(y, x2):
        # caller calls when y>c(s). 
        # Instead, find c_inv such that we call when s < c_inv(y)
        # x = v(s) < v(c_inv(y))
        # so call when x < v(c_inv(y))
        # Now we can distinguish fold/call regions with only y and x. 
        return (x2-y)/(y-1)
    
    @staticmethod
    def inverse_b(x, b0, x2, bracket=(1e-6, 100)):
        # Solve b(s) = x for s
        f = lambda s: LCP_utils.b_of_s(s, b0, x2) - x
        sol = root_scalar(f, bracket=bracket, method='brentq')
        if sol.converged:
            return sol.root
        else:
            raise ValueError("Root finding did not converge")

    @staticmethod
    def inverse_v(x, x2):
        # Solve v(s) = x for s
        return -1 - np.sqrt( (4*x-4) * (-2 + 2*x2) ) / (4*x-4)
    
    # integrate s over x and y, but we have x=v(s)
    # for each region:
    # break it into horizontal strips. 
    # for each strip, we have the left endpoint and right endpoint from x and y.
    # integrate s(x) over the strip using the inverse integration trick with x=v(s).
    # integrate the strips over y.4

    class Region:
        def point_in_region(self, x, y):
            return self.x_in_bounds(x) and self.y_in_bounds(y)
        
        def x_in_bounds(self, x):
            return self.x_min <= x < self.x_max
        
        def y_in_bounds(self, y):
            return self.y_min <= y < self.y_max
        
        def compute_area(self, grid_size=101):
            return compute_area(self.x_min_of_y, self.x_max_of_y, self.y_min, self.y_max, grid_size)
        
        def compute_s_integral(self, grid_size=101):
            raise NotImplementedError("compute_s_integral method must be implemented in subclasses")
        
        def compute_payoff(self, grid_size=101):
            area = self.compute_area(grid_size=grid_size)
            s_integral = self.compute_s_integral(grid_size=grid_size)
            return self.payoff_func(s_integral, area)
        
        def compute_payoff_vert_strip(self, grid_size=101):
            raise NotImplementedError("compute_payoff_vert_strip method must be implemented in subclasses")

    class InverseRegion(Region):
        def __init__(self, s_left_of_y, s_right_of_y, y_min, y_max, payoff_func, x_of_s):
            self.s_left_of_y = s_left_of_y
            self.s_right_of_y = s_right_of_y
            self.x_min_of_y = lambda y: x_of_s(self.s_left_of_y(y))
            self.x_max_of_y = lambda y: x_of_s(self.s_right_of_y(y))
            self.y_min = y_min
            self.y_max = y_max
            self.payoff_func = payoff_func
            self.x_of_s = x_of_s

        def compute_s_integral(self, grid_size=101):
            integrand = lambda y: inverse_integration(self.x_of_s, self.s_left_of_y(y), self.s_right_of_y(y), grid_size)
            return integrate(integrand, self.y_min, self.y_max, grid_size)
        
    class VariableRegion(Region):
        def __init__(self, x_min_of_y, x_max_of_y, y_min, y_max, payoff_func, s_of_xy):
            self.x_min_of_y = x_min_of_y
            self.x_max_of_y = x_max_of_y
            self.y_min = y_min
            self.y_max = y_max
            self.payoff_func = payoff_func
            self.s_of_xy = s_of_xy

        def compute_s_integral(self, grid_size=101):
            integrand = lambda y: integrate(lambda x: self.s_of_xy(x, y), self.x_min_of_y(y), self.x_max_of_y(y), grid_size)
            return integrate(integrand, self.y_min, self.y_max, grid_size)
    
        
    class ConstRegion(Region):
        def __init__(self, x_min_of_y, x_max_of_y, y_min, y_max, payoff_func, s):
            self.x_min_of_y = x_min_of_y
            self.x_max_of_y = x_max_of_y
            self.y_min = y_min
            self.y_max = y_max
            self.payoff_func = payoff_func
            self.s = s

        def compute_s_integral(self, grid_size=101):
            area = self.compute_area(grid_size=grid_size)
            s_integral = self.s * area
            return s_integral
    

class LCP(ContinuousPokerTemplate):
    @staticmethod
    def call_threshold(s, **kwargs):
        game_params = {'L': kwargs['L'], 'U': kwargs['U']}
        x2 = LCP_utils.compute_x2(game_params)
        return (x2+s)/(1+s)
    
    @staticmethod
    def bluff_threshold(**kwargs):
        game_params = {'L': kwargs['L'], 'U': kwargs['U']}
        return LCP_utils.compute_x2(game_params)
    
    @staticmethod
    def value_threshold(**kwargs):
        game_params = {'L': kwargs['L'], 'U': kwargs['U']}
        return LCP_utils.compute_x3(game_params)
    
    @staticmethod
    def bluff_size(x, **kwargs):
        game_params = {'L': kwargs['L'], 'U': kwargs['U']}
        L = game_params['L']
        U = game_params['U']
        x0 = LCP_utils.compute_x0(game_params)
        x1 = LCP_utils.compute_x1(game_params)
        x2 = LCP_utils.compute_x2(game_params)
        b0 = LCP_utils.compute_b0(game_params)
        if x < x0:
            return U
        elif x < x1:
            return LCP_utils.inverse_b(x, b0, x2)
        else:
            return L
        
    @staticmethod
    def value_size(x, **kwargs):
        game_params = {'L': kwargs['L'], 'U': kwargs['U']}
        L = game_params['L']
        U = game_params['U']
        x2 = LCP_utils.compute_x2(game_params)
        x4 = LCP_utils.compute_x4(game_params)
        x5 = LCP_utils.compute_x5(game_params)
        if x < x4:
            return L
        elif x < x5:
            return LCP_utils.inverse_v(x, x2)
        else:
            return U
        
    @staticmethod
    def expected_payoff_x(x, **kwargs):
        game_params = {'L': kwargs['L'], 'U': kwargs['U']}
        L, U = game_params['L'], game_params['U']
        x2 = LCP_utils.compute_x2(game_params)
        x3 = LCP_utils.compute_x3(game_params)
        v = lambda s : LCP_utils.v_of_s(s, x2)
        v_inv = lambda x : LCP_utils.inverse_v(x, x2)
        c = lambda s : LCP.call_threshold(s, **kwargs)
        if x <= x2: # all bluffs
            return x2 - 1/2
        elif x <= x3: # all checks
            return x-1/2
        else: 
            if x <= v(L): # min bets
                s=L
            elif x <= v(U): # intermediate bets
                s = v_inv(x)
            else: # max bets
                s = U
            return x*(2*s + 1) - s*(c(s) + 1) - 1/2
        
        
    @classmethod
    def expected_payoff_symbolic(cls, **kwargs):
        '''
        Compute the expected payoff using a reduced formula of just L and U.
        Much faster than the numerical integration.
        Formula found using mathematica.
        '''
        game_params = {'L': kwargs['L'], 'U': kwargs['U']}
        L, U = game_params['L'], game_params['U']
        A = U*(3+U*(3+U))
        numerator = A * (1+L)**3 - L**3 * (A+1)
        denominator = 2 * (
            (6 + 7 * A) * (L + 1)**3 - L**3 * (A + 1)
        )

        return numerator / denominator
        
    @classmethod
    def get_regions(cls, **kwargs):
        game_params = {'L': kwargs['L'], 'U': kwargs['U']}
        bth = cls.bluff_threshold(**kwargs)
        vth = cls.value_threshold(**kwargs)
        x2 = LCP_utils.compute_x2(game_params)
        b0 = LCP_utils.compute_b0(game_params)
        b = lambda s : LCP_utils.b_of_s(s, b0, x2)
        v = lambda s : LCP_utils.v_of_s(s, x2)
        c = lambda s : cls.call_threshold(s, **kwargs)
        c_inv = lambda y : LCP_utils.inverse_c(y, x2)
        U = game_params['U']
        L = game_params['L']

        # ----- Bluff Called -----
        # r0: x < b(U), y > c(U), s = U
        r0 = LCP_utils.ConstRegion(
            x_min_of_y=lambda y: 0,
            x_max_of_y=lambda y: b(U),
            y_min=c(U),
            y_max=1,
            payoff_func=ContinuousPokerTemplate.lose_showdown_payoff,
            s=U
        )

        # r1: b(U) < x < b(L), y > c(U), b(s) = x
        r1 = LCP_utils.InverseRegion(
            s_left_of_y=lambda y: U,
            s_right_of_y=lambda y: L,
            y_min=c(U),
            y_max=1,
            payoff_func=ContinuousPokerTemplate.lose_showdown_payoff,
            x_of_s=b
        )

        # r2: b(c_inv(y)) < x < b(L), c(L) < y < c(U), b(s) = x
        r2 = LCP_utils.InverseRegion(
            s_left_of_y=lambda y: c_inv(y),
            s_right_of_y=lambda y: L,
            y_min=c(L),
            y_max=c(U),
            payoff_func=ContinuousPokerTemplate.lose_showdown_payoff,
            x_of_s=b
        )

        # r3: b(L) < x < bth, y > c(L), s = L
        r3 = LCP_utils.ConstRegion(
            x_min_of_y=lambda y: b(L),
            x_max_of_y=lambda y: bth,
            y_min=c(L),
            y_max=1,
            payoff_func=ContinuousPokerTemplate.lose_showdown_payoff,
            s=L
        )

        # ---- Bluff Fold -----
        # r4: x < b(U), c(L) < y < c(U)
        r4 = LCP_utils.ConstRegion(
            x_min_of_y=lambda y: 0,
            x_max_of_y=lambda y: b(U),
            y_min=c(L),
            y_max=c(U),
            payoff_func=ContinuousPokerTemplate.win_ante_payoff,
            s=0 # s is irrelevant
        )

        # r5: b(U) < x < b(c_inv(y)), c(L) < y < c(U)
        r5 = LCP_utils.ConstRegion(
            x_min_of_y=lambda y: b(U),
            x_max_of_y=lambda y: b(c_inv(y)),
            y_min=c(L),
            y_max=c(U),
            payoff_func=ContinuousPokerTemplate.win_ante_payoff,
            s=0  # s is irrelevant
        )

        # r6: x < bth, y < c(L)
        r6 = LCP_utils.ConstRegion(
            x_min_of_y=lambda y: 0,
            x_max_of_y=lambda y: bth,
            y_min=0,
            y_max=c(L),
            payoff_func=ContinuousPokerTemplate.win_ante_payoff,
            s=0  # s is irrelevant
        )

        # ----- Check Loses -----
        # r7: bth < x < vth, y > vth
        r7 = LCP_utils.ConstRegion(
            x_min_of_y=lambda y: bth,
            x_max_of_y=lambda y: vth,
            y_min=vth,
            y_max=1,
            payoff_func=ContinuousPokerTemplate.lose_ante_payoff,
            s=0 
        )
            
        # r8: bth < x < y, bth < y < vth -- PERFECTLY CANCELS WITH r9
        
        # ----- Check Wins -----
        # r9: y < x < vth, bth < y < vth -- PERFECTLY CANCELS WITH r8
        
        # r10: bth < x < vth, y < bth
        r10 = LCP_utils.ConstRegion(
            x_min_of_y=lambda y: bth,
            x_max_of_y=lambda y: vth,
            y_min=0,
            y_max=bth,
            payoff_func=ContinuousPokerTemplate.win_ante_payoff,
            s=0  # No specific s value for this region
        )

        # ----- Value Loses -----
        # r11: vth < x < v(L), y > v(L), s=L
        r11 = LCP_utils.ConstRegion(
            x_min_of_y=lambda y: vth,
            x_max_of_y=lambda y: v(L),
            y_min=v(L),
            y_max=1,
            payoff_func=ContinuousPokerTemplate.lose_showdown_payoff,
            s=L
        )
        
        # r12: vth < x < y, vth < y < v(L), s=L -- PERFECTLY CANCELS WITH r16
        
        # r13: v(L) < x < v(U), v(U) < y < 1, s=v_inv(x)
        r13 = LCP_utils.VariableRegion(
            x_min_of_y=lambda y: v(L),
            x_max_of_y=lambda y: v(U),
            y_min=v(U),
            y_max=1,
            payoff_func=ContinuousPokerTemplate.lose_showdown_payoff,
            s_of_xy=lambda x, y : LCP_utils.inverse_v(x, x2)
        )
            
        # r14: v(L) < x < y, v(L) < y < v(U), x=v_inv(s) 
        r14 = LCP_utils.VariableRegion(
            x_min_of_y=lambda y: v(L),
            x_max_of_y=lambda y: y,
            y_min=v(L),
            y_max=v(U),
            payoff_func=ContinuousPokerTemplate.lose_showdown_payoff,
            s_of_xy=lambda x, y : LCP_utils.inverse_v(x, x2)
        )

        # r15: v(U) < x < y, y > v(U), s=U -- PERFECTLY CANCELS WITH r21
    
        # ----- Value Wins -----
        # r16: y < x < v(L), vth < y < v(L), s=L -- PERFECTLY CANCELS WITH r12

        # r17: vth < x < v(L), c(L) < y < vth, s=L
        r17 = LCP_utils.ConstRegion(
            x_min_of_y=lambda y: vth,
            x_max_of_y=lambda y: v(L),
            y_min=c(L),
            y_max=vth,
            payoff_func=ContinuousPokerTemplate.win_showdown_payoff,
            s=L
        )

        # r18: y < x < v(U), v(L) < y < v(U), s=v_inv(x)
        r18 = LCP_utils.VariableRegion(
            x_min_of_y=lambda y: y,
            x_max_of_y=lambda y: v(U),
            y_min=v(L),
            y_max=v(U),
            payoff_func=ContinuousPokerTemplate.win_showdown_payoff,
            s_of_xy=lambda x, y : LCP_utils.inverse_v(x, x2)
        )

        # r19: v(L) < x < v(U), c(U) < y < v(L), v(s)=x
        r19 = LCP_utils.InverseRegion(
            s_left_of_y=lambda y: L,
            s_right_of_y=lambda y: U,
            y_min=c(U),
            y_max=v(L),
            payoff_func=ContinuousPokerTemplate.win_showdown_payoff,
            x_of_s=v
        )

        # r20: v(L) < x < v(c_inv(y)), c(L) < y < c(U), v(s)=x
        r20 = LCP_utils.InverseRegion(
            s_left_of_y=lambda y: L,
            s_right_of_y=lambda y: c_inv(y),
            y_min=c(L),
            y_max=c(U),
            payoff_func=ContinuousPokerTemplate.win_showdown_payoff,
            x_of_s=v
        )

        # r21: y < x, y > v(U), s=U -- PERFECTLY CANCELS WITH r15

        # r22: x > v(U), c(U) < y < v(U), s=U
        r22 = LCP_utils.ConstRegion(
            x_min_of_y=lambda y: v(U),
            x_max_of_y=lambda y: 1,
            y_min=c(U),
            y_max=v(U),
            payoff_func=ContinuousPokerTemplate.win_showdown_payoff,
            s=U
        )

        # ------ Value Fold -----
        # r23: v(c_inv(y)) < x, c(L) < y < c(U)
        r23 = LCP_utils.ConstRegion(
            x_min_of_y=lambda y: v(c_inv(y)),
            x_max_of_y=lambda y: 1,
            y_min=c(L),
            y_max=c(U),
            payoff_func=ContinuousPokerTemplate.win_ante_payoff,
            s=0  # s is irrelevant
        )

        # r24: x > vth, y < c(L)
        r24 = LCP_utils.ConstRegion(
            x_min_of_y=lambda y: vth,
            x_max_of_y=lambda y: 1,
            y_min=0,
            y_max=c(L),
            payoff_func=ContinuousPokerTemplate.win_ante_payoff,
            s=0  # s is irrelevant
        )

        regions = {
            0: r0, 1: r1, 2: r2, 3: r3, 4: r4, 5: r5, 6: r6,
            7: r7, 10: r10,
            11: r11, 13: r13, 14: r14,
            17: r17, 18: r18, 19: r19,
            20: r20, 22: r22,
            23: r23, 24: r24
        }

        return regions

    @classmethod
    def expected_payoff_by_region(cls, grid_size=1001, **kwargs):
        '''
        Compute the integral over the square by regions to avoid ever solving for v_inv and b_inv.
        Not any faster than the numerical integration, but proof of concept for a symbolic integration.
        '''
        regions = cls.get_regions(**kwargs)

        total_payoff = 0
        for i, r in regions.items():
            payoff = r.compute_payoff() 
            # print(f"Payoff for region {i}: {payoff}")
            total_payoff+= payoff
        return total_payoff