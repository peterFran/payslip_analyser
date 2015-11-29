import os
import unittest

import analyser


class TestAnalyser(unittest.TestCase):
    def test_p60_deleted(self):
        directory = './resources'
        payslips = analyser.get_payslips(directory, 'pdf')
        self.assertFalse('PP8400.P60.GB109521.P2014.D140506.T1053.PDF' in payslips)
        result = ['PP8400.GB109521.P201309.D131129.pdf',
                  'PP8400.GB109521.P201412.D150313.pdf',
                  'PP8400.GB109521.P201504.D150629.pdf',
                  'PP8400.GB109521.P201405.D140730.pdf',
                  'PP8400.GB109521.P201508.D151030.pdf',
                  'PP8400.GB109521.P201505.D150730.pdf',
                  'PP8400.GB109521.P201411.D150130.pdf',
                  'PP8400.GB109521.P201506.D150828.pdf',
                  'PP8400.GB109521.P201406.D140901.pdf',
                  'PP8400.GB109521.P201501.D150327.pdf',
                  'PP8400.GB109521.P201502.D150428.pdf',
                  'PP8400.GB109521.P201308.D131030.pdf',
                  'PP8400.GB109521.P201401.D140331.pdf',
                  'PP8400.GB109521.P201409.D141201.pdf',
                  'PP8400.GB109521.P201507.D150929.pdf',
                  'PP8400.GB109521.P201402.D140428.pdf',
                  'PP8400.GB109521.P201503.D150601.pdf',
                  'PP8400.GB109521.P201312.D140227.pdf',
                  'PP8400.GB109521.P201407.D140929.pdf',
                  'PP8400.GB109521.P201310.D131220.pdf',
                  'PP8400.GB109521.P201311.D140130.pdf',
                  'PP8400.GB109521.P201307.D130930.pdf',
                  'PP8400.GB109521.P201404.D140630.pdf',
                  'PP8400.GB109521.P201410.D141219.pdf',
                  'PP8400.GB109521.P201408.D141030.pdf']
        self.assertListEqual(sorted(result), sorted(payslips))

    def test_async(self):
        directory = './resources'
        payslips = analyser.get_payslips(directory, 'pdf')
        payslips_dir = ["{}/{}".format(directory, slip) for slip in payslips]
        rv = analyser.asynchronously_convert_pdfs(payslips_dir, "./images")
        self.assertListEqual(sorted(rv), sorted(analyser.get_payslips('./images', 'jpg', True)))

    def test_tesseract(self):
        directory = './images'
        payslips = analyser.get_payslips(directory, 'jpg')
        payslips_dir = ["{}/{}".format(directory, slip) for slip in payslips]
        rv = analyser.asynchronously_convert_pdfs(payslips_dir, "./images")
        images = analyser.get_payslips('./images', 'jpg', True)
        rv = analyser.asynchronously_tesseract_images(rv)
        jpegs = analyser.get_payslips('./images', 'jpg', True)
        print(rv)
        # self.assertListEqual(sorted(rv), sorted(jpegs))
        self.assertEqual("a", "a")

    def tearDown(self):
        import shutil
        shutil.rmtree('./images')
        os.mkdir('./images')
        a = analyser.get_payslips('./images', 'jpg', True)
        self.assertTrue(len(a) == 0)
        self.assertListEqual([], a)


if __name__ == '__main__':
    unittest.main()
