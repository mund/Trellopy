from mock import Mock
import trellis

if __name__ == '__main__':
	tr = trellis.Trellis()
	mock_trellis = Mock(spec=tr,return_value=tr)
	mock_trellis.parse_input()