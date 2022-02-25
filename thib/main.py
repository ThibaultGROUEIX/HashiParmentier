import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import torch
from easydict import EasyDict
import os



def main(path="./input/"):
    # PARSER
    global_args= EasyDict()

    contributors_name = []
    contributors_num_skills = []
    contributors_skills = {}
    project_name = []
    project_duration = []
    project_score = []
    project_date = []
    project_num_roles = []
    project_roles = {}
    line = 0
    skill_list = []
    skill_to_contributor = {}
    skill_level_to_contributor = {}
    num_project_per_people =  {}

    with open(path, 'r') as file_reader:
        first_args_list = file_reader.readline().split(' ')

        global_args["number_of_contributor"] = int(first_args_list[0])
        global_args["number_of_project"] = int(first_args_list[1])

        for i in range(global_args["number_of_contributor"]):
            next_args_1 = file_reader.readline().split(' ')
            contributors_name.append(next_args_1[0])
            num_project_per_people[next_args_1[0]] = 0
            contributors_num_skills.append(int(next_args_1[1]))
            contributors_skills[next_args_1[0]] = {}

            for i in range(int(next_args_1[1])):
                next_args_2 = file_reader.readline().split(' ')
                level =  int(next_args_2[1])
                skill_name = next_args_2[0]
                if skill_name not in skill_list:
                    skill_list.append(skill_name)
                    skill_to_contributor[skill_name] = []
                    skill_level_to_contributor[skill_name] = {}

                for level_ in range(level+1):
                    if level_ not in skill_level_to_contributor[skill_name].keys():
                        skill_level_to_contributor[skill_name][level_] = []
                skill_level_to_contributor[skill_name][level].append(next_args_1[0]) 

                skill_to_contributor[skill_name].append(next_args_1[0])

                contributors_skills[next_args_1[0]][skill_name] = level
        
        for i in range(global_args["number_of_project"]):
            next_args_1 = file_reader.readline().split(' ')
            project_name.append(next_args_1[0])
            project_score.append(int(next_args_1[2]))
            project_date.append(int(next_args_1[3]))
            project_num_roles.append(int(next_args_1[4]))
            project_roles[next_args_1[0]] = []
            
            for i in range(int(next_args_1[4])):
                next_args_2 = file_reader.readline().split(' ')
                project_roles[next_args_1[0]].append((next_args_2[0],int(next_args_2[1])))
        ## More data processing
        ## Skills to people

        ## ALGO
        number_of_executed_project =  global_args["number_of_project"]
        from copy import deepcopy
        project_to_tackle = deepcopy(project_name)
        _, indices = torch.sort(torch.Tensor(project_date))
        project_to_tackle = [project_to_tackle[i] for i in indices]

        project_list_in_order = []

        contributors = {}
        step = 0
        while len(project_to_tackle) > 0:
            step += 1
            if step > len(project_to_tackle):
                break

            project = project_to_tackle[0]
            project_to_tackle.remove(project)
            project_to_tackle.append(project)

            drop_project = False
            skills = deepcopy(project_roles[project])
            contributors[project] = deepcopy(skills)
            people_to_upgrade = []
            skills_backup = deepcopy(skills)
            if project=="PhoneUltrav1":
                a=0
            while len(skills) > 0:
                availability = 100000
                num_item = 0
                for num, (skill, level) in enumerate(skills):
                    avail = count_number_available_dude(skill_level_to_contributor[skill], level)
                    if avail < availability:
                        availability = avail
                        num_item = num
                
                skill, level = skills[num_item]
                num_item_backup = contributors[project].index((skill, level))


                if not drop_project:
                    level_to_contributor = skill_level_to_contributor[skill]
                    
                    if level not in level_to_contributor.keys():
                        # Skip this project (for now :) 
                        drop_project = True
                        break
                    else:
                        # Pick
                        list_of_potential_contributors = []
                        level_max = max(level_to_contributor.keys())
                        candidate_for_mentorring = level_to_contributor[level-1]

                        for i in range(level,level_max+1):
                            list_of_potential_contributors += level_to_contributor[i]
                        
                        found_contributor = False
                        #filter 1
                        list_of_potential_contributors_2 = []
                        for contrib_potential in list_of_potential_contributors:
                            if not contrib_potential in contributors[project]:
                                list_of_potential_contributors_2.append(contrib_potential)
                        
                        found_mentor = False
                        for mentor in list_of_potential_contributors_2:
                            if found_mentor:
                                continue
                            item_mentor = 0
                            for iiiii, (skill__, level__) in enumerate(skills):
                                if iiiii== num_item:
                                    continue
                                if skill__ in contributors_skills[mentor]:
                                    if contributors_skills[mentor][skill__] >=level__:
                                        found_mentor = True
                                        mentor = mentor
                                        skill_mentor = skill__
                                        level_mentor = level__
                                        item_mentor = iiiii
                                        break
                        
                        if found_mentor and len(candidate_for_mentorring)>0:
                            found_contributor = True
                            item_mentor_back = contributors[project].index((skill_mentor, level_mentor))

                            if num_item>=item_mentor:
                                print(num_item, item_mentor)
                                skills.pop(num_item)
                                skills.pop(item_mentor)
                            else:
                                print(item_mentor)
                                skills.pop(item_mentor)
                                skills.pop(num_item)

                            num_project_per_people[candidate_for_mentorring[0]]+=1
                            
                            contributors[project][num_item_backup] = candidate_for_mentorring[0]
                            contributors[project][item_mentor_back] = mentor
                            try:
                                if contributors_skills[mentor][skill_mentor] == level_mentor:
                                    people_to_upgrade.append((mentor, skill_mentor))
                            except:
                                a=0
                            people_to_upgrade.append((candidate_for_mentorring[0], skill))


                        else:
                            list_num_project = []
                            if len(list_of_potential_contributors_2)>0:
                                for contrib_potential in list_of_potential_contributors_2:
                                    list_num_project.append(num_project_per_people[contrib_potential])

                                index = torch.argmin(torch.Tensor(list_num_project))
                                # contrib_potential = list_of_potential_contributors_2[index.int().item()]
                                contrib_potential = list_of_potential_contributors_2[0]
                                found_contributor = True
                                skills.pop(num_item)
                                num_project_per_people[contrib_potential]+=1
                                contributors[project][num_item_backup] = contrib_potential
                                if contributors_skills[contrib_potential][skill] == level:
                                    people_to_upgrade.append((contrib_potential, skill))
                        if not found_contributor:
                            drop_project = True
                            break


            if not drop_project:
                step = 0

                # Upgrade contributors skills.
                for people, skill in people_to_upgrade:
                    old_level = contributors_skills[people][skill]
                    contributors_skills[people][skill] += 1
                    skill_level_to_contributor[skill][old_level].remove(people)
                    if not old_level+1 in skill_level_to_contributor[skill].keys():
                        skill_level_to_contributor[skill][old_level+1] = []
                    skill_level_to_contributor[skill][old_level+1].append(people)
                project_to_tackle.remove(project)
                project_list_in_order.append(project)

        with open(path[:-4] + "_output.txt", 'w') as file_reader:
            file_reader.write(f"{len(project_list_in_order)}\n")

            for i, name in enumerate(project_list_in_order):
                file_reader.write(f"{name}\n")
                contrib = contributors[name]
                my_str = (" ").join(contrib)
                file_reader.write(f"{my_str}\n")

    print("done")

def count_number_available_dude(skill_level_to_contributor_skill, level):
    level_max = max(skill_level_to_contributor_skill.keys())
    reutrn_val = 0
    for i in range(level, level_max+1):
        reutrn_val += len(skill_level_to_contributor_skill[i])
    return reutrn_val

if __name__ == '__main__':
    main("./input/f_find_great_mentors.in.txt")
    main("./input/a_an_example.in.txt")
    main("./input/b_better_start_small.in.txt")
    main("./input/c_collaboration.in.txt")
    main("./input/d_dense_schedule.in.txt")
    main("./input/e_exceptional_skills.in.txt")






