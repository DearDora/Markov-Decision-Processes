from beautifultable import BeautifulTable
import copy

def print_table(U):
    x = copy.deepcopy(U)
    for i in range(3):
        x[i].insert(0,i+1)
    p = BeautifulTable()
    p.append_row([" ",1,2,3,4])
    for row in x:
        p.append_row(row)
    print(p) 

def up(U,row,col):
    # Bump into the wall
    if (row == 0) or (row == 2 and col == 1):
        return U[row][col]
    else:
        return U[row-1][col]

def down(U,row,col):
    # Bump into the wall
    if (row == 2) or (row == 0 and col == 1):
        return U[row][col]
    else:
        return U[row+1][col]

def left(U,row,col):
    # Bump into the wall
    if (col == 0) or (row == 1 and col == 2):
        return U[row][col]
    else:
        return U[row][col-1]

def right(U,row,col):
    # Bump into the wall
    if (col == 3) or (row == 1 and col == 0):
        return U[row][col]
    else:
        return U[row][col+1]

# Bellman equations store the three decimal places    
def Bellman(U,r_s,gama,row,col):
    u = up(U,row,col)
    d = down(U,row,col)
    l = left(U,row,col)
    r = right(U,row,col)
    result = r_s + gama*max(0.8*u+0.1*l+0.1*r,0.8*d+0.1*r+0.1*l,0.8*l+0.1*d+0.1*u,0.8*r+0.1*u+0.1*d)
    return round(result,4)
    

# Update U from right to left with Bellman equations and return the updated U
def update_U(U,r_s,gama):
    updated_U = copy.deepcopy(U)
    for i in reversed(range(0,3)):
        for j in reversed(range(0,4)):
            # Do not update "X" and terminate states
            if (i == 1 and j == 1) or (i == 1 and j == 3) or (i == 2 and j == 3):
                continue
            # Update state
            updated_U[i][j] = Bellman(U,r_s,gama,i,j)
    for i in reversed(range(0,3)):
        for j in reversed(range(0,4)):
            # Do not update "X" and terminate states
            if (i == 1 and j == 1) or (i == 1 and j == 3) or (i == 2 and j == 3):
                continue
            updated_U[i][j] = round(updated_U[i][j],3)
    return updated_U

def find_policy(U):
    policy = [[0,0,0,0],[0,"X",0,-1],[0,0,0,1]]
    for i in reversed(range(0,3)):
        for j in reversed(range(0,4)):
            # Do not update "X" and terminate states
            if (i == 1 and j == 1) or (i == 1 and j == 3) or (i == 2 and j == 3):
                continue
            # Find policy
            u = up(U,i,j)
            d = down(U,i,j)
            l = left(U,i,j)
            r = right(U,i,j)
            up_ = 0.8*u+0.1*l+0.1*r
            down_ = 0.8*d+0.1*l+0.1*r
            left_ = 0.8*l+0.1*u+0.1*d
            right_ = 0.8*r+0.1*u+0.1*d
            max_u = max(up_,down_,left_,right_)
            result = ""
            if up_ == max_u:
                result += "↑"
            if down_ == max_u:
                result += "↓"
            if left_ == max_u:
                result += "←"
            if right_ == max_u:
                result += "→"
            policy[i][j] = result
    return policy
            

def main():
    # Start with initial values for the true utilities
    init_utility = [[0,0,0,0],[0,"X",0,-1],[0,0,0,1]]
    gama = 1
    R_s = -1.0
    U = init_utility
    U_new = update_U(U,R_s,gama)
    # Iterate until the maximum change from Ui(s) to Ui+1(s) for all s is 
    # small enough
    print("Initial utility:")
    print_table(U)
    iteration = 1
    while (True):        
        U = copy.deepcopy(U_new)
        U_new = update_U(U,R_s,gama)
        if U != U_new:
            print("Iteration "+str(iteration)+":")
            print_table(U_new)
            iteration += 1
            continue
        else:
            print("After executed iteration "+str(iteration-1)+", it reaches to the optimal utility.")
            break
    # Terminate and find the optimal U
    optimal_U = U_new
    print("**********Optimal Utility**********")
    print_table(optimal_U)
    # Find the policy of the optimal U
    optimal_policy = find_policy(optimal_U)
    # Print the policy table
    print("**********Optimal Policy**********")
    print_table(optimal_policy)

if __name__ == "__main__":
    main()