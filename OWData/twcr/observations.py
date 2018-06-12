# (C) British Crown Copyright 2017, Met Office
#
# This code is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This code is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#

# Functions for handling observations.

import version_2c
import version_3
import datetime

def fetch_observations(dtime,version='none'):
    """Get observations from the 20CR archive at NERSC.

    Data wil be stored locally in directory $SCRATCH/20CR, to be retrieved by :func:`load_observations`. If the local files that would be produced already exists, this function does nothing.

    For 20CR version 2c, the data is retrieved in calendar year blocks, and the 'month' and 'day' arguments are ignored. 

    Args:
        dtime (:obj:`datetime.datetime`): Date and time to get observations for.
        version (:obj:`str`): 20CR version to retrieve data for.

    Will retrieve the data for the year of the given date-time. If the selected time is very close to the end of the calendar year, loading data for that time will also need data from the next calendar year (for interpolation). In this case, also fetch the data for the next calendar year. 

    Raises:
        StandardError: If version is not a supported value.
 
    |
    """

    if version=='2c':
        return version_2c.fetch_observations(dtime)
    if version in ('4.5.1','4.5.2'):
        return version_3.fetch_observations(dtime,version)
    raise StandardError("Unsupported version %s" % version)

def load_observations_1file(dtime,version='none'):
    """Load observations from disc, that were used in the assimilation run at the time specified.

    Data must be available in directory $SCRATCH/20CR, previously retrieved by :func:`fetch_observations`.

    Args:
        dtime (:obj:`int`): Date and time of assimilation run.
        version (:obj:`str`): 20CR version to load data from.

    Returns:
        :obj:`pandas.DataFrame`: Dataframe of observations.

    Raises:
        StandardError: Version number not supported, or data not on disc - see :func:`fetch_observations`

    |
    """

    if version=='2c':
        return version_2c.load_observations_1file(dtime)
    if version in ('4.5.1','4.5.2'):
        return version_3.load_observations_1file(dtime,version)
    raise StandardError("Unsupported version %s" % version)

def load_observations(start,end,version='none'):
    """Load observations from disc, for the selected period

    Data must be available in directory $SCRATCH/20CR, previously retrieved by :func:`fetch`.

    Args:
        start (:obj:`datetime.datetime`): Get observations at or after this time.
        end (:obj:`datetime.datetime`): Get observations before this time.
        version (:obj:`str`): 20CR version to load data from.

    Returns:
        :obj:`pandas.DataFrame`: Dataframe of observations.


    Raises:
        StandardError: Version number not supported, or data not on disc - see :func:`fetch_observations`

    |
    """

    if version=='2c':
        return version_2c.load_observations(start,end)
    if version in ('4.5.1','4.5.2'):
        return version_3.load_observations(start,end,version)
    raise StandardError("Unsupported version %s" % version)

def load_observations_fortime(v_time,version='none'):
    """Load observations from disc, that contribute to fields ata given time

    Data must be available in directory $SCRATCH/20CR, previously retrieved by :func:`fetch`.

    At the times when assimilation takes place, all the observations used at that time are provided by :func:`load_observations_1file` - this function serves the same function, but for intermediate times, where fields are obtained by interpolation. It gets all the observations from each field used in the interpolation, and assigns a weight to each one - the same as the weight used in interpolating the fields.

    Args:
        v_time (:obj:`datetime.datetime`): Get observations associated with this time.
        version (:obj:`str`): 20CR version to load data from.

    Returns:
        :obj:`pandas.DataFrame`: same as from :func:`load_observations`, except with aded column 'weight' giving the weight of each observation at the given time.

    Raises:
        StandardError: Version number not supported, or data not on disc - see :func:`fetch_observations`

    |
    """

    if version=='2c':
        return version_2c.load_observations_fortime(v_time)
    if version in ('4.5.1','4.5.2'):
        return version_3.load_observations_fortime(v_time,version)
    raise StandardError("Unsupported version %s" % version)
