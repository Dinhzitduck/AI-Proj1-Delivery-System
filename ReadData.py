def read_data(filepath):
    with open(filepath) as file:
        n, m, t, f = map(int, file.readline().split())
        grid = [list(file.readline().split()) for _ in range(n)]
    return grid, t, f



def convert_date_lv1(data):
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] != '-1' and data[i][j] != '0' and data[i][j] != 'S' and data[i][j] != 'G':
                data[i][j] = '0'
    return data
    
def convert_date_lv2(data):
    for i in range(len(data)):
        for j in range(len(data[i])):
            if len(data[i][j]) >= 2 and (data[i][j][0] in ['S', 'G', 'F']):
                data[i][j] = '0'
    return data


def main():   
    grid, t, f = read_data('input1.txt')
    map1 = convert_date_lv2(grid)
    print(map1)    
if __name__ == "__main__":
    main()