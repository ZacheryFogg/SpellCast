def map_str_to_2d_list(str) -> list:
        
        list_2d = []
        i = 1
        row = []
        for char in str:
            row.append(char)
            if i%5 == 0:
                list_2d.append(row)
                row = []
            i+=1

        return list_2d

# Example usage
input_str = "aoublfriuapcdajroeexsozui"
output = map_str_to_2d_list(input_str)
print(output)