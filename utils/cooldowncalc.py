import math

def getCooldown(grow, C0):
    # C0 : 기본 쿨타임 (육성 0 기준)
    cooldown = C0
    pow = 2
    while 100 <= grow:
        cooldown *= (math.pow(2, pow) - 1) / math.pow(2, pow)
        grow -= 100
        pow += 1
    cooldown *= math.pow((math.pow(2, pow) - 1) / math.pow(2, pow), grow / 100)
    return round(cooldown, 2)

def getGrow(C_target, C0, tol=1e-4):
    """
    주어진 스킬 쿨타임(C_target)에 해당하는 육성 수치(x)를 계산합니다.
    
    Args:
        C_target (float): 목표 스킬 쿨타임 (초)
        C0 (float): 기본 쿨타임 (육성 0 기준)
        tol (float): 허용 오차 (기본값 1e-4)
        
    Returns:
        float: 육성 수치 (0~300 범위)
    """
    def cooldown_function(x):
        r1 = 0.75
        r2 = 0.875
        r3 = 0.9375
        f1 = min(x, 100) / 100
        f2 = max(0, min(x - 100, 100)) / 100
        f3 = max(0, min(x - 200, 100)) / 100
        return C0 * (r1 ** f1) * (r2 ** f2) * (r3 ** f3)
    # 이분 탐색
    low = 0
    high = 300
    while high - low > tol:
        mid = (low + high) / 2
        C_mid = cooldown_function(mid)
        if C_mid > C_target:
            low = mid
        else:
            high = mid
    return int((low + high) / 2)
