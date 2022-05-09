# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from import_dataset import google_directed, ca_undirected, vk_directed


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print(google_directed('.test.txt', 6).get_all_edges())
    # print(ca_undirected('.test.txt', 6).get_all_edges())
    print(vk_directed('.test.csv', 7).get_all_edges())



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
