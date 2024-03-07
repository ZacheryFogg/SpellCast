def convert_to_2d_list(input_str):
    # Remove the outer brackets and split the string into rows
    rows = input_str[1:-1].split('],[')
    
    # Split each row into elements and strip whitespace
    list_2d_str = [[element.strip() for element in row.split(',')] for row in rows]

    return list_2d_str

# Example usage
input_str = "[[o,e,v,u,a],[n,o,y,i,u],[w,r,h,e,a],[l,o,i,k,f],[m,h,r,t,f]]"
output = convert_to_2d_list(input_str)
print(output)