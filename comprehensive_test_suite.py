#!/usr/bin/env python3
"""
Comprehensive test suite for all transliteration methods - REFACTORED VERSION.
Phase 2: Complete standardized test data for all 21 transliteration methods.
"""
import sys
import os
from datetime import datetime
import json
import argparse

# Add the current directory to the path to import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from model import XlitToolModel

class TransliterationTestSuite:
    """Refactored comprehensive test suite with unified test runner."""
    
    def __init__(self):
        self.model = XlitToolModel()
        self.test_results = []
        self.failed_tests = []
        
        # Test data converted from old format to new unified format
        self.test_data = self._create_unified_test_data()
    
    def run_test_case(self, method_name, test_case):
        """
        Single unified test runner function.
        
        Args:
            method_name (str): Name of transliteration method
            test_case (dict): Test case definition with input, expected, etc.
            
        Returns:
            dict: Test result with all relevant information
        """
        try:
            # Extract test parameters
            test_input = test_case["input"]
            expected_output = test_case.get("expected", "")
            match_case = test_case.get("match_case", False)
            test_name = test_case.get("name", "unnamed_test")
            description = test_case.get("description", "")
            
            # Run transliteration
            success, result, error, warnings = self.model.transliterate(
                method_name, test_input, match_case
            )
            
            # Determine if test passed
            if not success:
                passed = False
            elif expected_output == "":
                # For tests where we just check it doesn't crash
                passed = True
            else:
                passed = result == expected_output
            
            # Create test result
            test_result = {
                "method": method_name,
                "name": test_name,
                "description": description,
                "input": test_input,
                "expected": expected_output,
                "actual": result,
                "match_case": match_case,
                "success": success,
                "error": error,
                "warnings": warnings,
                "passed": passed
            }
            
            return test_result
            
        except Exception as e:
            # Handle unexpected errors in test execution
            return {
                "method": method_name,
                "name": test_case.get("name", "unnamed_test"),
                "description": test_case.get("description", ""),
                "input": test_case.get("input", ""),
                "expected": test_case.get("expected", ""),
                "actual": "",
                "match_case": test_case.get("match_case", False),
                "success": False,
                "error": f"Test execution error: {str(e)}",
                "warnings": [],
                "passed": False
            }
    
    def run_method_tests(self, method_name, failed_only=False):
        """Run all tests for a specific transliteration method."""
        print(f"\n=== Testing {method_name} ===")
        
        method_test_cases = self.test_data.get(method_name, [])
        if not method_test_cases:
            print(f"   ⚠ No test cases defined for {method_name}")
            return []
        
        method_results = []
        
        # If failed_only is True, first run all tests to identify failures
        if failed_only:
            # Run a quick pass to identify failed tests
            failing_test_cases = []
            for test_case in method_test_cases:
                result = self.run_test_case(method_name, test_case)
                if not result["passed"]:
                    failing_test_cases.append(test_case)
            
            if not failing_test_cases:
                print(f"   ✅ No failing tests found for {method_name}")
                return []
            
            test_cases_to_run = failing_test_cases
            print(f"   Found {len(failing_test_cases)} failing tests")
        else:
            test_cases_to_run = method_test_cases
        
        for test_case in test_cases_to_run:
            result = self.run_test_case(method_name, test_case)
            method_results.append(result)
            
            # Print test result
            status = "✓" if result["passed"] else "✗"
            test_name = result["name"]
            print(f"   {status} {test_name}: '{result['actual']}'")
            
            if not result["passed"]:
                if result["error"]:
                    print(f"     Error: {result['error']}")
                elif result["expected"]:
                    print(f"     Expected: '{result['expected']}', Got: '{result['actual']}'")
        
        # Print method summary
        passed = sum(1 for r in method_results if r["passed"])
        total = len(method_results)
        print(f"   Summary: {passed}/{total} tests passed")
        
        return method_results
    
    def run_all_tests(self, method_filter=None, failed_only=False):
        """Run comprehensive tests for all transliteration methods."""
        if method_filter:
            print(f"🧪 Starting Test Suite for: {method_filter}")
        elif failed_only:
            print("🧪 Starting Test Suite for Failed Tests Only")
        else:
            print("🧪 Starting Comprehensive Transliteration Test Suite (Refactored)")
        print("=" * 70)
        
        start_time = datetime.now()
        
        # Get all methods except "Select method"
        all_methods = [m for m in self.model.get_transliteration_methods() if m != "Select method"]
        
        # Filter methods if specified
        if method_filter:
            if method_filter in all_methods:
                methods = [method_filter]
            else:
                print(f"❌ Method '{method_filter}' not found!")
                print(f"Available methods:")
                for method in all_methods:
                    print(f"   - {method}")
                return []
        else:
            methods = all_methods
        
        for method in methods:
            method_results = self.run_method_tests(method, failed_only=failed_only)
            self.test_results.extend(method_results)
            
            # Track failed tests
            failed = [r for r in method_results if not r["passed"]]
            if failed:
                self.failed_tests.extend(failed)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Generate summary report
        self.generate_summary_report(duration)
        
        return self.test_results
    
    def generate_summary_report(self, duration):
        """Generate a comprehensive summary report."""
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r["passed"])
        failed_tests = len(self.failed_tests)
        
        print("\n" + "=" * 70)
        print("📊 TEST SUMMARY REPORT")
        print("=" * 70)
        print(f"⏱  Total Duration: {duration:.2f} seconds")
        print(f"📈 Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"📊 Success Rate: {(passed_tests/total_tests*100):.1f}%")
        
        # Method-wise breakdown
        method_stats = {}
        for result in self.test_results:
            method = result["method"]
            if method not in method_stats:
                method_stats[method] = {"total": 0, "passed": 0}
            method_stats[method]["total"] += 1
            if result["passed"]:
                method_stats[method]["passed"] += 1
        
        print("\n📋 Method-wise Results:")
        for method, stats in method_stats.items():
            success_rate = (stats["passed"] / stats["total"] * 100) if stats["total"] > 0 else 0
            status = "✅" if success_rate == 100 else "⚠️" if success_rate >= 80 else "❌"
            print(f"   {status} {method}: {stats['passed']}/{stats['total']} ({success_rate:.0f}%)")
        
        # Detailed failure report
        if self.failed_tests:
            print("\n🔍 DETAILED FAILURE REPORT:")
            print("-" * 50)
            
            for i, failure in enumerate(self.failed_tests, 1):
                print(f"\n{i}. {failure['method']} - {failure['name']}")
                print(f"   Input: '{failure['input']}'")
                print(f"   Expected: '{failure['expected']}'")
                print(f"   Actual: '{failure['actual']}'")
                if failure['error']:
                    print(f"   Error: {failure['error']}")
                if failure['description']:
                    print(f"   Description: {failure['description']}")
        
        # Save detailed results to file
        self.save_results_to_file()
    
    def show_summary_only(self):
        """Show a concise summary of test coverage without running tests."""
        print("📊 TEST COVERAGE SUMMARY")
        print("=" * 50)
        
        all_methods = [m for m in self.model.get_transliteration_methods() if m != "Select method"]
        total_test_count = 0
        
        print(f"🔍 Available Methods: {len(all_methods)}")
        print("\n📋 Test Coverage by Method:")
        
        for method in all_methods:
            test_cases = self.test_data.get(method, [])
            test_count = len(test_cases)
            total_test_count += test_count
            
            if test_count > 0:
                status = "✅"
            else:
                status = "❌"
            
            print(f"   {status} {method}: {test_count} test cases")
        
        print(f"\n📈 Total Test Cases: {total_test_count}")
        print(f"🎯 Methods with Tests: {len([m for m in all_methods if len(self.test_data.get(m, [])) > 0])}/{len(all_methods)}")
        
        # Show test categories
        print(f"\n🏷️  Common Test Categories:")
        print(f"   • Basic alphabet tests")
        print(f"   • Special character mappings")
        print(f"   • Geographic names (cities, countries)")
        print(f"   • Sample greetings and phrases")
        print(f"   • Method-specific pattern tests")
        
        return total_test_count
    
    def save_results_to_file(self):
        """Save detailed test results to a JSON file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"transliteration_test_results_refactored_{timestamp}.json"
        
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "test_suite_version": "refactored_v1.0",
            "summary": {
                "total_tests": len(self.test_results),
                "passed_tests": sum(1 for r in self.test_results if r["passed"]),
                "failed_tests": len(self.failed_tests),
                "success_rate": sum(1 for r in self.test_results if r["passed"]) / len(self.test_results) * 100 if self.test_results else 0
            },
            "detailed_results": self.test_results,
            "failed_tests": self.failed_tests
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Detailed results saved to: {filename}")
        except Exception as e:
            print(f"\n⚠️  Could not save results to file: {e}")
    
    def _create_unified_test_data(self):
        """
        Each method has a list of named test cases with consistent structure.
        """
        return {
            "Russian (Cyrillic)-->English (IC)": [
                {
                    "name": "basic_alphabet_lowercase",
                    "input": "абвгдеёжзийклмнопрстуфхцчшщъыьэюя",
                    "expected": "abvgdeyezhziyklmnoprstufkhtschshshchyeyuya",
                    "match_case": False,
                    "description": "Complete Cyrillic alphabet transliteration per IC standard"
                },
                {
                    "name": "basic_alphabet_uppercase", 
                    "input": "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
                    "expected": "ABVGDEYeZhZIYKLMNOPRSTUFKhTsChShShchYEYuYa",
                    "match_case": False,
                    "description": "Complete Cyrillic alphabet transliteration (uppercase)"
                },
                {
                    "name": "basic_alphabet_uppercase_match_case", 
                    "input": "АБВГДЕЁЖЗИЙКЛМНО ПРСТУФХЦЧШЩЪЫЬЭЮЯ",
                    "expected": "ABVGDEYEZHZIYKLMNO PRSTUFKHTSCHSHSHCHYEYUYA",
                    "match_case": True,
                    "description": "Complete Cyrillic alphabet transliteration (uppercase, case match)"
                },
                {
                    "name": "е_initial_position",
                    "input": "елка европа Елка Европа",
                    "expected": "yelka yevropa Yelka Yevropa",
                    "match_case": False,
                    "description": "Е/е at word start should be Ye/ye per IC rule"
                },
                {
                    "name": "yo_initial_position",
                    "input": "ёлка ёвропа Ёлка Ёвропа",
                    "expected": "yelka yevropa Yelka Yevropa",
                    "match_case": False,
                    "description": "Ё/ё at word start should be Ye/ye per IC rule"
                },
                {
                    "name": "e_after_consonants_lower_case",
                    "input": "бевегедежезекелеменепересетефехецечешеще",
                    "expected": "bevegedezhezekelemeneperesetefekhetsechesheshche",
                    "match_case": False,
                    "description": "е after consonants should be e per IC rule"
                },
                {
                    "name": "e_after_consonants_upper_case",
                    "input": "БЕВЕГЕДЕЖЕЗЕКЕЛЕМЕНЕПЕРЕСЕТЕФЕХЕЦЕЧЕШЕЩЕ",
                    "expected": "BEVEGEDEZhEZEKELEMENEPERESETEFEKhETsEChEShEShchE",
                    "match_case": False,
                    "description": "Е after consonants should be E per IC rule"
                },
                {
                    "name": "yo_after_consonants_lower_case",
                    "input": "бёвёгёдёжёзёкёлёмёнёпёрёсётёфёхёцёчёшёщё",
                    "expected": "bevegedezhezekelemeneperesetefekhetsechesheshche",
                    "match_case": False,
                    "description": "ё after consonants should be e per IC rule"
                },
                {
                    "name": "yo_after_consonants_upper_case",
                    "input": "БЁВЁГЁДЁЖЁЗЁКЁЛЁМЁНЁПЁРЁСЁТЁФЁХЁЦЁЧЁШЁЩЁ",
                    "expected": "BEVEGEDEZhEZEKELEMENEPERESETEFEKhETsEChEShEShchE",
                    "match_case": False,
                    "description": "Ё after consonants should be E per IC rule"
                },
                {
                    "name": "e_after_vowels",
                    "input": "аеееёеиеоеуеыеэеюеяеАЕЕЕЁЕИЕОЕУЕЫЕЭЕЮЕЯЕ",
                    "expected": "ayeyeyeyeyeiyeoyeuyeyyeeyeyuyeyayeAYeYeYeYeYeIYeOYeUYeYYeEYeYuYeYaYe",
                    "match_case": False,
                    "description": "Е/е after vowels should be Ye/ye per IC rule"
                },
                {
                    "name": "yo_after_vowels",
                    "input": "аёеёёёиёоёуёыёэёюёяёАЕЁЁЁЁИЁОЁУЁЫЁЭЁЮЁЯЁ",
                    "expected": "ayeyeyeyeyeiyeoyeuyeyyeeyeyuyeyayeAYeYeYeYeYeIYeOYeUYeYYeEYeYuYeYaYe",
                    "match_case": False,
                    "description": "Ё/ё after vowels should be Ye/ye per IC rule"
                },
                {
                    "name": "e_yo_after_short_i_hard_soft_signs_lowercase",
                    "input": "съел подъезд объект ателье литьё йё ъё",
                    "expected": "syel podyezd obyekt atelye litye yye ye",
                    "match_case": False,
                    "description": "е/ё after й,ъ,ь should be ye per IC rule"
                },
                {
                    "name": "e_yo_after_short_i_hard_soft_signs_uppercase",
                    "input": "СЪЕЛ ПОДЪЕЗД ОБЪЕКТ АТЕЛЬЕ ЛИТЬЁ ЙЁ ЪЁ",
                    "expected": "SYeL PODYeZD OBYeKT ATELYe LITYe YYe Ye",
                    "match_case": False,
                    "description": "Е/Ё after й,ъ,ь should be Ye per IC rule"
                },
                {
                    "name": "hard_sign_not_represented",
                    "input": "съел подъезд объект СЪЕЛ ПОДЪЕЗД ОБЪЕКТ",
                    "expected": "syel podyezd obyekt SYeL PODYeZD OBYeKT",
                    "match_case": False,
                    "description": "Hard sign ъ not represented per IC standard"
                },
                {
                    "name": "soft_sign_not_represented",
                    "input": "день сильный мать ДЕНЬ СИЛЬНЫЙ МАТЬ",
                    "expected": "den silnyy mat DEN SILNYY MAT",
                    "match_case": False,
                    "description": "Soft sign ь not represented per IC standard"
                },
                {
                    "name": "case_matching_test",
                    "input": "ЧЕМЕЗОВ ШАРАПОВА ШАРАпова ЦЕЛИТЕЛЬ ЦЕЛИтЕЛЬ ЩЕЦИН",
                    "expected": "CHEMEZOV SHARAPOVA ShARApova TSELITEL TsELItEL SHCHETSIN",
                    "match_case": True,
                    "description": "Case matching with uppercase text"
                }
            ],
            
            "Russian (Cyrillic)-->English (BGN)": [
                {
                    "name": "basic_alphabet_lowercase",
                    "input": "абвгдеёжзийклмнопрстуфхцчшщъыьэюя",
                    "expected": "abvgdeyëzhziyklmnoprstufkhtschshshch”y’eyuya",
                    "match_case": False,
                    "description": "Complete Cyrillic alphabet transliteration per BGN standard"
                },
                {
                    "name": "basic_alphabet_uppercase", 
                    "input": "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
                    "expected": "ABVGDEYëZhZIYKLMNOPRSTUFKhTsChShShch”Y’EYuYa",
                    "match_case": False,
                    "description": "Complete Cyrillic alphabet transliteration (uppercase)"
                },
                {
                    "name": "basic_alphabet_uppercase_match_case", 
                    "input": "АБВГДЕЁЖЗИЙКЛМНО ПРСТУФХЦЧШЩЪЫЬЭЮЯ",
                    "expected": "ABVGDEYËZHZIYKLMNO PRSTUFKHTSCHSHSHCH”Y’EYUYA",
                    "match_case": True,
                    "description": "Complete Cyrillic alphabet transliteration (uppercase, case match)"
                },
                {
                    "name": "е_initial_position",
                    "input": "елка европа Елка Европа",
                    "expected": "yelka yevropa Yelka Yevropa",
                    "match_case": False,
                    "description": "Е/е at word start should be Ye/ye per BGN rule"
                },
                {
                    "name": "yo_initial_position",
                    "input": "ёлка ёвропа Ёлка Ёвропа",
                    "expected": "yëlka yëvropa Yëlka Yëvropa",
                    "match_case": False,
                    "description": "Ё/ё at word start should be Ye/ye per BGN rule"
                },
                {
                    "name": "e_after_consonants_lower_case",
                    "input": "бевегедежезекелеменепересетефехецечешеще",
                    "expected": "bevegedezhezekelemeneperesetefekhetsechesheshche",
                    "match_case": False,
                    "description": "е after consonants should be e per BGN rule"
                },
                {
                    "name": "e_after_consonants_upper_case",
                    "input": "БЕВЕГЕДЕЖЕЗЕКЕЛЕМЕНЕПЕРЕСЕТЕФЕХЕЦЕЧЕШЕЩЕ",
                    "expected": "BEVEGEDEZhEZEKELEMENEPERESETEFEKhETsEChEShEShchE",
                    "match_case": False,
                    "description": "Е after consonants should be E per BGN rule"
                },
                {
                    "name": "yo_after_consonants_lower_case",
                    "input": "бёвёгёдёжёзёкёлёмёнёпёрёсётёфёхёцёчёшёщё",
                    "expected": "bëvëgëdëzhëzëkëlëmënëpërësëtëfëkhëtsëchëshëshchë",
                    "match_case": False,
                    "description": "ё after consonants should be ë per BGN rule"
                },
                {
                    "name": "yo_after_consonants_upper_case",
                    "input": "БЁВЁГЁДЁЖЁЗЁКЁЛЁМЁНЁПЁРЁСЁТЁФЁХЁЦЁЧЁШЁЩЁ",
                    "expected": "BËVËGËDËZhËZËKËLËMËNËPËRËSËTËFËKhËTsËChËShËShchË",
                    "match_case": False,
                    "description": "Ё after consonants should be Ë per BGN rule"
                },
                {
                    "name": "e_after_vowels",
                    "input": "аеееёеиеоеуеыеэеюеяеАЕЕЕЁЕИЕОЕУЕЫЕЭЕЮЕЯЕ",
                    "expected": "ayeyeyeyëyeiyeoyeuyeyyeeyeyuyeyayeAYeYeYeYëYeIYeOYeUYeYYeEYeYuYeYaYe",
                    "match_case": False,
                    "description": "Е/е after vowels should be Ye/ye per BGN rule"
                },
                {
                    "name": "yo_after_vowels",
                    "input": "аёеёёёиёоёуёыёэёюёяёАЕЁЁЁЁИЁОЁУЁЫЁЭЁЮЁЯЁ",
                    "expected": "ayëyeyëyëyëiyëoyëuyëyyëeyëyuyëyayëAYeYëYëYëYëIYëOYëUYëYYëEYëYuYëYaYë",
                    "match_case": False,
                    "description": "Ё/ё after vowels should be Yë/yë per BGN rule"
                },
                {
                    "name": "e_yo_after_short_i_hard_soft_signs_lowercase",
                    "input": "съел подъезд объект ателье литьё йё ъё",
                    "expected": "s”yel pod”yezd ob”yekt atel’ye lit’yë yyë ”yë",
                    "match_case": False,
                    "description": "е/ё after й,ъ,ь should be ye and yë per BGN rule"
                },
                {
                    "name": "e_yo_after_short_i_hard_soft_signs_uppercase",
                    "input": "СЪЕЛ ПОДЪЕЗД ОБЪЕКТ АТЕЛЬЕ ЛИТЬЁ ЙЁ ЪЁ",
                    "expected": "S”YeL POD”YeZD OB”YeKT ATEL’Ye LIT’Yë YYë ”Yë",
                    "match_case": False,
                    "description": "Е/Ё after й,ъ,ь should be Ye and Yë per BGN rule"
                },
                {
                    "name": "hard_sign_not_represented",
                    "input": "съел подъезд объект СЪЕЛ ПОДЪЕЗД ОБЪЕКТ",
                    "expected": "s”yel pod”yezd ob”yekt S”YeL POD”YeZD OB”YeKT",
                    "match_case": False,
                    "description": "Hard sign ъ is ” per BGN BGN standard"
                },
                {
                    "name": "soft_sign_not_represented",
                    "input": "день сильный мать ДЕНЬ СИЛЬНЫЙ МАТЬ",
                    "expected": "den’ sil’nyy mat’ DEN’ SIL’NYY MAT’",
                    "match_case": False,
                    "description": "Soft sign ь is ’ per BGN standard"
                },
                {
                    "name": "case_matching_test",
                    "input": "ЧЕМЕЗОВ ШАРАПОВА ШАРАпова ЦЕЛИТЕЛЬ ЦЕЛИтЕЛЬ ЩЕЦИН",
                    "expected": "CHEMEZOV SHARAPOVA ShARApova TSELITEL’ TsELItEL’ SHCHETSIN",
                    "match_case": True,
                    "description": "Case matching with uppercase text"
                }
            ],
            
            "Ukrainian (Cyrillic)-->English (IC)": [
                {
                    "name": "basic_alphabet_lowercase",
                    "input": "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя'’",
                    "expected": "abvhgdeyezhzyiyiyklmnoprstufkhtschshshchyuya",
                    "match_case": False,
                    "description": "Ukrainian Cyrillic alphabet lower case"
                },
                {
                    "name": "basic_alphabet_uppercase",
                    "input": "АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ'’",
                    "expected": "ABVHGDEYeZhZYIYiYKLMNOPRSTUFKhTsChShShchYuYa",
                    "match_case": False,
                    "description": "Ukrainian Cyrillic alphabet upper case"
                },
                {
                    "name": "basic_alphabet_uppercase_match_case",
                    "input": "АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ'’",
                    "expected": "ABVHGDEYEZHZYIYIYKLMNOPRSTUFKHTSCHSHSHCHYUYA",
                    "match_case": True,
                    "description": "Ukrainian Cyrillic alphabet match case"
                },
            ],
            
            "Ukrainian (Cyrillic)-->English (National Standard)": [
                {
                    "name": "basic_alphabet_lowercase",
                    "input": "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя",
                    "expected": "abvhgdeiezhzyiiiklmnoprstufkhtschshshchiuia",
                    "match_case": False,
                    "description": "Ukrainian National Standard alphabet lower case"
                },
                {
                    "name": "basic_alphabet_uppercase",
                    "input": "АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ",
                    "expected": "ABVHGDEIeZhZYIIIKLMNOPRSTUFKhTsChShShchIuIa",
                    "match_case": False,
                    "description": "Ukrainian National Standard alphabet upper case"
                },
                {
                    "name": "basic_alphabet_uppercase_match_case",
                    "input": "АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ",
                    "expected": "ABVHGDEIEZHZYIIIKLMNOPRSTUFKHTSCHSHSHCHIUIA",
                    "match_case": True,
                    "description": "Ukrainian National Standard alphabet match case"
                },
            ],
            
            "Ukrainian (Chinese Academic)-->English": [
                {
                    "name": "Quanzhou",
                    "input": "Цюаньчжоу",
                    "expected": "Quanzhou",
                    "match_case": False,
                    "description": "Basic Ukrainian Chinese Academic transliteration"
                },
                {
                    "name": "Zhangping",
                    "input": "Чжанпін",
                    "expected": "Zhangping",
                    "match_case": False,
                    "description": "Ukrainian Chinese Academic alphabet test"
                },
            ],
            
            "Kazakh (Cyrillic)-->English (IC)": [
                {
                    "name": "basic_alphabet_test",
                    "input": "аәбвгғдеёжзиійкқлмнңоөпрстуүұфхһцчшщыэюяьъ",
                    "expected": "aabvgghdeyozhziiykqlmnngooprstuuufkhhtschshshchyeyuya",
                    "match_case": False,
                    "description": "Kazakh Cyrillic alphabet"
                },
                {
                    "name": "basic_alphabet_test_uppercase",
                    "input": "АӘБВГҒДЕЁЖЗИІЙКҚЛМНҢОӨПРСТУҮҰФХҺЦЧШЩЫЭЮЯЬЪ",
                    "expected": "AABVGGhDEYoZhZIIYKQLMNNgOOPRSTUUUFKhHTsChShShchYEYuYa",
                    "match_case": False,
                    "description": "Kazakh Cyrillic alphabet uppercase"
                },
                {
                    "name": "basic_alphabet_test_uppercase_case_match",
                    "input": "АӘБВГҒДЕЁЖЗИІЙКҚЛМНҢОӨПРСТУҮҰФХҺЦЧШЩЫЭЮЯЬЪ",
                    "expected": "AABVGGHDEYOZHZIIYKQLMNNGOOPRSTUUUFKHHTSCHSHSHCHYEYUYA",
                    "match_case": True,
                    "description": "Kazakh Cyrillic alphabet uppercase case match"
                },
                {
                    "name": "basic_alphabet_test",
                    "input": "Ғғ ғҒ ҒҒ ғғ Жж жЖ ЖЖ жж Ңң ңҢ ҢҢ ңң Хх хХ ХХ хх Цц цЦ ЦЦ цц Чч чЧ ЧЧ чч Шш шШ ШШ шш Щщ щЩ ЩЩ щщ",
                    "expected": "Gh gh Gh gh Zh zh Zh zh Ng ng Ng ng Kh kh Kh kh Ts ts Ts ts Ch ch Ch ch Sh sh Sh sh Shch shch Shch shch",
                    "match_case": False,
                    "description": "Kazakh Cyrillic double multigraphs to single multigraph"
                },
            ],
            
            "Belarussian (Cyrillic)-->English (IC)": [
                {
                    "name": "basic_alphabet_lowercase",
                    "input": "абвгґдеёжзійклмнопрстуўфхцчшыьэюя’'",
                    "expected": "abvhgdyeyozhziyklmnoprstuwfkhtschshyeyuya",
                    "match_case": False,
                    "description": "Belarusian Cyrillic alphabet lowercase"
                },
                {
                    "name": "basic_alphabet_uppercase",
                    "input": "АБВГҐДЕЁЖЗІЙКЛМНОПРСТУЎФХЦЧШЫЬЭЮЯ’'",
                    "expected": "ABVHGDYeYoZhZIYKLMNOPRSTUWFKhTsChShYEYuYa",
                    "match_case": False,
                    "description": "Belarusian Cyrillic alphabet uppercase"
                },
                {
                    "name": "basic_alphabet_uppercase_match_case",
                    "input": "ABVHGDYEYOZHZIYKLMNOPRSTUWFKHTSCHSHYEYUYA’'",
                    "expected": "",
                    "match_case": True,
                    "description": "Belarusian Cyrillic alphabet uppercase match case"
                },
            ],
            
            "Bulgarian (Cyrillic)-->English (IC)": [
                {
                    "name": "basic_alphabet_and_final_ia_lowercase",
                    "input": "абвгдежзийклмнопрстуфхцчшщъьюяия",
                    "expected": "abvgdezhziyklmnoprstufhtschshshtayyuyaia",
                    "match_case": False,
                    "description": "Bulgarian Cyrillic alphabet lowercase, including final ia"
                },
                {
                    "name": "basic_alphabet_and_final_ia_uppercase",
                    "input": "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЬЮЯИЯ",
                    "expected": "ABVGDEZhZIYKLMNOPRSTUFHTsChShShtAYYuYaIA",
                    "match_case": False,
                    "description": "Bulgarian Cyrillic alphabet uppercase, including final ia"
                },
                {
                    "name": "basic_alphabet_and_final_ia_uppercase_case_match",
                    "input": "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЬЮЯИЯ",
                    "expected": "ABVGDEZHZIYKLMNOPRSTUFHTSCHSHSHTAYYUYAIA",
                    "match_case": True,
                    "description": "Bulgarian Cyrillic alphabet uppercase case match, including final ia"
                },
                {
                    "name": "ia_ending_test",
                    "input": "ия ИЯ",
                    "expected": "ia IA",
                    "match_case": False,
                    "description": "Tests regex for ия ending"
                },
                {
                    "name": "digraph_reduction",
                    "input": "Жж жЖ ЖЖ жж Цц цЦ ЦЦ цц Чч чЧ ЧЧ чч Шш шШ ШШ шш Щщ щЩ ЩЩ щщ",
                    "expected": "Zh zh Zh zh Ts ts Ts ts Ch ch Ch ch Sh sh Sh sh Sht sht Sht sht",
                    "match_case": False,
                    "description": "Tests reduction of digraphs"
                },
            ],
            
            "Serbian (Cyrillic)-->English (IC)": [
                {
                    "name": "basic_alphabet_lowercase",
                    "input": "абвгдђежзијклљмнњопрстћуфхцчџш",
                    "expected": "abvgddjezzijklljmnnjoprstcufhccdzs",
                    "match_case": False,
                    "description": "Serbian Cyrillic alphabet lowercase"
                },
                {
                    "name": "basic_alphabet_uppercase",
                    "input": "АБВГДЂЕЖЗИЈКЛЉМНЊОПРСТЋУФХЦЧЏШ",
                    "expected": "ABVGDDjEZZIJKLLjMNNjOPRSTCUFHCCDzS",
                    "match_case": False,
                    "description": "Serbian Cyrillic alphabet uppercase"
                },
                {
                    "name": "basic_alphabet_uppercase_case_match",
                    "input": "АБВГДЂЕЖЗИЈКЛЉМНЊОПРСТЋУФХЦЧЏШ",
                    "expected": "ABVGDDJEZZIJKLLJMNNJOPRSTCUFHCCDZS",
                    "match_case": True,
                    "description": "Serbian Cyrillic alphabet uppercase case match"
                },
            ],
            
            "Tajik (Cyrillic)-->English (IC)": [
                {
                    "name": "basic_alphabet_lowercase",
                    "input": "абвгғдеёжзиӣйкқлмнопрстуӯфхҳчҷшъэюяцщьы",
                    "expected": "abvgghdeyozhziiykqlmnoprstuufkhhchjsheyuyatsshchy",
                    "match_case": False,
                    "description": "Full Tajik Cyrillic alphabet lowercase"
                },
                {
                    "name": "basic_alphabet_uppercase",
                    "input": "АБВГҒДЕЁЖЗИӢЙКҚЛМНОПРСТУӮФХҲЧҶШЪЭЮЯЦЩЬЫ",
                    "expected": "ABVGGhDEYoZhZIIYKQLMNOPRSTUUFKhHChJShEYuYaTsShchY",
                    "match_case": False,
                    "description": "Full Tajik Cyrillic alphabet uppercase"
                },
                {
                    "name": "basic_alphabet_uppercase_case_match",
                    "input": "АБВГҒДЕЁЖЗИӢЙКҚЛМНОПРСТУӮФХҲЧҶШЪЭЮЯЦЩЬЫ",
                    "expected": "ABVGGHDEYOZHZIIYKQLMNOPRSTUUFKHHCHJSHEYUYATSSHCHY",
                    "match_case": True,
                    "description": "Full Tajik Cyrillic alphabet uppercase case match"
                },
                {
                    "name": "ye_initial_position",
                    "input": "Елка елка",
                    "expected": "Yelka yelka",
                    "match_case": False,
                    "description": "Е/е should be Ye/ye per Tajik IC standard"
                },

                {
                    "name": "doubled_multigraphs",
                    "input": "Жж жЖ жж ЖЖ Хх хХ хх ХХ Чч чЧ чч ЧЧ Шш шШ шш ШШ Ғғ ғҒ ғғ ҒҒ Цц цЦ цц ЦЦ Щщ щЩ щщ ЩЩ",
                    "expected": "Zh zh zh Zh Kh kh kh Kh Ch ch ch Ch Sh sh sh Sh Gh gh gh Gh Ts ts ts Ts Shch shch shch Shch",
                    "match_case": False,
                    "description": "Tests consonant + е → consonant + e"
                },
            ],
            
            "Kyrghyz (Cyrillic)-->English (IC)": [
                {
                    "name": "basic_alphabet_lowercase",
                    "input": "абвгдеёжзийклмнңоөпрстуүфхцчшщыэюяьъ",
                    "expected": "abvgdeyojziyklmnngooprstuufkhtschshshchyeyuya",
                    "match_case": False,
                    "description": "Kyrgyz Cyrillic alphabet"
                },
                {
                    "name": "basic_alphabet_upperase",
                    "input": "АБВГДЕЁЖЗИЙКЛМНҢОӨПРСТУҮФХЦЧШЩЫЭЮЯЬЪ",
                    "expected": "ABVGDEYoJZIYKLMNNgOOPRSTUUFKhTsChShShchYEYuYa",
                    "match_case": False,
                    "description": "Kyrgyz Cyrillic alphabet uppercase"
                },
                {
                    "name": "basic_alphabet_uppercase_case_match",
                    "input": "АБВГДЕЁЖЗИЙКЛМНҢОӨПРСТУҮФХЦЧШЩЫЭЮЯЬЪ",
                    "expected": "ABVGDEYOJZIYKLMNNGOOPRSTUUFKHTSCHSHSHCHYEYUYA",
                    "match_case": True,
                    "description": "Kyrgyz Cyrillic alphabet uppercase case match"
                },
                {
                    "name": "multigraphs",
                    "input": "Ңң ңҢ ҢҢ ңң Хх хХ ХХ хх Цц цЦ ЦЦ цц Чч чЧ ЧЧ чч Шш шШ ШШ шш Щщ щЩ ЩЩ щщ",
                    "expected": "Ng ng Ng ng Kh kh Kh kh Ts ts Ts ts Ch ch Ch ch Sh sh Sh sh Shch shch Shch shch",
                    "match_case": False,
                    "description": "Kyrgyz Cyrillic doubled multigraphs to one"
                },
            ],
            
            "Uzbek (Cyrillic)-->English (IC)": [
                {
                    "name": "basic_alphabet_lowercase",
                    "input": "абвгғдеёжзийкқлмнопрстуўфхҳцчшэюяьъ",
                    "expected": "abvgghdeyojziykqlmnoprstuofkhhtschsheyuya",
                    "match_case": False,
                    "description": "Uzbek Cyrillic alphabet (basic)"
                },
                {
                    "name": "basic_alphabet_uppercase",
                    "input": "АБВГҒДЕЁЖЗИЙКҚЛМНОПРСТУЎФХҲЦЧШЭЮЯЬЪ",
                    "expected": "ABVGGhDEYoJZIYKQLMNOPRSTUOFKhHTsChShEYuYa",
                    "match_case": False,
                    "description": "Uzbek Cyrillic alphabet uppercase"
                },
                {
                    "name": "basic_alphabet_uppercase_case_match",
                    "input": "АБВГҒДЕЁЖЗИЙКҚЛМНОПРСТУЎФХҲЦЧШЭЮЯЬЪ",
                    "expected": "ABVGGHDEYOJZIYKQLMNOPRSTUOFKHHTSCHSHEYUYA",
                    "match_case": True,
                    "description": "Uzbek Cyrillic alphabet uppercase case match"
                },
                {
                    "name": "multigraph_test",
                    "input": "Ғғ ғҒ ҒҒ ғғ Хх хХ ХХ хх Цц цЦ ЦЦ цц Чч чЧ ЧЧ чч Шш шШ ШШ шш",
                    "expected": "Gh gh Gh gh Kh kh Kh kh Ts ts Ts ts Ch ch Ch ch Sh sh Sh sh",
                    "match_case": False,
                    "description": "Uzbek multigraph reduction"
                },
            ],
            
            "Tatar (Cyrillic)-->English (IC)": [
                {
                    "name": "basic_alphabet_lowercase",
                    "input": "аәбвгдеёжҗзийклмнңоөпрстуүфхһцчшщыэюяьъ",
                    "expected": "aabvgdeyozhjziyklmnngooprstuufkhhtschshshchyeyuya",
                    "match_case": False,
                    "description": "Tatar Cyrillic alphabet lowercase"
                },
                {
                    "name": "basic_alphabet_uppercase",
                    "input": "АӘБВГДЕЁЖҖЗИЙКЛМНҢОӨПРСТУҮФХҺЦЧШЩЫЭЮЯЬЪ",
                    "expected": "AABVGDEYoZhJZIYKLMNNgOOPRSTUUFKhHTsChShShchYEYuYa",
                    "match_case": False,
                    "description": "Tatar Cyrillic alphabet uppercase"
                },
                {
                    "name": "basic_alphabet_uppercase_case_match",
                    "input": "АӘБВГДЕЁЖҖЗИЙКЛМНҢОӨПРСТУҮФХҺЦЧШЩЫЭЮЯЬЪ",
                    "expected": "AABVGDEYOZHJZIYKLMNNGOOPRSTUUFKHHTSCHSHSHCHYEYUYA",
                    "match_case": True,
                    "description": "Tatar Cyrillic alphabet uppercase case match"
                },
                {
                    "name": "multigraphs",
                    "input": "Жж жЖ ЖЖ жж Ңң ңҢ ҢҢ ңң Хх хХ ХХ хх Цц цЦ ЦЦ цц Чч чЧ ЧЧ чч Шш шШ ШШ шш Щщ щЩ ЩЩ щщ",
                    "expected": "Zh zh Zh zh Ng ng Ng ng Kh kh Kh kh Ts ts Ts ts Ch ch Ch ch Sh sh Sh sh Shch shch Shch shch",
                    "match_case": False,
                    "match_case": False,
                    "description": "Tatar Cyrillic double multigraphs to single"
                },
            ],
            "Mongolian (Cyrillic)-->English (MNS)": [
                {
                    "name": "basic_alphabet_lowercase",
                    "input": "абвгдеёжзийклмноөпрстуүфхцчшщъыьэюя",
                    "expected": "abvgdyeyojziiklmnoöprstuüfkhtschshshiyieyuya",
                    "match_case": False,
                    "description": "Mongolian Cyrillic alphabet lowercase"
                },
                {
                    "name": "basic_alphabet_uppercase",
                    "input": "АБВГДЕЁЖЗИЙКЛМНОӨПРСТУҮФХЦЧШЩЪЫЬЭЮЯ",
                    "expected": "ABVGDYeYoJZIIKLMNOÖPRSTUÜFKhTsChShShIYIEYuYa",
                    "match_case": False,
                    "description": "Mongolian Cyrillic alphabet uppercase"
                },
                {
                    "name": "basic_alphabet_uppercase_case_match",
                    "input": "АБВГДЕЁЖЗИЙКЛМНОӨПРСТУҮФХЦЧШЩЪЫЬЭЮЯ",
                    "expected": "ABVGDYEYOJZIIKLMNOÖPRSTUÜFKHTSCHSHSHIYIEYUYA",
                    "match_case": True,
                    "description": "Mongolian Cyrillic alphabet uppercase case match"
                },
            ],
            "Turkmen (Cyrillic)-->English (IC)": [
                {
                    "name": "basic_alphabet_lowercase",
                    "input": "абвгдеёжҗзийклмнңоөпрстуүфхцчшщыэәюяьъ",
                    "expected": "abvgdeyozhjziyklmnngooprstuufhtschshshchyeayuya",
                    "match_case": False,
                    "description": "Turkmen Cyrillic alphabet lowercase"
                },
                {
                    "name": "basic_alphabet_uppercase",
                    "input": "АБВГДЕЁЖҖЗИЙКЛМНҢОӨПРСТУҮФХЦЧШЩЫЭӘЮЯЬЪ",
                    "expected": "ABVGDEYoZhJZIYKLMNNgOOPRSTUUFHTsChShShchYEAYuYa",
                    "match_case": False,
                    "description": "Turkmen Cyrillic alphabet uppercase"
                },
                {
                    "name": "basic_alphabet_uppercase_case_match",
                    "input": "АБВГДЕЁЖҖЗИЙКЛМНҢОӨПРСТУҮФХЦЧШЩЫЭӘЮЯЬЪ",
                    "expected": "ABVGDEYOZHJZIYKLMNNGOOPRSTUUFHTSCHSHSHCHYEAYUYA",
                    "match_case": True,
                    "description": "Turkmen Cyrillic alphabet uppercase case match"
                },
                {
                    "name": "multigraph_handling",
                    "input": "ЖЖ ҢҢ ЦЦ ЧЧ ШШ ЩЩ Жж Ңң Цц Чч Шш Щщ жЖ ңҢ цЦ чЧ шШ щЩ жж ңң цц чч шш щщ",
                    "expected": "Zh Ng Ts Ch Sh Shch Zh Ng Ts Ch Sh Shch zh ng ts ch sh shch zh ng ts ch sh shch",
                    "match_case": False,
                    "description": "Reduce doubled multigraphs to a single"
                },
            ],
            
            "Azeri (Cyrillic)-->English (IC)": [
                {
                    "name": "basic_alphabet_lowercase",
                    "input": "абвгҝғдеёәжзийјклмноөпрстуүфхһчҹшщыэюяьъ",
                    "expected": "abvggghdeyoazhziyyklmnooprstuufkhhchjshshchyeyuya",  # No expected - basic functionality test
                    "match_case": False,
                    "description": "Azeri Cyrillic alphabet lowercase"
                },
                {
                    "name": "basic_alphabet_uppercase",
                    "input": "АБВГҜҒДЕЁӘЖЗИЙЈКЛМНОӨПРСТУҮФХҺЧҸШЩЫЭЮЯЬЪ",
                    "expected": "ABVGGGhDEYoAZhZIYYKLMNOOPRSTUUFKhHChJShShchYEYuYa",  # No expected - basic functionality test
                    "match_case": False,
                    "description": "Azeri Cyrillic alphabet uppercase"
                },
                {
                    "name": "basic_alphabet_uppercase_match_case",
                    "input": "АБВГҜҒДЕЁӘЖЗИЙЈКЛМНОӨПРСТУҮФХҺЧҸШЩЫЭЮЯЬЪ",
                    "expected": "ABVGGGHDEYOAZHZIYYKLMNOOPRSTUUFKHHCHJSHSHCHYEYUYA",  # No expected - basic functionality test
                    "match_case": True,
                    "description": "Azeri Cyrillic alphabet uppercase match case"
                },
                {
                    "name": "doubled_character_reduction",
                    "input": "ғғ хх жж чч шш щщ ҒҒ ХХ ЖЖ ЧЧ ШШ ЩЩ",
                    "expected": "gh kh zh ch sh shch Gh Kh Zh Ch Sh Shch",  # No expected - basic functionality test
                    "match_case": False,
                    "description": "Azeri Cyrillic doubled letter reduction"
                },
                {
                    "name": "doubled_character_reduction_case_match",
                    "input": "ғғ хх жж чч шш щщ ҒҒ ХХ ЖЖ ЧЧ ШШ ЩЩ",
                    "expected": "gh kh zh ch sh shch GH KH ZH CH SH SHCH",  # No expected - basic functionality test
                    "match_case": True,
                    "description": "Azeri Cyrillic doubled letter reduction case match"
                },
                {
                    "name": "doubled_character_reduction_mixed_case",
                    "input": "Ғғ Хх Жж Чч Шш Щщ ғҒ хХ жЖ чЧ шШ щЩ",
                    "expected": "Gh Kh Zh Ch Sh Shch gh kh zh ch sh shch",  # No expected - basic functionality test
                    "match_case": True,
                    "description": "Azeri Cyrillic doubled letter reduction mixed case"
                },
            ],
            
            "Macedonian (Cyrillic)-->English (IC)": [
                {
                    "name": "basic_alphabet_lowercase",
                    "input": "абвгдѓежзѕијклљмнњопрстќуфхцчџш’'",
                    "expected": "abvgdgjezhzdzijklljmnnjoprstkjufhtschdzhsh",
                    "match_case": False,
                    "description": "Macedonian Cyrillic alphabet lowercase"
                },
                {
                    "name": "basic_alphabet_uppercase",
                    "input": "АБВГДЃЕЖЗЅИЈКЛЉМНЊОПРСТЌУФХЦЧЏШ’'",
                    "expected": "ABVGDGjEZhZDzIJKLLjMNNjOPRSTKjUFHTsChDzhSh",
                    "match_case": False,
                    "description": "Macedonian Cyrillic alphabet uppercase"
                },
                {
                    "name": "basic_alphabet_uppercase_case_match",
                    "input": "АБВГДЃЕЖЗЅИЈКЛЉМНЊОПРСТЌУФХЦЧЏШ’'",
                    "expected": "ABVGDGJEZHZDZIJKLLJMNNJOPRSTKJUFHTSCHDZHSH",
                    "match_case": True,
                    "description": "Macedonian Cyrillic alphabet uppercase case match"
                },
            ],
            
            "Georgian (Cyrillic)-->English (IC)": [
                {
                    "name": "georgian_alphabet",
                    "input": "აბგდევზთიკლმნოპჟრსტუფქღყშჩცძწჭხჯჰ",
                    "expected": "Abgdevztiklmnopzhrstupkghqshchtsdztschkhjh",
                    "match_case": False,
                    "description": "Georgian script alphabet test. First letter capital."
                },
                {
                    "name": "georgian_alphabet_separate_title_case",
                    "input": "ა ბ გ დ ე ვ ზ თ ი კ ლ მ ნ ო პ ჟ რ ს ტ უ ფ ქ ღ ყ შ ჩ ც ძ წ ჭ ხ ჯ ჰ",
                    "expected": "A B G D E V Z T I K L M N O P Zh R S T U P K Gh Q Sh Ch Ts Dz Ts Ch Kh J H",
                    "match_case": False,
                    "description": "Georgian script alphabet test, title case"
                },
            ],
            
            "Uyghur (Cyrillic)-->English (IC)": [
                {
                    "name": "basic_alphabet_lowercase",
                    "input": "аәбвгғдеёжҗзийкқлмнңоөпрстуүфхһчшюяьъ",
                    "expected": "aebwgghdeyojzhziykqlmnngooprstuufxhchshyuya",
                    "match_case": False,
                    "description": "Uyghur Cyrillic alphabet lowercase"
                },
                {
                    "name": "basic_alphabet_uppercase",
                    "input": "АӘБВГҒДЕЁЖҖЗИЙКҚЛМНҢОӨПРСТУҮФХҺЧШЮЯЬЪ",
                    "expected": "AEBWGGhDEYoJZhZIYKQLMNNgOOPRSTUUFXHChShYuYa",
                    "match_case": False,
                    "description": "Uyghur Cyrillic alphabet uppercase"
                },
                {
                    "name": "basic_alphabet_uppercase_case_match",
                    "input": "АӘБВГҒДЕЁЖҖЗИЙКҚЛМНҢОӨПРСТУҮФХҺЧШЮЯЬЪ",
                    "expected": "AEBWGGHDEYOJZHZIYKQLMNNGOOPRSTUUFXHCHSHYUYA",
                    "match_case": True,
                    "description": "Uyghur Cyrillic alphabet uppercase case match"
                },
                {
                    "name": "multigraphs",
                    "input": "Җҗ җҖ ҖҖ җҗ Ғғ ғҒ ҒҒ ғғ Ңң ңҢ ҢҢ ңң Чч чЧ ЧЧ чч Шш шШ ШШ шш",
                    "expected": "Zh zh Zh zh Gh gh Gh gh Ng ng Ng ng Ch ch Ch ch Sh sh Sh sh",
                    "match_case": False,
                    "description": "Uyghur Cyrillic double multigraphs to single"
                },
            ],
            
            # Scientific/Academic Russian Methods
            "Russian (Cyrillic)-->English (Scientific)": [
                {
                    "name": "basic_alphabet_lowercase",
                    "input": "абвгдеёжзийклмнопрстуфхцчшщъыьэюя",
                    "expected": "",  # No expected - basic functionality test
                    "match_case": False,
                    "description": "Russian alphabet for scientific transliteration"
                },
                {
                    "name": "author_chekhov",
                    "input": "Чехов",
                    "expected": "Čexov",
                    "match_case": False,
                    "description": "Russian author name with diacritics"
                },
                {
                    "name": "author_dostoevsky",
                    "input": "Достоевский",
                    "expected": "Dostoevskij",
                    "match_case": False,
                    "description": "Russian author with scientific transliteration"
                },
                {
                    "name": "sample_word",
                    "input": "Литература",
                    "expected": "Literatura",
                    "match_case": False,
                    "description": "Literature in scientific system"
                }
            ],
            
            "Russian (Cyrillic)-->English (ISO-9)": [
                {
                    "name": "basic_alphabet_lowercase",
                    "input": "абвгдеёжзийклмнопрстуфхцчшщъыьэюя",
                    "expected": "",  # No expected - basic functionality test
                    "match_case": False,
                    "description": "Russian alphabet for ISO-9 transliteration"
                },
                {
                    "name": "country_russia",
                    "input": "Россия",
                    "expected": "Rossiâ",
                    "match_case": False,
                    "description": "Russia in ISO-9 system"
                },
                {
                    "name": "capital_moscow",
                    "input": "Москва",
                    "expected": "Moskva",
                    "match_case": False,
                    "description": "Moscow in ISO-9 system"
                },
                {
                    "name": "sample_word",
                    "input": "Федерация",
                    "expected": "Federaciâ",
                    "match_case": False,
                    "description": "Federation in ISO-9 system"
                }
            ],
            
            "Russian (Cyrillic)-->English (ALA-LC)": [
                {
                    "name": "basic_alphabet_lowercase",
                    "input": "абвгдеёжзийклмнопрстуфхцчшщъыьэюя",
                    "expected": "",  # No expected - basic functionality test
                    "match_case": False,
                    "description": "Russian alphabet for ALA-LC transliteration"
                },
                {
                    "name": "library_term",
                    "input": "библиотека",
                    "expected": "biblioteka",
                    "match_case": False,
                    "description": "Library in ALA-LC system"
                },
                {
                    "name": "catalog_term",
                    "input": "каталог",
                    "expected": "katalog",
                    "match_case": False,
                    "description": "Catalog in ALA-LC system"
                },
                {
                    "name": "sample_word",
                    "input": "архив",
                    "expected": "arkhiv",
                    "match_case": False,
                    "description": "Archive in ALA-LC system"
                }
            ],
            
            "Russian (Cyrillic)-->English (Gost 7.79-2000b)": [
                {
                    "name": "basic_alphabet_lowercase",
                    "input": "абвгдеёжзийклмнопрстуфхцчшщъыьэюя",
                    "expected": "",  # No expected - basic functionality test
                    "match_case": False,
                    "description": "Russian alphabet for GOST transliteration"
                },
                {
                    "name": "standard_term",
                    "input": "стандарт",
                    "expected": "standart",
                    "match_case": False,
                    "description": "Standard in GOST system"
                },
                {
                    "name": "system_term",
                    "input": "система",
                    "expected": "sistema",
                    "match_case": False,
                    "description": "System in GOST system"
                },
                {
                    "name": "sample_word",
                    "input": "документ",
                    "expected": "dokument",
                    "match_case": False,
                    "description": "Document in GOST system"
                }
            ],

            "Russian (Chinese Cyrillic)-->English (Pinyin)": [
                {
                    "name": "basic_alphabet_lowercase",
                    "input": "абвгдеёжзийклмнопрстуфхцчшщъыьэюя",
                    "expected": "",  # No expected - basic functionality test
                    "match_case": False,
                    "description": "Russian alphabet for Chinese Pinyin system"
                },
                {
                    "name": "Huangshan",
                    "input": "Хуаншань",
                    "expected": "Huangshan",
                    "match_case": False,
                    "description": "Russian city name in Chinese"
                },
                {
                    "name": "Bozhou",
                    "input": "Бочжоу",
                    "expected": "Bozhou",
                    "match_case": False,
                    "description": "Moscow in Chinese Pinyin"
                },
                {
                    "name": "Quanzhou",
                    "input": "Цюаньчжоу",
                    "expected": "Quanzhou",
                    "match_case": False,
                    "description": "Russia in Chinese Pinyin"
                }
            ],
            
            "Russian (Japanese Cyrillic)-->English (Hepburn)": [
                {
                    "name": "basic_alphabet_lowercase",
                    "input": "абвгдеёжзийклмнопрстуфхцчшщъыьэюя",
                    "expected": "",  # No expected - basic functionality test
                    "match_case": False,
                    "description": "Russian alphabet for Japanese Polivanov Pinyin system"
                },
            ]
        }

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Comprehensive Transliteration Test Suite with command-line options",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python comprehensive_test_suite.py
    Run all tests for all methods

  python comprehensive_test_suite.py --method "Russian (Cyrillic)-->English (IC)"
    Run tests for a specific method only

  python comprehensive_test_suite.py --failed-only
    Run only tests that are currently failing

  python comprehensive_test_suite.py --summary
    Show test coverage summary without running tests

  python comprehensive_test_suite.py --method "Ukrainian (Cyrillic)-->English (IC)" --failed-only
    Run only failing tests for a specific method
        """
    )
    
    parser.add_argument(
        "--method",
        type=str,
        help="Run tests for a specific transliteration method only"
    )
    
    parser.add_argument(
        "--failed-only",
        action="store_true",
        help="Run only tests that are currently failing"
    )
    
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Show test coverage summary without running tests"
    )
    
    return parser.parse_args()

def main():
    """Main entry point for the refactored test suite."""
    args = parse_arguments()
    
    # Create test suite
    test_suite = TransliterationTestSuite()
    
    # Handle summary-only mode
    if args.summary:
        test_suite.show_summary_only()
        return
    
    # Show header based on mode
    print("🚀 Comprehensive Transliteration Test Suite - REFACTORED")
    if args.method and args.failed_only:
        print(f"Mode: Failed tests only for {args.method}")
    elif args.method:
        print(f"Mode: Single method - {args.method}")
    elif args.failed_only:
        print("Mode: Failed tests only")
    else:
        print("Phase 2: Complete standardized test data for all 21 methods")
    print()
    
    # Run tests based on arguments
    results = test_suite.run_all_tests(
        method_filter=args.method,
        failed_only=args.failed_only
    )
    
    # Exit with appropriate code
    failed_count = len(test_suite.failed_tests)
    if failed_count == 0:
        print("\n🎉 All tests passed successfully!")
        sys.exit(0)
    else:
        print(f"\n⚠️  {failed_count} test(s) failed. See report above for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()
