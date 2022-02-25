import os
import numpy as np

class Project():
    def __init__(self, name, days, score, bestbefore, nb_roles):
        self.name = name
        self.days = days
        self.score = score
        self.bestbefore = bestbefore
        self.nb_roles = nb_roles
        self.roles = []

class Solution():

    def __init__(self, nb_proj):
        self.nb_proj = nb_proj

        self.projects_assigned = {}
        ## dict of project: [list of contribuors}




def read_input(filename, pathdir="../input_data/"):
    input_args = dict()
    with open(pathdir + filename, 'r') as file_reader:
        first_args_list = file_reader.readline().split(' ')

        input_args["num_contributors"] = int(first_args_list[0])
        input_args["num_projects"] = int(first_args_list[1])

        num_contrib_added = 0
        contributors = {}
        while num_contrib_added < input_args["num_contributors"]:
            contrib_args = file_reader.readline().split(' ')
            name = contrib_args[0]
            num_skills = int(contrib_args[1])

            skill_list = {}
            for sk in range(num_skills):
                skill_line = file_reader.readline().split(' ')
                name_skill = skill_line[0]
                level = int(skill_line[1])
                skill_list[name_skill] = level
            contributors[name] = skill_list

            num_contrib_added += 1

        num_projects_add = 0
        projects = []
        while num_projects_add < input_args["num_projects"]:

            line_proj = file_reader.readline().rstrip('\n').split(' ')
            # print("line car: ", line_car)
            name_proj = (line_proj[0])
            proj = Project(line_proj[0],
                           int(line_proj[1]),
                           int(line_proj[2]),
                           int(line_proj[3]),
                           int(line_proj[4]))
            roles = int(line_proj[4])

            for r_i in range(roles):
                line_role = file_reader.readline().split(' ')
                proj.roles.append( (line_role[0],int(line_role[1])) )

            projects.append(proj)
            num_projects_add +=1

    return contributors, projects


# contributors, projects = read_input("a_an_example.in.txt", pathdir="input_data/")

def write_output(file_path, solution):
    with open(file_path, 'w') as file_writer:
        file_writer.write(str(solution.nb_proj))
        for proj in solution.projects_assigned:
            file_writer.write("\n" + proj + "\n" + " ".join(solution.projects_assigned[proj]))

    return 1




def submitter(fname, intersect_dict):
    f = open(f"{fname}.txt", "w")
    f.write(f'{len(intersect_dict)}\n')
    for intersection, timers in intersect_dict.items():
        f.write(f'{intersection}\n')
        f.write(f'{len(timers)}\n')
        for timer in timers:
            f.write(f'{timer[0].name} {timer[1]}\n')
    f.close()
