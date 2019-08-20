cmdTable = {
	'ipc_echo_cmd': b'\x01\x10',
	'system_reboot_cmd': b'\x02\x10',
	'system_runtime_get_cmd': b'\x03\x10',
	'system_memory_get_cmd': b'\x04\x10',
	'system_firmware_version_get_cmd': b'\x05\x10',
	'system_factory_cmd': b'\x06\x10',
	'system_flash_lock_set_cmd': b'\x07\x10',
	'system_flash_lock_get_cmd': b'\x08\x10',
	'uart_set_cmd': b'\x09\x10',
	'uart_get_cmd': b'\x0a\x10',
	'power_standby_set_cmd': b'\x0b\x10',
	'power_wifi_ps_set_cmd': b'\x0c\x10',
	'power_wifi_ps_get_cmd': b'\x0d\x10',
	'power_mcu_ps_set_cmd': b'\x0e\x10',
	'power_mcu_ps_get_cmd': b'\x0f\x10',
	'wifi_version_get_cmd': b'\x10\x10',
	'wifi_mac_get_cmd': b'\x11\x10',
	'wifi_scan_cmd': b'\x12\x10',
	'wifi_ip_get_cmd': b'\x13\x10',
	'wifi_link_info_get_cmd': b'\x14\x10',
	'wifi_connect_cmd': b'\x15\x10',
	'wifi_disconnect_cmd': b'\x16\x10',
	'wifi_ap_add_set_cmd': b'\x17\x10',
	'wifi_ap_add_get_cmd': b'\x18\x10',
	'wifi_softap_start_cmd': b'\x19\x10',
	'wifi_softap_stop_cmd': b'\x1a\x10',
	'wifi_softap_state_get_cmd': b'\x1b\x10',
}
eventTable = {
	'ipc_echo_event': b'\x01\x20',
	'system_runtime_get_event': b'\x02\x20',
	'system_memory_get_event': b'\x03\x20',
	'system_firmware_version_get_event': b'\x04\x20',
	'system_flash_lock_get_event': b'\x05\x20',
	'uart_get_event': b'\x06\x20',
	'power_wifi_ps_get_event': b'\x07\x20',
	'power_mcu_ps_get_event': b'\x08\x20',
	'wifi_status_event': b'\x09\x20',
	'wifi_version_get_event': b'\x0a\x20',
	'wifi_mac_get_event': b'\x0b\x20',
	'wifi_scan_event': b'\x0c\x20',
	'wifi_ip_get_event': b'\x0d\x20',
	'wifi_link_info_get_event': b'\x0e\x20',
	'wifi_ap_add_get_event': b'\x0f\x20',
	'wifi_softap_state_get_event': b'\x10\x20',
}
