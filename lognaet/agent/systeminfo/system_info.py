# -*- coding: utf-8 -*-
###############################################################################
#
# ODOO (ex OpenERP)
# Open Source Management Solution
# Copyright (C) 2001-2015 Micronaet S.r.l. (<http://www.micronaet.it>)
# Developer: Nicola Riolini @thebrush (<https://it.linkedin.com/in/thebrush>)
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
import pdb
import sys
import psutil
import GPUtil
import platform
from datetime import datetime

# Constant:
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


# -----------------------------------------------------------------------------
# Utility:
# -----------------------------------------------------------------------------
def get_size(bytes, suffix='B'):
    """ Scale bytes to its proper format
        e.g:
            1253656 => '1.20MB'
            1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < factor:
            return '{}{}{}'.format(
                bytes, unit, suffix)
        bytes /= factor


# -----------------------------------------------------------------------------
# Log procedure:
# -----------------------------------------------------------------------------
data = {}

setup = [
    # Library name, Library, Excluded command
    (
        'psutil',
        psutil,
        [
            # Too much data:
            'get_process_list',
            'net_connections',
            'get_pid_list',
            'pids',
            'test',

            # Unused:
            'process_iter',

            # Error data:
            'pid_exists', 'disk_usage', 'sys', 'warnings', 'errno',
            'signal', 'wait_procs', 'callable', 'pwd',
            'time', 'subprocess', 'os',
            ],
        [],
        [
            'avail_phymem',
        ],
    ),
    (
        'platform',
        platform, [
            # Too much data:

            # Error data:
            'popen',
            'string',
            'sys',
            're',
            'os',
            'system_alias',
            ],
        [],
        [],
    ),
    ]

for name, library, excluded, byte_value, byte_function in setup:
    data[name] = {}
    data[name]['info'] = {}
    data[name]['error'] = {}
    for method in dir(library):
        if not method.islower():  # No upper function
            continue
        if method.startswith('_'):
            continue
        if method in excluded:
            # print('Exluded %s > %s' % (name, command))
            continue

        try:
            command = '%s.%s' % (name, method)

            # -----------------------------------------------------------------
            #                        Simple call:
            # -----------------------------------------------------------------
            command_type = type(eval(command))

            # -----------------------------------------------------------------
            # Simple call formatted:
            # -----------------------------------------------------------------
            if name == 'psutil' and method == 'boot_time':
                boot_time = datetime.fromtimestamp(psutil.boot_time())
                data[name]['info']['boot_time'] = boot_time.strftime(
                    DATETIME_FORMAT)

            # -----------------------------------------------------------------
            # Simple call direct:
            # -----------------------------------------------------------------
            elif method in byte_value:
                data[name]['info'][method] = get_size(eval(command))
            elif method in byte_function:
                data[name]['info'][method] = get_size(eval('%s()' % command))
            elif command_type == tuple:
                data[name]['info'][method] = eval(command)
            else:   # Function
                data[name]['info'][method] = eval('%s()' % command)

            # -----------------------------------------------------------------
            #                       Extra Complex call:
            # -----------------------------------------------------------------
            # Disk status (extra call for disk status):
            if name == 'psutil' and method == 'disk_partitions':
                data[name]['info']['disk_usage'] = ''

                for partition in psutil.disk_partitions():
                    try:
                        usage = psutil.disk_usage(
                            partition.mountpoint)
                    except PermissionError:
                        # this can be catch due to the disk that isn't ready
                        continue
                    data[name]['info']['disk_usage'] += \
                        'Dev: %s - MP: %s - FS: %s >> ' \
                        'Tot.: %s - Used: %s - Free: %s - Perc.: %s' % (
                            partition.device,
                            partition.mountpoint,
                            partition.fstype,

                            get_size(usage.total),
                            get_size(usage.used),
                            get_size(usage.free),
                            get_size(usage.percent),
                            )
        except:
            data[name]['error'][method] = sys.exc_info()

for name, library, excluded, byte_value, byte_function in setup:
    for mode in ('info', 'error'):
        print('\n\nLibrary %s, INFO' % name)
        for field in sorted(data[name][mode]):
            print('%s --> %s' % (field, data[name][mode][field]))

"""
# CPU usage per Core
for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
    print(f"Core {i}: {percentage}%")
print(f"Total CPU Usage: {psutil.cpu_percent()}%")

# Memory Information
svmem = psutil.virtual_memory()
print(f"Total: {get_size(svmem.total)}")
print(f"Available: {get_size(svmem.available)}")
print(f"Used: {get_size(svmem.used)}")
print(f"Percentage: {svmem.percent}%")
print("="*20, "SWAP", "="*20)

# get the swap memory details (if exists)
swap = psutil.swap_memory()
print(f"Total: {get_size(swap.total)}")
print(f"Free: {get_size(swap.free)}")
print(f"Used: {get_size(swap.used)}")
print(f"Percentage: {swap.percent}%")

# get IO statistics since boot
disk_io = psutil.disk_io_counters()
disk_io.read_bytes disk_io.write_bytes

# Network information
# get all network interfaces (virtual and physical)
if_addrs = psutil.net_if_addrs()
for interface_name, interface_addresses in if_addrs.items():
    for address in interface_addresses:
        print(f"=== Interface: {interface_name} ===")
        if str(address.family) == 'AddressFamily.AF_INET':
            print(f"  IP Address: {address.address}")
            print(f"  Netmask: {address.netmask}")
            print(f"  Broadcast IP: {address.broadcast}")
        elif str(address.family) == 'AddressFamily.AF_PACKET':
            print(f"  MAC Address: {address.address}")
            print(f"  Netmask: {address.netmask}")
            print(f"  Broadcast MAC: {address.broadcast}")

# GPU information
from tabulate import tabulate
gpus = GPUtil.getGPUs()
list_gpus = []
for gpu in gpus:
    # get the GPU id
    gpu_id = gpu.id
    # name of GPU
    gpu_name = gpu.name
    # get % percentage of GPU usage of that GPU
    gpu_load = f"{gpu.load*100}%"
    # get free memory in MB format
    gpu_free_memory = f"{gpu.memoryFree}MB"
    # get used memory
    gpu_used_memory = f"{gpu.memoryUsed}MB"
    # get total memory
    gpu_total_memory = f"{gpu.memoryTotal}MB"
    # get GPU temperature in Celsius
    gpu_temperature = f"{gpu.temperature} °C"
    gpu_uuid = gpu.uuid
    list_gpus.append((
        gpu_id, gpu_name, gpu_load, gpu_free_memory, gpu_used_memory,
        gpu_total_memory, gpu_temperature, gpu_uuid
    ))

print(tabulate(list_gpus, headers=(
    "id", "name", "load", "free memory", "used memory", "total memory",
    "temperature", "uuid")))

# Boot time:
boot_ts = datetime.fromtimestamp(psutil.boot_time())
data['boot'] = '{}-{}-{} {}:{}:{}'.format(
    boot_ts.year,
    boot_ts.month,
    boot_ts.day,
    boot_ts.hour,
    boot_ts.minute,
    boot_ts.second,
    )

# CPU info
CPU = psutil.cpu_freq()
data['CPU'] = {
    'physical_core': psutil.cpu_count(logical=False),
    'total_core': psutil.cpu_count(logical=True),    
    'frequency_max': CPU.max,  # MHz
    'frequency_min': CPU.min,  # MHz
    'frequency_current': CPU.current,  # MHz
    }
"""
