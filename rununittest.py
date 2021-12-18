import unittest
import iir_filter
import scipy.signal as signal

"""Function used to collect the IIR filter output influenced by the specifications"""


def getCoefficients(w, order, system_type, input_signal):
    coeff = []
    irr_result = []
    b, a = signal.butter(order, 2 * w, system_type)

    for i in b:
        coeff.append(i)

    for i in a:
        coeff.append(i)

    f = iir_filter.IIR2_filter(coeff)

    for i in range(len(input_signal)):
        irr_result.append(round(f.filter(input_signal[i]), 4))

    return irr_result


"""Function used to collect the IIR filter output influenced by SOS at given specifications"""


def getSOSCoefficients(w, order, system_type, input_signal):
    sos = signal.butter(order, 2 * w, system_type, output='sos')
    sos_check = []

    fi = iir_filter.IIR_filter(sos)

    for i in range(len(input_signal)):
        sos_check.append(round(fi.filter(input_signal[i]), 4))

    return sos_check


"""Unit test class function for a lowpass and highpass filters"""


class TestStringMethods(unittest.TestCase):

    def test_lowpass_2nd_order_filter(self):
        cutoff_freq = 0.1  # define the normalized cutoff frequency
        filter_order = 2  # state the filter order
        filter_type = 'lowpass'  # state the type of filter used
        test_input = [1, 3, 5]  # define the input signal coefficients

        hand_calculated_values = [0.0675, 0.4144, 1.2552]  # array that contains the hand calculated values for the
        # above specification

        filter_calculated_values = getCoefficients(cutoff_freq, filter_order, filter_type,
                                                   test_input)  # array contains the IIR filter output values for the
        # same specification

        self.assertEqual(hand_calculated_values,
                         filter_calculated_values)  # compare both arrays to check if they aer similar

    def test_lowpass_sos_filter(self):
        cutoff_freq = 0.1  # define the normalized cutoff frequency
        filter_order = 2  # state the filter order
        filter_type = 'lowpass'  # state the type of filter used
        test_input = [1, 3, 5]  # define the input signal coefficients

        hand_calculated_values = [0.0675, 0.4144, 1.2552]  # array that contains the hand calculated values for the
        # above specification

        filter_sos_calculated_values = getSOSCoefficients(cutoff_freq, filter_order, filter_type,
                                                          test_input)  # array contains the sos influenced IIR filter
        # output values for the same specification

        self.assertEqual(hand_calculated_values,
                         filter_sos_calculated_values)  # compare both arrays to check if they aer similar

    def test_highpass_2nd_order_filter(self):
        cutoff_freq = 0.3  # define the normalized cutoff frequency
        filter_order = 2  # state the filter order
        filter_type = 'highpass'  # state the type of filter used
        test_input = [6, -8, 3]  # define the input signal coefficients

        hand_calculated_values = [1.2394, -4.5894, 6.6175]  # array that contains the hand calculated values for the
        # above specification

        filter_calculated_values = getCoefficients(cutoff_freq, filter_order, filter_type,
                                                   test_input)  # array contains the IIR filter output values for the
        # same specification

        self.assertEqual(hand_calculated_values,
                         filter_calculated_values)  # compare both arrays to check if they aer similar

    def test_highpass_sos_filter(self):
        cutoff_freq = 0.3  # define the normalized cutoff frequency
        filter_order = 2  # state the filter order
        filter_type = 'highpass'  # state the type of filter used
        test_input = [6, -8, 3]  # define the input signal coefficients

        hand_calculated_values = [1.2394, -4.5894, 6.6175]  # array that contains the hand calculated values for the
        # above specification

        filter_sos_calculated_values = getSOSCoefficients(cutoff_freq, filter_order, filter_type,
                                                          test_input)  # array contains the sos influenced IIR filter
        # output values for the same specification

        self.assertEqual(hand_calculated_values,
                         filter_sos_calculated_values)  # compare both arrays to check if they aer similar


if __name__ == '__main__':
    unittest.main()
