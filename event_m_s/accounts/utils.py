

# user detection function

def detectUser(user):
    if user.role == 'cs':
        redirectURL = 'customerDashboard'
        return redirectURL
    elif user.role == 'ad':
        redirectURL = 'adminDashboard'
        return redirectURL