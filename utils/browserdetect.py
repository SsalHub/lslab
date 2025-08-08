
def isMobile(user_agent):
    mobile_keywords = ["Mobile", "Android", "iPhone", "iPad", "iPod"]
    return any(keyword in user_agent for keyword in mobile_keywords)