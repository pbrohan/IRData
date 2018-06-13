import unittest
from mock import patch

import OWData.twcr as twcr
import datetime
import sys
import os
import os.path
import shutil
import tempfile
import iris
import cf_units
import numpy

version='2c'
 
# Can only load data if it's on disc - create fake data file
def fake_data_file(variable,version,year):
    file_name="%s/20CR/version_%s/hourly/%04d/%s.nc" % (
                 os.environ["SCRATCH"],
                 version,
                 year,
                 variable)
    if os.path.isfile(file_name): return
    if not os.path.isdir(os.path.dirname(file_name)):
        os.makedirs(os.path.dirname(file_name))
    fh=open(file_name,'a')
    fh.close()

# Will mock calls to iris.load_cube with a fake cube constructor
def fake_cube(file_name,constraint):

    year=int(constraint.__dict__['_coord_values']['time'].year)
    month=int(constraint.__dict__['_coord_values']['time'].month)
    day=int(constraint.__dict__['_coord_values']['time'].day)
    hour=int(constraint.__dict__['_coord_values']['time'].hour)
    try:
        minute=int(constraint.__dict__['_coord_values']['time'].minute)
    except:
        minute=0
    dtime=datetime.datetime(year,month,day,hour,minute)

    ensemble = iris.coords.DimCoord(numpy.linspace( 0, 9, 10 ),
                                    long_name='member')
    latitude = iris.coords.DimCoord(numpy.linspace(-90, 90, 19),
                                    standard_name='latitude',
                                    units='degrees')
    longitude = iris.coords.DimCoord(numpy.linspace(-170, 180, 36),
                                     standard_name='longitude',
                                     units='degrees')
    cube = iris.cube.Cube(numpy.zeros((10,19,36),numpy.float32),
                dim_coords_and_dims=[(ensemble,  0),
                                     (latitude,  1),
                                     (longitude, 2)])
    
    dthours=(dtime-datetime.datetime(1900,1,1)).total_seconds()/3600.0
    time      = iris.coords.AuxCoord(dthours,
                                     long_name='time',
                                     var_name='time',
                                     units=cf_units.Unit(
                          'hours since 1900-01-01 00:00:0.0', 
                                      calendar='gregorian'))
    cube.add_aux_coord(time)
    return cube

class TestLoad(unittest.TestCase):
 
    # Controlled and temporary disc environment
    def setUp(self):
        self.oldscratch=os.environ["SCRATCH"]
        os.environ["SCRATCH"]=tempfile.mkdtemp()

    def tearDown(self):
        if os.path.isdir("%s/20CR" % os.environ["SCRATCH"]):
            shutil.rmtree("%s/20CR" % os.environ["SCRATCH"])
        os.rmdir(os.environ["SCRATCH"])
        os.environ["SCRATCH"]=self.oldscratch

    # load prmsl at analysis time
    def test_load_prmsl(self):
        fake_data_file('prmsl',version,2010)
        with patch.object(iris,'load_cube', 
                                side_effect=fake_cube) as mock_load: 
            tc=twcr.load('prmsl',
                         datetime.datetime(2010,3,12,6),
                         version=version)
        # Right dimensions
        self.assertEqual(len(tc.coords()),4)
        # Right ensemble dimension name?
        self.assertEqual(tc.coords()[0].long_name,'member')
        # Right time?
        self.assertEqual(tc.coords()[3].points[0],965934)

    # load prmsl with interpolated time
    def test_load_prmsl_interpolated(self):
        fake_data_file('prmsl',version,2010)
        with patch.object(iris,'load_cube', 
                                side_effect=fake_cube) as mock_load: 
            tc=twcr.load('prmsl',
                         datetime.datetime(2010,3,12,9),
                         version=version)
        # Right dimensions
        self.assertEqual(len(tc.coords()),4)
        # Right ensemble dimension name?
        self.assertEqual(tc.coords()[0].long_name,'member')
        # Right time?
        self.assertEqual(tc.coords()[3].points[0],965937)

    # Dud variable
    def test_fetch_mslp(self):
        with self.assertRaises(StandardError) as cm:
            tc=twcr.load('mslp',
                         datetime.datetime(1969,3,12),
                         version=version)
        self.assertIn("One or more of the files specified did not exist",
                         str(cm.exception))
 
if __name__ == '__main__':
    unittest.main()
