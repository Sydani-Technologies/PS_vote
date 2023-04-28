import frappe
from frappe import auth
import json
from datetime import date

@frappe.whitelist(allow_guest=True)
def login(usr, pwd):
    try:
        login_manager = auth.LoginManager()
        login_manager.authenticate(user=usr, pwd=pwd)
        login_manager.post_login()

        # frappe.msgprint(str('Logged in as ' + frappe.session.user))

        frappe.response['message'] = {
            "success_key": 1,
            "user": frappe.session.user
        }

    except frappe.AuthenticationError:
        frappe.response['message'] = {
            "success_key": 0,
            "message": "Authentication Error"
        }

    return


@frappe.whitelist(allow_guest=True)
def cast_vote(employee_voted, ps, user_email):
    employee_voted_dic = json.loads(employee_voted)

    # get todays date
    todays_date = date.today()

    # check if the user has already voted today
    todays_user_vote = frappe.db.get_value('Ps_vote', {'voter_name': user_email, 'created': todays_date}, 'voter_name')
    if todays_user_vote:
        frappe.response['message'] = {
            "success_key": 0,
            "message": 'has voted already'
        }
    else:
        # create a new Ps_vote document
        ps_vote = frappe.get_doc({
            'doctype': 'Ps_vote',
            'voter_name': user_email,
            'vote_name': employee_voted_dic['employee_name'],
            'ps': ps,
            'votes': 1,
            'created': todays_date
        })
        ps_vote.insert()
    
        frappe.response['message'] = {
            "success_key": 1,
            "message": 'Submitted Successfully'
        }

@frappe.whitelist(allow_guest=True)
def get_result(team, from_date='', to_date=''):
    # todays_date = '2023-3-12'
    todays_date = date.today()
    if frappe.session.user == 'Guest':
        return frappe.session.user
    else:
        if team == 'Latitude' or team == 'Longitude':

            stmt = f"""SELECT vote_name, ps, COUNT(votes) as votes_today FROM `tabPs_vote` """
            total_votes_stmt = f"""SELECT vote_name, votes, voter_name, ps, created  FROM `tabPs_vote` """

            if team == "Latitude":
                add_ps_filter = "WHERE `ps` = 'Latitude' "
                stmt += add_ps_filter
                total_votes_stmt += add_ps_filter
            elif team == "Longitude":
                add_ps_filter = "WHERE `ps` = 'Longitude' "
                stmt += add_ps_filter
                total_votes_stmt += add_ps_filter
            elif team == "Combined":
                add_ps_filter = "WHERE `ps` = 'Combined' "
                stmt += add_ps_filter
                total_votes_stmt += add_ps_filter
            frappe.msgprint(str("kfdk,szfn"))


            if from_date != '' and to_date == '':
                date_filter = f"AND `created` = '{todays_date}' "
            elif from_date != '' and to_date != '':
                date_filter = f"AND `created` BETWEEN CAST('{from_date}' AS DATE) AND CAST('{to_date}' AS DATE) "
            else:
                date_filter = f"AND `created` = '{todays_date}' "

            stmt += date_filter
            stmt += 'GROUP BY vote_name ORDER BY COUNT(votes) DESC LIMIT 12'
            total_votes_stmt += date_filter

        else:
            stmt = f"""SELECT vote_name, ps, COUNT(votes) as votes_today FROM `tabPs_vote` """
            total_votes_stmt = f"""SELECT vote_name, votes, voter_name, ps, created  FROM `tabPs_vote` """

            if from_date != '' and to_date == '':
                date_filter = f"WHERE `created` = '{from_date}' "
            elif from_date != '' and to_date != '':
                date_filter = f"WHERE `created` BETWEEN CAST('{from_date}' AS DATE) AND CAST('{to_date}' AS DATE) "
            else:
                date_filter = f"WHERE `created` = '{todays_date}' "

            stmt += date_filter
            stmt += 'GROUP BY vote_name ORDER BY COUNT(votes) DESC LIMIT 12'
            total_votes_stmt += date_filter

        votes = frappe.db.sql(stmt, as_dict=True)
        total_votes = frappe.db.sql(total_votes_stmt, as_dict=True)
        # frappe.msgprint(str(votes))

        frappe.response['message'] = {
            "success_key": 1,
            "user": frappe.session.user,
            "votes": votes,
            "total_votes": total_votes,
        }

@frappe.whitelist(allow_guest=True)
def search_employee(query, ps):

    if ps == 'Latitude' or ps == 'Longitude':
    # search the Employee doctype for possible matches
        employees = frappe.db.sql(f"""SELECT employee_name, image, employee FROM `tabEmployee` WHERE ps='{ps}' AND employee_name LIKE '%{query}%'""", as_dict=True)

        # append possible matches to results list
        frappe.response['message'] = {
        "success_key": 1,
        "message": {
            "employees": employees
        }
        }
        # frappe.msgprint(str(employees))
    else:
        employees = frappe.db.sql(f"""SELECT employee_name, image, employee FROM `tabEmployee` WHERE employee_name LIKE '%{query}%'""", as_dict=True)

        # append possible matches to results list
        frappe.response['message'] = {
        "success_key": 1,
        "message": {
            "employees": employees
        }
        }
        # frappe.msgprint(str(employees))

    return


@frappe.whitelist(allow_guest=True)
def get_employee(ps):
    stmt = ""

    if (ps == 'Latitude'):
        stmt += "SELECT employee_name, image, employee FROM `tabEmployee` WHERE `ps` = 'Latitude' "
    elif (ps == 'Longitude'):
        stmt += "SELECT employee_name, image, employee FROM `tabEmployee` WHERE `ps` = 'Longitude'"
    else:
        stmt += "SELECT employee_name, image, employee FROM `tabEmployee`"

    employees = frappe.db.sql(stmt, as_dict=True)

    frappe.response['message'] = {
        "success_key": 1,
        "employees": employees
    }
    # frappe.msgprint(str(employees))





    # frappe.msgprint(str(todays_day))
    # return frappe.db.sql("SELECT * FROM `tabPS Vote`", as_dict=True)

    # GET RANDOM RECORDS
# items = frappe.get_list("Item", fields=["name", "item_name"], order_by=f"RAND()", limit_page_length=0)


# @frappe.whitelist()
# def get_result(team, from_date='', to_date=''):
#     if frappe.session.user == 'Guest':
#         return frappe.session.user
#         frappe.response['message'] = {
#             "success_key": 0,
#             "user": frappe.session.user,
#             "votes": '',
#             "total_votes": '',
#         }
#     else:
#         if team == 'Latitude' or 'Longitude': 
#             # Do SOmething
#             stmt = f"""SELECT vote_name, ps, COUNT(votes) as votes_today FROM `tabPs_vote` """
#             total_votes_stmt = f"""SELECT vote_name, votes, voter_name, ps, created  FROM `tabPs_vote` """
#             todays_date = '2023-3-12'
#             # todays_date = date.today()

#             if team == "Latitude":
#               add_ps_filter = "WHERE `ps` = 'Latitude' "
#               stmt += add_ps_filter
#               total_votes_stmt += add_ps_filter
#             elif team == "Longitude":
#               add_ps_filter = "WHERE `ps` = 'Longitude' "
#               stmt += add_ps_filter
#               total_votes_stmt += add_ps_filter
#             else: 
#               add_ps_filter = ''
#               stmt += add_ps_filter
#               total_votes_stmt += add_ps_filter


#             if from_date != '' and to_date == '':
#                 date_filter = f"AND `created` = '{from_date}' "
#             elif from_date != '' and to_date != '':
#                 date_filter = f"AND `created` BETWEEN CAST('{from_date}' AS DATE) AND CAST('{to_date}' AS DATE) " 
#             else:
#                 date_filter = f"AND `created` = '{todays_date}' "


#             stmt += date_filter
#             stmt += 'GROUP BY vote_name ORDER BY COUNT(votes) DESC LIMIT 8'
#             total_votes_stmt += date_filter

#         else: 
#             stmt = f"""SELECT vote_name, ps, COUNT(votes) as votes_today FROM `tabPs_vote` """
#             total_votes_stmt = f"""SELECT vote_name, votes, voter_name, ps, created  FROM `tabPs_vote` """
#             todays_date = '2023-3-12'
#             # todays_date = date.today()

#             if from_date != '' and to_date == '':
#                 date_filter = f"WHERE `created` = '{from_date}' "
#             elif from_date != '' and to_date != '':
#                 date_filter = f"WHERE `created` BETWEEN CAST('{from_date}' AS DATE) AND CAST('{to_date}' AS DATE) " 
#             else:
#                 date_filter = f"WHERE `created` = '{todays_date}' "


#             if team == "Latitude":
#               add_ps_filter = "AND `ps` = 'Latitude' "
#               stmt += add_ps_filter
#               total_votes_stmt += add_ps_filter
#             elif team == "Longitude":
#               add_ps_filter = "AND `ps` = 'Longitude' "
#               stmt += add_ps_filter
#               total_votes_stmt += add_ps_filter
#             else: 
#               add_ps_filter = ''
#               stmt += add_ps_filter
#               total_votes_stmt += add_ps_filter


#             stmt += date_filter
#             stmt += 'GROUP BY vote_name ORDER BY COUNT(votes) DESC LIMIT 8'
#             total_votes_stmt += date_filter

#         votes = frappe.db.sql(stmt, as_dict=True)
#         total_votes = frappe.db.sql(total_votes_stmt, as_dict=True)
#         frappe.response['message'] = {
#             "success_key": 1,
#             "user": frappe.session.user,
#             "votes": votes,
#             "total_votes": total_votes,
#         }
