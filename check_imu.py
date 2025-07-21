import depthai as dai

try:
    with dai.Device() as device:
        # Get device calibration data
        calibData = device.readCalibration()
        # Try to get IMU extrinsics
        try:
            imu_extrinsics = calibData.getImuToCameraExtrinsics(dai.CameraBoardSocket.CAM_A)
            print("IMU detected!")
            print("IMU Extrinsics (relative to CAM_A):")
            print(imu_extrinsics)
            # You can also try to enable IMU streams
            pipeline = dai.Pipeline()
            imu = pipeline.create(dai.node.IMU)
            imu.enableIMUSensor(dai.IMUSensor.ACCELEROMETER_RAW, 200) # Enable accelerometer at 200Hz
            imu.enableIMUSensor(dai.IMUSensor.GYROSCOPE_RAW, 200)    # Enable gyroscope at 200Hz
            imu.setBatchReportThreshold(1)
            imu.setMaxBatchReports(1)

            xout_imu = pipeline.create(dai.node.XLinkOut)
            xout_imu.setStreamName("imu_data")
            imu.out.link(xout_imu.input)

            device.startPipeline(pipeline)
            imu_queue = device.getOutputQueue(name="imu_data", maxSize=8, blocking=False)

            print("\nAttempting to read IMU data (press Ctrl+C to stop)...")
            while True:
                imu_data = imu_queue.get()  # Blocking call, will wait until a new data has arrived
                if imu_data:
                    for packet in imu_data.packets:
                        print(f"Accelerometer: X={packet.accelMps.x:.2f} Y={packet.accelMps.y:.2f} Z={packet.accelMps.z:.2f} m/s^2")
                        print(f"Gyroscope: X={packet.gyroRad.x:.2f} Y={packet.gyroRad.y:.2f} Z={packet.gyroRad.z:.2f} rad/s")
                        break # Just show one packet for brevity
                time.sleep(0.1)

        except RuntimeError as e:
            if "IMU not detected" in str(e) or "imu" in str(e).lower() and "failed" in str(e).lower():
                print("IMU not detected on this OAK-D Lite.")
            else:
                print(f"An error occurred while checking for IMU: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

except RuntimeError as e:
    print(f"Could not connect to OAK-D Lite: {e}")
    print("Ensure the camera is connected and the depthai-ros drivers are installed correctly.")