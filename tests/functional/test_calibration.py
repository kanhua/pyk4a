import pytest

from pyk4a import Calibration, ColorResolution, DepthMode, K4AException


@pytest.fixture()
def calibration(calibration_raw) -> Calibration:
    return Calibration.from_raw(
        calibration_raw, depth_mode=DepthMode.NFOV_UNBINNED, color_resolution=ColorResolution.RES_720P
    )


class TestCalibration:
    @staticmethod
    def test_from_raw_incorrect_data(calibration_raw):
        with pytest.raises(K4AException):
            Calibration.from_raw(
                "none-calibration-json-string", depth_mode=DepthMode.NFOV_UNBINNED, color_resolution=ColorResolution.OFF
            )

    @staticmethod
    def test_from_raw(calibration_raw):
        calibration = Calibration.from_raw(
            calibration_raw, depth_mode=DepthMode.NFOV_UNBINNED, color_resolution=ColorResolution.OFF
        )
        assert calibration

    @staticmethod
    def test_convert_3d_to_2d():

        from pyk4a import CalibrationType,PyK4APlayback

        test_mkv_file = r"C:\Users\kanhu\Documents\2020-12-23data\tomita_20201223_2.mkv"

        ppk = PyK4APlayback(test_mkv_file)
        ppk.open()
        calibration=ppk.calibration

        original_2d_points=(100,100)
        converted_3d_pts=calibration.convert_2d_to_3d(original_2d_points,300.0,CalibrationType.COLOR,CalibrationType.DEPTH)

        converted_2d_pts=calibration.convert_3d_to_2d(converted_3d_pts)
        print(converted_2d_pts)
        ppk.close()
        assert calibration


    @staticmethod
    @pytest.mark.opengl
    def test_creating_transfromation_handle(calibration: Calibration):
        transformation = calibration.transformation_handle
        assert transformation is not None
