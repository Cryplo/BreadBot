def read_misc_file(filepath) -> str:
    """Takes in a string filepath, returns the content of that file as a string"""
    with open(filepath) as my_file:
        file_content = my_file.read()
    return file_content


def bread_file_to_list(filepath) -> list:
    """Takes in a string filepath, returns the content of that file with each line being an element in a list"""
    with open(filepath) as my_file:
        bread_list = [s.strip() for s in my_file.readlines()]
    return bread_list


misc_paths = ['text_files/misc_text_files/updateLog.txt', 'text_files/misc_text_files/help.txt',
              'text_files/misc_text_files/faq.txt']
# Initializes variables by setting them equal to the string returned by calling read_misc_file
# on the corresponding misc_path
updateLog, helpContent, faqContent = map(read_misc_file, misc_paths)

bread_paths = ['text_files/bread_data/common_bread.txt', 'text_files/bread_data/rare_bread.txt',
               'text_files/bread_data/mythical_bread.txt', 'text_files/bread_data/legendary_bread.txt']



print("Config Done")

# Does the same thing, but sets the variables equal to lists instead of strings
common_bread, rare_bread, mythical_bread, legendary_bread = map(bread_file_to_list, bread_paths)


bake_cooldown = 600
#Make sure adds up to 1,000
bake_percents = [600,350,47,3]
