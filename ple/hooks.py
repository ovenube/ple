# -*- coding: utf-8 -*-
from __future__ import unicode_literals

app_name = "ple"
app_title = "PLE-PERU"
app_publisher = "seethersan"
app_description = "App para la elaboracion de libros electronicos SUNAT PERU"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "carlos_jcez@hotmail.com"
app_version = "1.0.0"
app_license = "MIT"
fixtures = ["Custom Field", "Custom Script"]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/ple/css/ple.css"
# app_include_js = "/assets/ple/js/ple.js"

# include js, css files in header of web template
# web_include_css = "/assets/ple/css/ple.css"
# web_include_js = "/assets/ple/js/ple.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "ple.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "ple.install.before_install"
after_install = "ple.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "ple.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"ple.tasks.all"
# 	],
# 	"daily": [
# 		"ple.tasks.daily"
# 	],
# 	"hourly": [
# 		"ple.tasks.hourly"
# 	],
# 	"weekly": [
# 		"ple.tasks.weekly"
# 	]
# 	"monthly": [
# 		"ple.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "ple.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "ple.event.get_events"
# }

