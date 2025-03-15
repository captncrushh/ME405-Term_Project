import pyb
import struct

class BNO055:
    BNO055_ADDRESS = 0x28  # Default I2C address

    # Register addresses
    OPR_MODE_REG = 0x3D
    CALIB_STAT_REG = 0x35
    CALIB_DATA_REG = 0x55
    EULER_ANGLES_REG = 0x1A
    GYRO_DATA_REG = 0x14
    
    MODE_CONFIG = 0x00
    MODE_NDOF = 0x0C
    
    def __init__(self, i2c):
        self.i2c = i2c
        self.set_mode(self.MODE_NDOF)
    
    def set_mode(self, mode):
        """Sets the IMU's operating mode."""
        self.i2c.mem_write(mode, self.BNO055_ADDRESS, self.OPR_MODE_REG)
        pyb.delay(10)
    
    def get_calibration_status(self):
        """Returns a tuple (sys, gyro, accel, mag) indicating calibration levels."""
        status = self.i2c.mem_read(1, self.BNO055_ADDRESS, self.CALIB_STAT_REG)[0]
        sys = (status >> 6) & 0x03
        gyro = (status >> 4) & 0x03
        accel = (status >> 2) & 0x03
        mag = status & 0x03
        return sys, gyro, accel, mag
    
    def get_calibration_data(self):
        """Reads and returns the calibration coefficients as binary data."""
        return self.i2c.mem_read(22, self.BNO055_ADDRESS, self.CALIB_DATA_REG)
    
    def set_calibration_data(self, data):
        """Writes calibration coefficients to the IMU."""
        self.i2c.mem_write(data, self.BNO055_ADDRESS, self.CALIB_DATA_REG)
    
    def get_euler_angles(self):
        """Returns heading, pitch, and roll in degrees."""
        raw = self.i2c.mem_read(6, self.BNO055_ADDRESS, self.EULER_ANGLES_REG)
        if not raw:
            print("IMU read failed!")  # Debugging
            return None, None, None
        
        heading, pitch, roll = struct.unpack('<hhh', raw)
        
        # If the IMU is returning zeros, it's likely not calibrated
        if heading == 0 and pitch == 0 and roll == 0:
            print("Warning: IMU may not be initialized or calibrated.")
        
        return heading / 16.0, pitch / 16.0, roll / 16.0

    def get_heading(self):
        """Returns only the heading angle."""
        return self.get_euler_angles()[0]
    
    def get_angular_velocity(self):
        """Returns angular velocity (gyro x, y, z) in degrees per second."""
        raw = self.i2c.mem_read(6, self.BNO055_ADDRESS, self.GYRO_DATA_REG)
        x, y, z = struct.unpack('<hhh', raw)
        return x / 16.0, y / 16.0, z / 16.0
    
    def get_yaw_rate(self):
        """Returns only the yaw rate."""
        return self.get_angular_velocity()[2]
