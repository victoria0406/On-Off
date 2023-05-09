# import dash
# from dash import html
# from pages.report import layout as layout_daily
# from pages.weekly import layout as layout_weekly

# dash.register_page(__name__, path_template="/report/<type>")

# def layout(type = 'daily'):
#     if (type == 'daily'):
#         return layout_daily()
#     elif (type == 'weekly'):
#         return layout_weekly()
#     else: 
#         return html.H1('404')