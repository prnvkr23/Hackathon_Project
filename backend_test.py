import requests
import sys
import json
from datetime import datetime
import time

class SmartComplaintPortalTester:
    def __init__(self, base_url="https://fixmate-ai-1.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.student_token = None
        self.admin_token = None
        self.student_user = None
        self.admin_user = None
        self.tests_run = 0
        self.tests_passed = 0
        self.complaint_ids = []

    def run_test(self, name, method, endpoint, expected_status, data=None, token=None, headers=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}" if not endpoint.startswith('http') else endpoint
        test_headers = {'Content-Type': 'application/json'}
        
        if token:
            test_headers['Authorization'] = f'Bearer {token}'
        if headers:
            test_headers.update(headers)

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=test_headers, timeout=30)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=test_headers, timeout=30)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=test_headers, timeout=30)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    return True, response.json()
                except:
                    return True, response.text
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_root_endpoint(self):
        """Test root API endpoint"""
        return self.run_test("Root API Endpoint", "GET", "", 200)

    def test_student_registration(self):
        """Test student registration"""
        timestamp = datetime.now().strftime('%H%M%S')
        student_data = {
            "name": "Test Student",
            "email": f"student{timestamp}@test.com",
            "password": "test123",
            "role": "student"
        }
        
        success, response = self.run_test(
            "Student Registration",
            "POST",
            "auth/register",
            200,
            data=student_data
        )
        
        if success and 'token' in response:
            self.student_token = response['token']
            self.student_user = response['user']
            print(f"   Student ID: {self.student_user['id']}")
            return True
        return False

    def test_admin_registration(self):
        """Test admin registration"""
        timestamp = datetime.now().strftime('%H%M%S')
        admin_data = {
            "name": "Test Admin",
            "email": f"admin{timestamp}@test.com",
            "password": "admin123",
            "role": "admin"
        }
        
        success, response = self.run_test(
            "Admin Registration",
            "POST",
            "auth/register",
            200,
            data=admin_data
        )
        
        if success and 'token' in response:
            self.admin_token = response['token']
            self.admin_user = response['user']
            print(f"   Admin ID: {self.admin_user['id']}")
            return True
        return False

    def test_duplicate_email_registration(self):
        """Test duplicate email registration should fail"""
        if not self.student_user:
            return False
            
        duplicate_data = {
            "name": "Another User",
            "email": self.student_user['email'],
            "password": "test123",
            "role": "student"
        }
        
        success, _ = self.run_test(
            "Duplicate Email Registration (Should Fail)",
            "POST",
            "auth/register",
            400,
            data=duplicate_data
        )
        return success

    def test_student_login(self):
        """Test student login"""
        if not self.student_user:
            return False
            
        login_data = {
            "email": self.student_user['email'],
            "password": "test123"
        }
        
        success, response = self.run_test(
            "Student Login",
            "POST",
            "auth/login",
            200,
            data=login_data
        )
        
        if success and 'token' in response:
            print(f"   Login successful for: {response['user']['name']}")
            return True
        return False

    def test_invalid_login(self):
        """Test invalid credentials"""
        invalid_data = {
            "email": "nonexistent@test.com",
            "password": "wrongpassword"
        }
        
        return self.run_test(
            "Invalid Login (Should Fail)",
            "POST",
            "auth/login",
            401,
            data=invalid_data
        )[0]

    def test_protected_route_me(self):
        """Test /auth/me endpoint with valid token"""
        if not self.student_token:
            return False
            
        success, response = self.run_test(
            "Get Current User (/auth/me)",
            "GET",
            "auth/me",
            200,
            token=self.student_token
        )
        
        if success:
            print(f"   User: {response.get('name')} ({response.get('role')})")
        return success

    def test_unauthorized_access(self):
        """Test protected route without token"""
        return self.run_test(
            "Unauthorized Access (Should Fail)",
            "GET",
            "auth/me",
            401
        )[0]

    def test_complaint_submission_with_category(self):
        """Test complaint submission with category"""
        if not self.student_token:
            return False
            
        complaint_data = {
            "student_name": self.student_user['name'],
            "category": "Electrical",
            "location": "Classroom 204",
            "description": "Fan in classroom 204 is not working"
        }
        
        success, response = self.run_test(
            "Submit Complaint (With Category)",
            "POST",
            "complaints",
            200,
            data=complaint_data,
            token=self.student_token
        )
        
        if success:
            self.complaint_ids.append(response['id'])
            print(f"   Complaint ID: {response['id']}")
            print(f"   AI Category: {response.get('ai_category')}")
            print(f"   Priority: {response.get('priority')}")
            print(f"   Summary: {response.get('summary')}")
        return success

    def test_complaint_submission_without_category(self):
        """Test complaint submission without category (AI detection)"""
        if not self.student_token:
            return False
            
        complaint_data = {
            "student_name": self.student_user['name'],
            "location": "Lab 301",
            "description": "Electrical spark in lab 301 - dangerous!"
        }
        
        success, response = self.run_test(
            "Submit Complaint (AI Category Detection)",
            "POST",
            "complaints",
            200,
            data=complaint_data,
            token=self.student_token
        )
        
        if success:
            self.complaint_ids.append(response['id'])
            print(f"   Complaint ID: {response['id']}")
            print(f"   AI Category: {response.get('ai_category')}")
            print(f"   Priority: {response.get('priority')}")
            print(f"   Summary: {response.get('summary')}")
            
            # Verify AI detected category and high priority for dangerous situation
            if response.get('priority') == 'High':
                print("   ✅ AI correctly detected HIGH priority for dangerous situation")
            else:
                print(f"   ⚠️  Expected HIGH priority, got: {response.get('priority')}")
        return success

    def test_more_complaint_types(self):
        """Test various complaint types for AI analysis"""
        if not self.student_token:
            return False
            
        test_complaints = [
            {
                "data": {
                    "student_name": self.student_user['name'],
                    "location": "Library",
                    "description": "WiFi is very slow in library"
                },
                "expected_category": "Internet",
                "expected_priority": "Low"
            },
            {
                "data": {
                    "student_name": self.student_user['name'],
                    "location": "3rd Floor Washroom",
                    "description": "Washroom on 3rd floor is extremely dirty"
                },
                "expected_category": "Cleaning",
                "expected_priority": "Medium"
            }
        ]
        
        all_passed = True
        for i, test_case in enumerate(test_complaints):
            success, response = self.run_test(
                f"AI Analysis Test {i+1}",
                "POST",
                "complaints",
                200,
                data=test_case["data"],
                token=self.student_token
            )
            
            if success:
                self.complaint_ids.append(response['id'])
                print(f"   Expected: {test_case['expected_category']}/{test_case['expected_priority']}")
                print(f"   Got: {response.get('ai_category')}/{response.get('priority')}")
            else:
                all_passed = False
                
        return all_passed

    def test_get_student_complaints(self):
        """Test student can see their own complaints"""
        if not self.student_token:
            return False
            
        success, response = self.run_test(
            "Get Student Complaints",
            "GET",
            "complaints",
            200,
            token=self.student_token
        )
        
        if success:
            print(f"   Found {len(response)} complaints for student")
            for complaint in response[:2]:  # Show first 2
                print(f"   - {complaint.get('description')[:50]}... (Status: {complaint.get('status')})")
        return success

    def test_get_admin_complaints(self):
        """Test admin can see all complaints"""
        if not self.admin_token:
            return False
            
        success, response = self.run_test(
            "Get All Complaints (Admin)",
            "GET",
            "complaints",
            200,
            token=self.admin_token
        )
        
        if success:
            print(f"   Admin sees {len(response)} total complaints")
        return success

    def test_admin_update_complaint(self):
        """Test admin can update complaint status"""
        if not self.admin_token or not self.complaint_ids:
            return False
            
        complaint_id = self.complaint_ids[0]
        update_data = {"status": "In Progress"}
        
        success, response = self.run_test(
            "Update Complaint Status (Admin)",
            "PUT",
            f"complaints/{complaint_id}",
            200,
            data=update_data,
            token=self.admin_token
        )
        
        if success:
            print(f"   Updated status to: {response.get('status')}")
        return success

    def test_student_cannot_update_complaint(self):
        """Test student cannot update complaint status"""
        if not self.student_token or not self.complaint_ids:
            return False
            
        complaint_id = self.complaint_ids[0]
        update_data = {"status": "Resolved"}
        
        return self.run_test(
            "Student Update Complaint (Should Fail)",
            "PUT",
            f"complaints/{complaint_id}",
            403,
            data=update_data,
            token=self.student_token
        )[0]

    def test_get_analytics_admin(self):
        """Test admin analytics endpoint"""
        if not self.admin_token:
            return False
            
        success, response = self.run_test(
            "Get Analytics (Admin)",
            "GET",
            "analytics",
            200,
            token=self.admin_token
        )
        
        if success:
            print(f"   Total Complaints: {response.get('total_complaints')}")
            print(f"   Pending: {response.get('pending_count')}")
            print(f"   In Progress: {response.get('in_progress_count')}")
            print(f"   Resolved: {response.get('resolved_count')}")
            print(f"   Categories: {response.get('category_breakdown')}")
            print(f"   Priorities: {response.get('priority_breakdown')}")
        return success

    def test_student_cannot_access_analytics(self):
        """Test student cannot access analytics"""
        if not self.student_token:
            return False
            
        return self.run_test(
            "Student Access Analytics (Should Fail)",
            "GET",
            "analytics",
            403,
            token=self.student_token
        )[0]

    def test_duplicate_detection(self):
        """Test duplicate complaint detection"""
        if not self.student_token or not self.complaint_ids:
            return False
            
        # Submit similar complaints
        similar_complaints = [
            "Fan broken in room 204",
            "Room 204 fan not working", 
            "The fan in classroom 204 is broken"
        ]
        
        for desc in similar_complaints:
            complaint_data = {
                "student_name": self.student_user['name'],
                "location": "Classroom 204",
                "description": desc
            }
            
            success, response = self.run_test(
                f"Submit Similar Complaint",
                "POST",
                "complaints",
                200,
                data=complaint_data,
                token=self.student_token
            )
            
            if success:
                self.complaint_ids.append(response['id'])
        
        # Test duplicate detection endpoint
        if self.complaint_ids:
            complaint_id = self.complaint_ids[0]
            success, response = self.run_test(
                "Get Duplicate Complaints",
                "GET",
                f"complaints/{complaint_id}/duplicates",
                200,
                token=self.student_token
            )
            
            if success:
                duplicates = response.get('duplicates', [])
                print(f"   Found {len(duplicates)} potential duplicates")
                for dup in duplicates[:2]:
                    print(f"   - Similarity: {dup.get('similarity')}% - {dup.get('description')[:40]}...")
            return success
        return False

def main():
    print("🚀 Starting Smart Complaint Portal API Tests")
    print("=" * 60)
    
    tester = SmartComplaintPortalTester()
    
    # Test sequence
    tests = [
        ("Root Endpoint", tester.test_root_endpoint),
        ("Student Registration", tester.test_student_registration),
        ("Admin Registration", tester.test_admin_registration),
        ("Duplicate Email Check", tester.test_duplicate_email_registration),
        ("Student Login", tester.test_student_login),
        ("Invalid Login", tester.test_invalid_login),
        ("Protected Route (/auth/me)", tester.test_protected_route_me),
        ("Unauthorized Access", tester.test_unauthorized_access),
        ("Complaint with Category", tester.test_complaint_submission_with_category),
        ("Complaint AI Detection", tester.test_complaint_submission_without_category),
        ("Various Complaint Types", tester.test_more_complaint_types),
        ("Get Student Complaints", tester.test_get_student_complaints),
        ("Get Admin Complaints", tester.test_get_admin_complaints),
        ("Admin Update Complaint", tester.test_admin_update_complaint),
        ("Student Cannot Update", tester.test_student_cannot_update_complaint),
        ("Admin Analytics", tester.test_get_analytics_admin),
        ("Student Cannot Access Analytics", tester.test_student_cannot_access_analytics),
        ("Duplicate Detection", tester.test_duplicate_detection),
    ]
    
    failed_tests = []
    
    for test_name, test_func in tests:
        try:
            if not test_func():
                failed_tests.append(test_name)
        except Exception as e:
            print(f"❌ {test_name} - Exception: {str(e)}")
            failed_tests.append(test_name)
    
    # Print results
    print("\n" + "=" * 60)
    print(f"📊 TEST RESULTS: {tester.tests_passed}/{tester.tests_run} tests passed")
    
    if failed_tests:
        print(f"\n❌ FAILED TESTS ({len(failed_tests)}):")
        for test in failed_tests:
            print(f"   - {test}")
    else:
        print("\n✅ ALL TESTS PASSED!")
    
    print(f"\n🔑 Test Tokens Generated:")
    print(f"   Student Token: {tester.student_token[:20] if tester.student_token else 'None'}...")
    print(f"   Admin Token: {tester.admin_token[:20] if tester.admin_token else 'None'}...")
    
    return 0 if len(failed_tests) == 0 else 1

if __name__ == "__main__":
    sys.exit(main())