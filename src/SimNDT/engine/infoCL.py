#!/usr/bin/env python
# encoding: utf-8
"""
infoCL.py

Created by Miguel Molero on 2013-10-01.
Copyright (c) 2013 MMolero. All rights reserved.
"""

global ErrorImportCL
import numpy as    np

try:
    import pyopencl    as    cl

    ErrorImportCL = False
    print("ErrorImportCL--------->", ErrorImportCL)

except ImportError:
    ErrorImportCL = True
    print("ErrorImportCL--------->", ErrorImportCL)

import copy


def importCL():
    global ErrorImportCL
    return not ErrorImportCL


def getPlatforms():
    return cl.get_platforms()


def getPlatformsInfo():
    for p in cl.get_platforms():
        # Print out some information about the platforms
        print("Platform:", p.name)
        print("Vendor:", p.vendor)
        print("Version:", p.version)


def getDevices():
    return [device for platform in cl.get_platforms() for device in platform.get_devices()]


def getPlatformsAndDevices():
    return [(platform, device) for platform in cl.get_platforms() for device in platform.get_devices()]


def getDevice(DEVICE):
    try:
        return [device for platform in cl.get_platforms()
                for device in platform.get_devices()
                if cl.device_type.to_string(device.type) == DEVICE]
    except:
        return cl.get_platforms()[0].get_devices()


def getDevicesName():
    return [cl.device_type.to_string(device.type) for platform in cl.get_platforms()
            for device in platform.get_devices()]


def getDevicesInfo():
    for platform in cl.get_platforms():
        for d in platform.get_devices():
            print("\t-------------------------")
            # Print out some information about the devices
            print("\t\tName:", d.name)
            print("\t\tVersion:", d.opencl_c_version)
            print("\t\tMax. Compute Units:", d.max_compute_units)
            print("\t\tLocal Memory Size:", d.local_mem_size / 1024, "KB")
            print("\t\tGlobal Memory Size:", d.global_mem_size / (1024 * 1024), "MB")
            print("\t\tMax Alloc Size:", d.max_mem_alloc_size / (1024 * 1024), "MB")
            print("\t\tMax Work-group Size:", d.max_work_group_size)

            # Find the maximum dimensions of the work-groups
            dim = d.max_work_item_sizes
            print("\t\tMax Work-item Dims:(", dim[0], " ".join(map(str, dim[1:])), ")")

            print("\t-------------------------")
            print(dim)
            print("\n-------------------------")
