alphabet = "a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z".split(",")

def get_index(character):
    # Get the index associated to a letter (used in the transition table)
    # return the index found
    return ord(character) - ord('a')

