# -*- coding: utf-8 -*-
from SciDataTool.Functions import AxisError, axes_dict, rev_axes_dict


def comp_axes(self, axes_list):
    """Completes the RequestedAxis objects in axes_list.
    Parameters
    ----------
    self: Data
        a Data object
    axes_list: list
        a list of RequestedAxis objects
    Returns
    -------
    list of RequestedAxis objects
    """
    
    # Check if the requested axis is defined in the Data object
    for axis_requested in axes_list:
        axis_name = axis_requested.name
        for index, axis in enumerate(self.axes):
            if axis.name == axis_name:
                axis_requested.index = index
                axis_requested.corr_name = axis_name
        if axis_requested.index is None:
            # Check if requested axis is in correspondance dicts
            if axis_name in axes_dict.keys():
                for index, axis in enumerate(self.axes):
                    if axis.name == axes_dict[axis_name][0]:
                        axis_requested.corr_name = axes_dict[axis_name][0]
                        axis_requested.operation = axes_dict[axis_name][0]+"_to_"+axis_name
                        axis_requested.transform = axes_dict[axis_name][1]
                        axis_requested.index = index
                if axis_requested.index is None:
                    raise AxisError("ERROR: Requested axis [" + axis_name + "] is not available")
            elif axis_name in rev_axes_dict.keys():
                for index, axis in enumerate(self.axes):
                    if axis.name == rev_axes_dict[axis_name][0]:
                        axis_requested.corr_name = rev_axes_dict[axis_name][0]
                        axis_requested.operation = rev_axes_dict[axis_name][0]+"_to_"+axis_name
                        axis_requested.transform = rev_axes_dict[axis_name][1]
                        axis_requested.index = index
                if axis_requested.index is None:
                    raise AxisError("ERROR: Requested axis [" + axis_name + "] is not available")
            else:
                # Axis does not exist and is ignored
                axes_list.remove(axis_requested)
    # Extract the requested axes (symmetries + unit)
    for axis_requested in axes_list:
        axis_requested.get_axis(self.axes[axis_requested.index], self.normalizations)
    return axes_list
        