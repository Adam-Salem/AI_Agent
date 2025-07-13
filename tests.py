from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file
import unittest

class TestFileInfo(unittest.TestCase):
    
    # get_file_info test cases
    
    # def test_calculator_info(self):
    #     result = get_files_info("calculator", ".")
    #     print("Result for current directory:")
    #     print(result)
    #     self.assertEqual(result, "- main.py: file_size=575 bytes, is_dir=False\n- pkg: file_size=4096 bytes, is_dir=True\n- tests.py: file_size=1342 bytes, is_dir=False")
        
    # def test_pkg_info(self):
    #     result = get_files_info("calculator", "pkg")
    #     print("Result for 'pkg' directory:")
    #     print(result)
    #     self.assertEqual(result, "- __pycache__: file_size=4096 bytes, is_dir=True\n- calculator.py: file_size=1737 bytes, is_dir=False\n- render.py: file_size=766 bytes, is_dir=False")
        
    # def test_bin_info(self):
    #     result = get_files_info("calculator", "/bin")
    #     print("Result for '/bin' directory:")
    #     self.assertEqual(result, "Error: Cannot list \"/bin\" as it is outside the permitted working directory")
        
    # def test_calculator_info_2(self):
    #     result = get_files_info("calculator", "../")
    #     print("Result for '../' directory:")
    #     print(result)
    #     self.assertEqual(result, "Error: Cannot list \"../\" as it is outside the permitted working directory")
        
    # get_file_content test cases
    
    # def test_lorem_output(self):
    #     result = get_file_content("calculator", "lorem.txt")
    #     print(result)

    # def test_main_output(self):
    #     result = get_file_content("calculator", "main.py")
    #     print(result)
    #     self.assertTrue(result.startswith("# main.py"))
        
    # def test_calc_output(self):
    #     result = get_file_content("calculator", "pkg/calculator.py")
    #     print(result)
    #     self.assertTrue(result.startswith("# calculator.py"))

    # def test_bad_output(self):
    #     result = get_file_content("calculator", "/bin/cat")
    #     print(result)
    #     self.assertEqual(result, 'Error: Cannot read "/bin/cat" as it is outside the permitted working directory')
    
    # write_file test cases
    
    def test_write_lorem(self):
        result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
        print(result)
        self.assertEqual(result, 'Successfully wrote to "lorem.txt" (28 characters written)')
        
    def test_write_more_lorem(self):
        result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
        print(result)
        self.assertEqual(result, 'Successfully wrote to "pkg/morelorem.txt" (26 characters written)')

    def test_write_temp(self):
        result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
        print(result)
        self.assertEqual(result, 'Error: Cannot write to "/tmp/temp.txt" as it is outside the permitted working directory')

    def test_run_main(self):
        result = run_python_file("calculator", "main.py")
        print(result)
        self.assertEqual(result, 'STDOUT:Calculator App\nUsage: python main.py "<expression>"\nExample: python main.py "3 + 5"\n')
        
    def test_run_tests(self):
        result = run_python_file("calculator", "tests.py")
        print(result)
        self.assertEqual(result, 'STDERR:.........\n----------------------------------------------------------------------\nRan 9 tests in 0.000s\n\nOK\n')
    
    def test_run_bad_main(self):
        result = run_python_file("calculator", "../main.py")
        print(result)
        self.assertEqual(result, 'Error: Cannot execute "../main.py" as it is outside the permitted working directory')
        
    def test_run_nonexistent(self):
        result = run_python_file("calculator", "nonexistent.py")
        print(result)
        self.assertEqual(result, 'Error: File "nonexistent.py" not found')
    
if __name__ == "__main__":
    unittest.main()