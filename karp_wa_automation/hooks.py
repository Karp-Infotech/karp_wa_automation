app_name = "karp_wa_automation"
app_title = "Karp Wa Automation"
app_publisher = "Karp Infotech"
app_description = "Whatsapp Automations"
app_email = "sushil.pal@gmail.com"
app_license = "unlicense"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "karp_wa_automation",
# 		"logo": "/assets/karp_wa_automation/logo.png",
# 		"title": "Karp Wa Automation",
# 		"route": "/karp_wa_automation",
# 		"has_permission": "karp_wa_automation.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/karp_wa_automation/css/karp_wa_automation.css"
# app_include_js = "/assets/karp_wa_automation/js/karp_wa_automation.js"

# include js, css files in header of web template
# web_include_css = "/assets/karp_wa_automation/css/karp_wa_automation.css"
# web_include_js = "/assets/karp_wa_automation/js/karp_wa_automation.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "karp_wa_automation/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "karp_wa_automation/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "karp_wa_automation.utils.jinja_methods",
# 	"filters": "karp_wa_automation.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "karp_wa_automation.install.before_install"
# after_install = "karp_wa_automation.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "karp_wa_automation.uninstall.before_uninstall"
# after_uninstall = "karp_wa_automation.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "karp_wa_automation.utils.before_app_install"
# after_app_install = "karp_wa_automation.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "karp_wa_automation.utils.before_app_uninstall"
# after_app_uninstall = "karp_wa_automation.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "karp_wa_automation.notifications.get_notification_config"

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

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
# 	"all": [
# 		"karp_wa_automation.tasks.all"
# 	],
# 	"daily": [
# 		"karp_wa_automation.tasks.daily"
# 	],
# 	"hourly": [
# 		"karp_wa_automation.tasks.hourly"
# 	],
# 	"weekly": [
# 		"karp_wa_automation.tasks.weekly"
# 	],
# 	"monthly": [
# 		"karp_wa_automation.tasks.monthly"
# 	],
    "cron": {
            "*/30 9-22 * * *": [
                "karp_wa_automation.automation.wa_automation.send_transactional_wa_msgs"
            ],
            "0 0 1 1 *": [
                "karp_wa_automation.automation.wa_automation.init_wa"
            ]
        }
}

# Testing
# -------

# before_tests = "karp_wa_automation.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "karp_wa_automation.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "karp_wa_automation.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["karp_wa_automation.utils.before_request"]
# after_request = ["karp_wa_automation.utils.after_request"]

# Job Events
# ----------
# before_job = ["karp_wa_automation.utils.before_job"]
# after_job = ["karp_wa_automation.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"karp_wa_automation.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

