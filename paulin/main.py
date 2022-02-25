import numpy as np
import os
import time as tt

from paulin.read_write_paulin import Solution, Project, read_input, write_output


# b_better_start_small.in.txt
entries = {"b":"b_better_start_small.in.txt",
 "c":"c_collaboration.in.txt",
"d":"d_dense_schedule.in.txt",
"e":"e_exceptional_skills.in.txt",
"f":"f_find_great_mentors.in.txt"}

letter = "f"
contributors, projects = read_input(entries[letter], #"a_an_example.in.txt"
                                    pathdir="../input_data/")

contributors_time_to_availability = {}
for contrib in contributors: ## add time to availability
    contributors_time_to_availability[contrib] = (0, contributors[contrib])

def update_pool_competences(contrib_dict):
    # max level of competence

    pool_competences = {}
    for contrib in contrib_dict:
        for compet, level in contrib_dict[contrib]:
            if compet in pool_competences:
                pool_competences[compet] = max(level, pool_competences[compet])
            else:
                pool_competences[compet] = level
    return pool_competences

# pool_competences = update_pool_competences(contributors)

def pool_competences_dict(contrib_dict):
    ##dict of avb competences with list of (contrib,level)
    compet_dict = {}
    for contrib in contrib_dict:
        compet_list = contrib_dict[contrib]
        for compet in compet_list:
            if contrib not in compet_dict:
                compet_dict[compet] = [(contrib, compet_list[compet]),]
            else:
                compet_dict[compet].append( (contrib, compet_list[compet]), )
    return compet_dict


def pool_has_needed_competences(pool_competences, contributors, project_roles, contributors_avb_list):
    added_contributors = []
    mentored = [] #list of person and competence to mentor
    avb_contrib_for_project = contributors_avb_list.copy()

    def exist_mentor_in_list_contrib(list_contrib, role_to_find, needed_level):
        for contrib in list_contrib:

            if role_to_find in contributors[contrib] and contributors[contrib][role_to_find] >= needed_level:
                return True
        return False

    for (role, level) in project_roles:
        has_found_contr = False
        if role in pool_competences:
            list_contrib_level = sorted(pool_competences[role], key=lambda r : r[1], reverse=True)

            for (contrib, level_contrib) in list_contrib_level: ##iterate on list of possible until avb..
                if level_contrib < level -1:
                    return None
                elif level_contrib == level -1: ##check if there is an existing mentor
                    if not  exist_mentor_in_list_contrib(added_contributors, role, level):
                        return None
                    else: ## take this contributor and add as trainee
                        if avb_contrib_for_project[contrib] == 0:
                            added_contributors.append(contrib)
                            mentored.append( (contrib, role ),)
                            avb_contrib_for_project[contrib] = 1
                            has_found_contr = True
                            break
                else:
                    if avb_contrib_for_project[contrib] ==0:
                        added_contributors.append(contrib)
                        avb_contrib_for_project[contrib] = 1
                        has_found_contr = True
                        break
            if not has_found_contr:
                return None
        else:
            return None
    return added_contributors, mentored

# contrib_avail = {contrib:0 for contrib in contributors}
# r = pool_has_needed_competences(avb_comp, contributors, projects[0].roles, contrib_avail)
#


def update_avb_contribs_with_working_project(avb_contribs_dict, contributors_working, project_duration):
    for contrib in contributors_working:
        avb_contribs_dict[contrib] = project_duration, avb_contribs_dict[contrib][1]



# def update_avb_competences_with_working_project(avb_compet_dict, contributors_working):
#     for compet in avb_compet_dict:
#         i
#
# #



solution = Solution(nb_proj=0)

available_competences = contributors.copy()

contrib_avail = {contrib:0 for contrib in contributors} ## 0 meaning availablitly now


time = 0
avb_comp = pool_competences_dict(contributors)

proj_still_feasible = projects.copy()

start_time = tt.time()

while proj_still_feasible : #check still projects exists

    projects_possible = [p for p in proj_still_feasible if
                         (pool_has_needed_competences(avb_comp, contributors, p.roles, contrib_avail) is not None)]

    if projects_possible:
        ## sort project by ascending (num_days/score)
        projects_possible.sort(key= lambda p : p.days/ p.score)

        project_treat = projects_possible[0]
        #remove p from feasible projects:
        proj_still_feasible.remove(project_treat)

        contributors_affected, mentored = pool_has_needed_competences(avb_comp, contributors, project_treat.roles, contrib_avail)

        for contrib in contributors_affected: ## contributors will be available in time t+ p.days
            contrib_avail[contrib] = project_treat.days

        ## add project
        solution.nb_proj += 1
        solution.projects_assigned[project_treat.name] = contributors_affected

        ## improve competences of mentored and update avb_competences:
        for (mentored_contrib, role_mentored) in mentored:
            contributors[mentored_contrib][role_mentored] +=1
            avb_comp = pool_competences_dict(contributors)

    if not projects_possible:  ## n
        ## got to t+1
        time = time + 1
        print("time = ", time)

        if tt.time() > start_time + 200:
            break
        for contrib in contrib_avail:
            contrib_avail[contrib] = max(0, contrib_avail[contrib] - 1)
        for proj in proj_still_feasible:
            proj.bestbefore += -1

        proj_still_feasible = [proj for proj in proj_still_feasible if proj.bestbefore >= proj.days]
        if not proj_still_feasible:
            break

    # for p in projects_possible:
    #     p.bestbefore += - project_treat.days
    # projects_possible = [p for p in projects_possible if p.bestbefore >0]





# project.


write_output("../outputs_paulin/"+letter+".out", solution)