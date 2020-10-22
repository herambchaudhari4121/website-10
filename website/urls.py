"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from weatherSys import views
from live_data import views as v
from chongqing import views as chongqing_v


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),

    path('login', views.login),
    path('feature_now', views.feature_now),
    path('features', views.features),
    path('show_equip', views.show_equip),
    path('features_filter', views.features_filter),
    path('equip_name', views.equip_name),
    path('features_his', views.features_his),
    path('all_service', views.all_service),
    # path('console/', views.console),
    # path('console/add_service/', views.add_service),
    path('add_user', views.add_user),
    path('unconnected_equip', views.unconnected_equip),
    path('add_service', views.add_service),
    # path('console/add_soil/', views.add_soil),
    # path('console/service/', views.service),
    # path('console/service_manage/', views.service_manage),
    # path('console/user_manage/', views.user_manage),
    path('delete_user', views.delete_user),
    path('user_list', views.user_list),
    path('modify_user', views.modify_user),
    path('add_service', views.add_service),
    path('location_tree', views.location_tree),
    path('initial_data', views.initial_data),
    path('modify_service', views.modify_service),
    path('delete_service', views.delete_service),
    path('map_point', views.map_point),
    path('get_status', views.get_status),
    # path('service_connection', views.service_connection),
    path('equip_type', views.equip_type),
    path('add_equipments', views.add_equipments),
    path('unconnected_assist_equip', views.unconnected_assist_equip),
    path('delete_equipments', views.delete_equipments),
    path('equip_all_info', views.equip_all_info),
    path('show_dict', views.show_dict),
    path('manage_equipments', views.manage_equipments),
    path('manage_parameter', views.manage_parameter),
    path('objects_under_service', views.objects_under_service),
    path('manage_connection', views.manage_connection),
    path('river_data',views.river_data),
    path('line_data', views.line_data),
    path('get_warning', views.get_warning),
    path('wb_test', views.wb_test),
    # path('show_requests', views.show_requests),
    # path('set_weather_time', views.set_weather_time),
    # path('set_weather_id', views.set_weather_id),
    # path('get_weather_id', views.get_weather_id),
    # path('socket_test/', views.socket_test),
    # path('send_socket', views.send_socket),
    # path('re_write_data', views.re_write_data),
    # path('ws_test', views.ws_test),
    # path('stability_test', views.stability_test),
    # path('get_time', views.get_time),
    # path('set_time', views.set_time),
    path('soil_live_collection', views.soil_live_collection),
    # path('get_message', views.get_message),
    # path('select_equipment', views.select_equipment),
    path('live_data_distribution', v.live_data_distribution),
    path('get_live_data', v.get_live_data),
    path('reverse_features', views.reverse_features),
    path('device_remote_control', v.device_remote_control),
    path('generate_file', views.generate_file),
    path('rain_fall_data', views.rain_fall_data),
    path('get_success_rate', views.get_success_rate),
    path('soil_map', chongqing_v.soil_map),
    path('soil_data_receive', chongqing_v.soil_data_receive),
    path('report_rate',chongqing_v.report_rate),
    path('get_report', chongqing_v.get_report),
    path('district_station', chongqing_v.district_station),
    path('chongqing_features', chongqing_v.chongqing_features),
    path('chongqing_statistic', chongqing_v.chongqing_statistic),
    path('chongqing_line', chongqing_v.chongqing_line),
    path('vertical_statistic', chongqing_v.vertical_statistic),
    path('ch_equip_all_info',chongqing_v.equip_all_info),
    path('ch_add_equipments', chongqing_v.add_equipments),
    path('ch_unconnected_assist_equip',chongqing_v.unconnected_assist_equip),
    path('ch_delete_equipments', chongqing_v.delete_equipments),
    path('ch_manage_equipments', chongqing_v.manage_equipments),
    path('ch_manage_parameter', chongqing_v.manage_parameter),
    path('ch_kriging', chongqing_v.kriging),
    path('traffic_line', views.traffic_line),
    # path('socket_close', views.socket_close)
    # path('time_out_test', views.time_out_test)
    # path('close_socket', views.close_socket)
    # path('get_weather_info', views.get_weather_info),
    # path('send_socket', views.send_socket),
    # path('socket_test', views.socket_test),
    # path('json_t', views.json_t)
    # path('console/equipments/', views.equipments),
    # path('console/connect_equipments/', views.connect_equipments),
    # path('wb_test', v.wb_test),
    path('list', v.list),
    path('token_test', views.token_test)
]
